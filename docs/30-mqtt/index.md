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

- **Purpose**: Comprehensive guide for configuring whatwatt Go MQTT client to publish energy data to MQTT brokers
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
    whatwatt Go will only publish values if a meter is connected.

## Configuration Overview

- Endpoint: `/api/v1/mqtt/settings` (GET, POST, PUT)
- Response content type: `application/json`
- Full details and field reference: see MQTT Client page.

See: `30-mqtt/mqtt-client.md` for complete configuration reference and examples.

--8<-- "../_partials/auth-note.md"

## Payload Templates

- Templates define the payload content published to MQTT using predefined variables.
- See: `30-mqtt/template.md` for the full variable list and examples.

## Report Interval

The default MQTT report period is 30s. If the meter reports less frequently, the effective period stretches. You can change this setting via WebUI in **System > Interval to Systems**.
