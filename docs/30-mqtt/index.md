---
title: MQTT Integration
category: concepts
tags:
- mqtt
- broker
- local-broker
- pub-sub
- messaging
- iot-integration
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints: []
protocols:
- MQTT
- TCP
related_concepts:
- message queues
- publish-subscribe
- integration
- local integration
- mqtt brokers
use_cases:
- mqtt integration
- home automation
- iot platforms
- real-time messaging
real_device_tested: false
---

# MQTT Integration

## Document Context

- **Purpose**: Comprehensive guide for configuring WhatWatt Go MQTT client to publish energy data to MQTT brokers
- **When to use**: Setting up home automation, IoT platforms, real-time messaging systems, local data integration without cloud dependencies
- **Prerequisites**: Basic MQTT concepts (pub/sub, brokers, topics), MQTT broker setup (Mosquitto, etc.), network connectivity knowledge
- **Related to**: MQTT payload templates, reading variables, secure MQTT with TLS, message queuing systems
- **Validates against**: MQTT client configuration and message publishing with real energy meter data

## Key Facts

- **Configuration endpoint**: /api/v1/mqtt/settings (GET, POST, PUT)
- **Connection types**: Unencrypted TCP (mqtt://) and encrypted TLS (mqtts://)
- **Authentication**: Username/password broker authentication supported
- **Client requirements**: Unique client_id per broker, meter connection required for publishing
- **Payload format**: Customizable JSON templates with device variables
- **Topic configuration**: User-defined MQTT topics for message routing
- **TLS options**: Certificate validation with optional CN check skip
- **Publishing trigger**: Only publishes when meter is connected and providing data

The device can be connected to an MQTT broker using the built-in MQTT client. The MQTT client supports both unencrypted and encrypted connections.

!!! note
    WhatWatt Go will only publish values if a meter is connected.

## Configuration via REST API

HTTP REST API to configure MQTT client (you can also do it from the device's WebUI):

| Endpoint              | `api/v1/mqtt/settings` |
| --------------------- | ---------------------- |
| Method                | GET, POST, PUT         |
| Response content type | application/json       |

--8<-- "../_partials/auth-note.md"

## MQTT Settings Object

| Field                | Type    | Default      | Range                                         | Description                                                      |
| -------------------- | ------- | ------------ | --------------------------------------------- | ------------------------------------------------------------ |
| `.enable`            | boolean | false        |                                               | Enables or disables the MQTT client                         |
| `.url`               | string  | empty string | 0..127, should start with mqtt:// or mqtts:// | mqtt - for unencrypted TCP connections<br/>mqtts - for encrypted TLS connections |
| `.username`          | string  | empty string | 0..127                                        | The username for broker authentication                       |
| `.password`          | string  | empty string | 0..127                                        | Password (not returned on GET - use password_len instead)    |
| `.client_id`         | string  | empty string | 0..63                                         | Unique identifier for the MQTT client. Must be unique per broker |
| `.skip_cn_check`     | boolean | false        |                                               | Skips server certificate Common Name validation             |
| `.publish.topic`     | string  | empty string | 0..127                                        | MQTT topic where messages will be published                 |
| `.publish.template`  | string  | empty string | 0..1023                                       | The published payload template                              |
| `.broker.certificate`| string  | null         |                                               | Custom broker certificate (PEM format)                     |
| `.client.certificate`| string  | null         |                                               | Client certificate for mutual TLS (PEM format)             |
| `.client.key`        | string  | null         |                                               | Client private key for mutual TLS (not returned on GET)    |
| `.client.key_password`| string | null         | 0..255                                        | Client key decryption password (not returned on GET)       |

!!! warning "Size Limit"
    The maximum size of the configuration JSON cannot exceed 8 kB.

## Example Configuration Response

```json
{
  "enable": true,
  "url": "mqtts://akenza.io",
  "username": "akenza",
  "client_id": "whatwatt",
  "skip_cn_check": false,
  "publish": {
    "topic": "test",
    "template": "{\n\t\"P_In\": ${1_7_0},\n\t\"P_Out\": ${2_7_0},\n\t\"E_In\": ${1_8_0},\n\t\"E_Out\": ${2_8_0},\n\t\"Meter\": {\n\t\t\"DateTime\": \"${meter.date_time}\"\n\t},\n\t\"Sys\": {\n\t\t\"Id\": \"${sys.id}\"\n\t}\n}"
  },
  "password_len": 0
}
```

## Configuration Methods

- **POST**: Replace the entire configuration
- **PUT**: Update configuration (existing fields preserved, including password)
- **GET**: Read current configuration (passwords show as length only)

To delete certificate fields, set them to `null` in JSON.

## Report Interval

The default MQTT report period is 30s, but if the meter sends reports less frequently, it will be longer. You can change this setting via WebUI in **System > Interval to Systems** section.
