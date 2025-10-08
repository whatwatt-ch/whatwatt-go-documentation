---
title: Provision Payload
category: concepts
tags:
- provision_payload
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Provision Payload

## Document Context

- **Purpose**: Guide for configuring WhatWatt Go device with MQTT TLS settings via REST API using JSON payload with embedded certificates
- **When to use**: When deploying secure MQTT configuration to WhatWatt Go devices, setting up TLS client authentication, configuring device connectivity
- **Prerequisites**: Generated certificates (CA, client cert, client key), device IP address, understanding of JSON format and REST API
- **Related to**: Certificate generation (tls-ca-ecc.md), MQTT setup (index.md), TLS configuration (tls-conf.md)
- **Validates against**: WhatWatt Go REST API v1, 8kB payload limit, PEM certificate format requirements

## Key Facts

- **API endpoint**: `/api/v1/mqtt/settings` - Device MQTT configuration endpoint
- **Method**: POST with JSON payload - Upload configuration, GET - Retrieve current settings
- **Payload limit**: ≤ 8 kB - Total JSON size including certificates
- **Certificate format**: PEM with escaped newlines (\n) in JSON strings
- **Security**: Private keys not returned in GET responses, immediate connection attempt after configuration

Configure the WhatWatt Go device with MQTT TLS settings via REST API.

## Sample Configuration File

Create a file `mqtt.json` with the complete MQTT configuration (≤ 8 kB):

```json
{
  "enable": true,
  "url": "mqtts://192.168.99.186:8883",
  "skip_cn_check": true,
  "client_id": "whatwatt-001",
  "publish": {
    "topic": "lab/energy/whatwatt-001",
    "template": "{ \"P_In\": ${1_7_0}, \"P_Out\": ${2_7_0} }"
  },
  "broker": {
    "certificate": "-----BEGIN CERTIFICATE-----\nMIIBXTCCAQOgAwIBAgIJAKZ...ca-cert-content...vQ==\n-----END CERTIFICATE-----\n"
  },
  "client": {
    "certificate": "-----BEGIN CERTIFICATE-----\nMIIBYDCCAQagAwIBAgIJAL...client-cert-content...Xw==\n-----END CERTIFICATE-----\n",
    "key": "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEII...private-key-content...oUQDQgAE...\n-----END EC PRIVATE KEY-----\n"
  }
}
```

## Certificate Preparation

Convert certificate files to JSON format:

```bash
# Method 1: Manual copy-paste with proper escaping
cat ca.crt
cat whatwatt.crt
cat whatwatt.key

# Method 2: Automatic JSON escaping
echo '"'$(cat ca.crt | sed 's/$/\\n/' | tr -d '\n')'"'
echo '"'$(cat whatwatt.crt | sed 's/$/\\n/' | tr -d '\n')'"'
echo '"'$(cat whatwatt.key | sed 's/$/\\n/' | tr -d '\n')'"'
```

!!! warning "Certificate Format"
    - Certificates must be in PEM format
    - Newlines must be escaped as `\n` in JSON
    - Keep the `-----BEGIN` and `-----END` lines
    - Ensure no extra spaces or characters

## Upload Configuration

Upload the configuration to the device:

```bash
curl -X POST http://192.168.99.176/api/v1/mqtt/settings \
  -H "Content-Type: application/json" \
  --data-binary @mqtt.json
```

## Configuration Fields Explained

| Field                  | Value                              | Description                           |
|------------------------|------------------------------------|---------------------------------------|
| `enable`               | `true`                            | Enable MQTT client                    |
| `url`                  | `mqtts://IP:8883`                 | Secure MQTT broker URL               |
| `skip_cn_check`        | `true`                            | Skip hostname verification            |
| `client_id`            | `whatwatt-001`                    | Unique client identifier              |
| `publish.topic`        | `lab/energy/whatwatt-001`         | MQTT topic for published data        |
| `publish.template`     | JSON with variables               | Message payload template              |
| `broker.certificate`   | CA certificate (PEM)              | Validates broker certificate          |
| `client.certificate`   | Client certificate (PEM)          | Device authentication                 |
| `client.key`           | Client private key (PEM)          | Device TLS encryption                 |

## Verify Configuration

Check if the configuration was applied successfully:

```bash
curl http://192.168.99.176/api/v1/mqtt/settings
```

The response should show:

```json
{
  "enable": true,
  "url": "mqtts://192.168.99.186:8883",
  "skip_cn_check": true,
  "client_id": "whatwatt-001",
  "publish": {
    "topic": "lab/energy/whatwatt-001",
    "template": "{ \"P_In\": ${1_7_0}, \"P_Out\": ${2_7_0} }"
  },
  "password_len": 0
}
```

!!! note "Security"
    - Private keys are not returned in GET responses
    - Use `password_len` and similar fields to verify if secrets are set
    - The device will attempt to connect immediately after configuration
