---
title: MQTT Client Configuration
category: concepts
tags:
- mqtt
- configuration
- client
last_verified: '2025-11-26'
---

# MQTT Client Configuration

The device can connect to an MQTT broker using the built‑in client. Both unencrypted (`mqtt://`) and TLS encrypted (`mqtts://`) connections are supported.

!!! note "Publish Condition"
    The device publishes measurement values only when a meter is connected.

## Configuration Endpoint

| Endpoint              | `api/v1/mqtt/settings` |
| --------------------- | ---------------------- |
| Method                | GET, POST, PUT         |
| Response content type | application/json       |

## Settings Object Fields

| Field                | Type    | Default      | Range                                         | Remarks |
| -------------------- | ------- | ------------ | --------------------------------------------- | ------- |
| `.enable`            | boolean | false        |                                               | Enables or disables the MQTT client. |
| `.url`               | string  | empty string | 0..127, starts with `mqtt://` or `mqtts://`   | `mqtt` – not encrypted TCP; `mqtts` – encrypted TLS. |
| `.username`          | string  | empty string | 0..127                                        | Unique client username. |
| `.password`          | string  | empty string | 0..127                                        | Not returned on GET; instead `password_len` shows length (0 = not set). |
| `.client_id`         | string  | empty string | 0..63                                         | Must be unique per broker; duplicate IDs cause prior session disconnect. |
| `.skip_cn_check`     | boolean | false        |                                               | Skips certificate Common Name validation. |
| `.publish.topic`     | string  | empty string | 0..127                                        | Target topic for published messages. |
| `.publish.template`  | string  | empty string | 0..1023                                       | Payload template (text; often JSON). |
| `.broker.certificate`| string  | null         |                                               | Broker CA/server certificate in PEM (optional). |
| `.client.certificate`| string  | null         |                                               | Client certificate in PEM (for mutual TLS; requires `.client.key`). |
| `.client.key`        | string  | null         |                                               | Client private key (PEM). Not returned on GET; `key_len` reports length. |
| `.client.key_password` | string | null        | 0..255                                        | Password for encrypted private key; not returned on GET (`key_password_len`). |

!!! note "Payload Size Limit"
    POST/PUT JSON maximum size: 8 kB.

## Example Response (GET)

```json
{
  "enable": false,
  "url": "mqtts://broker.example.com",
  "username": "demo",
  "client_id": "device123",
  "skip_cn_check": false,
  "publish": {
    "topic": "test",
    "template": "{\n  \"P_In\": ${1_7_0},\n  \"P_Out\": ${2_7_0},\n  \"E_In\": ${1_8_0},\n  \"E_Out\": ${2_8_0},\n  \"Meter\": {\n    \"DateTime\": \"${meter.date_time}\"\n  },\n  \"Sys\": {\n    \"Id\": \"${sys.id}\"\n  }\n}"
  },
  "password_len": 0
}
```

## Updating Configuration

- POST full object to replace entire configuration.
- PUT partial object to update specific fields (existing secret values retained).
- Set any certificate/key/password field to `null` to delete it.
- Reporting period (default 30 s) stretches if meter reports less frequently; adjustable in **System > Interval to Systems**.

## Template & Variables

See [MQTT Template](template.md) for the full variable list, examples, and guidance on quoting and substitution.

!!! note "Tips"
    - Treat missing fields as unavailable; don’t assume zero means present.
    - Quote text variables, don’t quote numeric variables in templates.
    - Shortly after power‑on some values may be `null` or empty until available.
