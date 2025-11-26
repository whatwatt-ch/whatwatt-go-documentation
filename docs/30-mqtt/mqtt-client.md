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

## Template Description

Payload templates are text (commonly JSON) with embedded predefined variables using `${variable_name}` syntax.

!!! warning "Unresolved Variables"
    Unresolved variables remain literally as `${name}`. Shortly after power‑on some values may be `null` (numeric) or empty (text) until available.

### Example Template (Not Yet Valid JSON)

```text
{
  "P_In": ${1_7_0},
  "P_Out": ${2_7_0},
  "E_In": ${1_8_0},
  "E_Out": ${2_8_0},
  "Meter": {
    "DateTime": "${meter.date_time}"
  },
  "Sys": {
    "Id": "${sys.id}"
  }
}
```

!!! note "Validity"
    JSON becomes valid only after substitution; quote text variables, do not quote numeric variables.

### Example Generated JSON

```json
{
  "P_In": 0.014,
  "P_Out": 0,
  "E_In": 200.934,
  "E_Out": 8.965,
  "Meter": {
    "DateTime": "2025-11-17T15:52:50Z"
  },
  "Sys": {
    "Id": "ECC9FF5C7F14"
  }
}
```

## Available Variables (Selection)

| Name                | Type   | Unit   | Description |
| ------------------- | ------ | ------ | ----------- |
| `1_8_0`             | double | kWh    | Positive active energy total |
| `2_8_0`             | double | kWh    | Negative active energy total |
| `1_7_0`             | double | kW     | Positive active instantaneous power total |
| `2_7_0`             | double | kW     | Negative active instantaneous power total |
| `21_7_0`            | double | kW     | Positive active instantaneous power L1 |
| `41_7_0`            | double | kW     | Positive active instantaneous power L2 |
| `61_7_0`            | double | kW     | Positive active instantaneous power L3 |
| `3_7_0`             | double | kvar   | Positive reactive instantaneous power total |
| `4_7_0`             | double | kvar   | Negative reactive instantaneous power total |
| `9_7_0`             | double | kVA    | Apparent instantaneous power total |
| `31_7_0`            | double | A      | Instantaneous current L1 |
| `51_7_0`            | double | A      | Instantaneous current L2 |
| `71_7_0`            | double | A      | Instantaneous current L3 |
| `meter.date_time`   | string | ISO8601| Report date/time (local) |
| `meter.date_time_utc` | string | ISO8601| Report date/time (UTC) |
| `sys.date_time`     | string | ISO8601| System date/time (local) |
| `sys.date_time_utc` | string | ISO8601| System date/time (UTC) |
| `tariff`            | uint   |        | Current tariff (may be absent or 0 if unknown) |
| `timestamp`         | uint   |        | UNIX timestamp (UTC) |
| `conv_factor`       | double |        | Multiplicative conversion factor |

See the full MQTT Template page for the complete variable list.

## Defensive Parsing Tips

- Treat missing fields as unavailable; do not assume zero means present.
- Always parse numbers with fallback (e.g. default to 0 only for calculations, not logic).
- Consider logging unresolved variables during integration testing.

## Next Steps

- Secure connection setup: see Secure MQTT section.
- Define custom topic naming: ensure uniqueness per device.
- Use retained messages sparingly (device does not publish retained by default).
