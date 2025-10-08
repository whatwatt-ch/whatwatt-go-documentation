---
title: Local Variable Reading
category: api-endpoints
tags:
- variables
- mqtt-template
- testing
- debugging
- local-access
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /api/v1/variables
protocols:
- HTTP
- REST
related_concepts:
- mqtt templates
- variable testing
- template debugging
- local development
use_cases:
- mqtt template testing
- variable debugging
- integration planning
- development workflow
real_device_tested: true
authentication: required when device password is set
---

# Local Variable Reading

## Document Context

- **Purpose**: Access all MQTT template variables for testing and development purposes
- **When to use**: When developing MQTT templates, debugging variable availability, or planning integrations
- **Prerequisites**: Basic understanding of MQTT templates and variable substitution
- **Related to**: MQTT template configuration, variable debugging, integration planning
- **Validates against**: Real device variable data

## Key Facts

- **Endpoint**: `/api/v1/variables`
- **Method**: GET only
- **Authentication**: Required when device Web UI password is set
- **Response format**: JSON array of name-value objects
- **Typical response time**: <100ms
- **Variable types**: System info, energy values, meter data, network status
- **Null handling**: Variables show as "null" string when not available

## Endpoint Details

You can read all available MQTT template variables locally via REST API to test and debug your MQTT templates.

| Endpoint              | `api/v1/variables` |
| --------------------- | ------------------ |
| Method                | GET                |
| Response content type | application/json   |

--8<-- "../_partials/auth-note.md"

## Example Request

=== "No auth"

  ```bash
  curl http://whatwatt-ABCDEF.local/api/v1/variables
  ```

=== "With password"

  ```bash
  curl --anyauth -u ":PASSWORD" http://whatwatt-ABCDEF.local/api/v1/variables
  ```

## Example Response

The response returns an array of objects, each containing a single variable name-value pair:

```json
[
  { "sys.name": "" },
  { "sys.id": "A842E39F8124" },
  { "sys.firmware": "1.2.15" },
  { "sys.date_time": "2025-02-20T17:49:45Z" },
  { "1_8_0": "24.087" },
  { "energy.in": "24.087" },
  { "1_8_1": "null" },
  { "1_8_2": "null" },
  { "2_8_0": "0.004" },
  { "energy.out": "0.004" },
  { "2_8_1": "null" },
  { "2_8_2": "null" },
  { "3_8_0": "10.505" },
  { "3_8_1": "null" },
  { "3_8_2": "null" },
  { "4_8_0": "15.385" },
  { "4_8_1": "null" },
  { "4_8_2": "null" },
  { "1_7_0": "0.006" },
  { "power.in": "0.006" },
  { "21_7_0": "0.006" },
  { "41_7_0": "0" },
  { "61_7_0": "0" },
  { "2_7_0": "0" },
  { "power.out": "0" },
  { "22_7_0": "0" },
  { "42_7_0": "0" },
  { "62_7_0": "0" },
  { "31_7_0": "0.06" },
  { "51_7_0": "0" },
  { "71_7_0": "0" },
  { "32_7_0": "233" },
  { "52_7_0": "0" },
  { "72_7_0": "0" },
  { "tariff": "2" },
  { "conv_factor": "1" },
  { "timestamp": "1735542122" },
  { "meter.date_time": "2024-12-30T08:02:02Z" },
  { "meter.id": "" },
  { "meter.type": "LGZ1030662444349" },
  { "meter.vendor": "Landis+Gyr" },
  { "meter.model": "" },
  { "meter.interface": "MBUS" },
  { "meter.protocol": "DLMS" },
  { "meter.protocol_ver": "" },
  { "meter.status": "OK" },
  { "plug.interface": "MBUS" },
  { "plug.voltage.usb": "5.272" },
  { "plug.voltage.p1": "2.844" },
  { "plug.voltage.mbus": "10.952" },
  { "wifi.mode": "sta" },
  { "wifi.sta.status": "ok" },
  { "wifi.sta.ssid": "sjj" },
  { "wifi.sta.bssid": "DC15C84FBAB6" },
  { "wifi.sta.rssi": "-30" },
  { "wifi.sta.channel": "13" },
  { "wifi.sta.mac": "A842E39F8124" },
  { "wifi.sta.ip": "192.168.99.176" },
  { "wifi.sta.mask": "255.255.255.0" },
  { "wifi.sta.gw": "192.168.99.1" },
  { "wifi.sta.dns": "0.0.0.0" }
]
```

## Usage

This endpoint is useful for:

- **Template testing**: Verify which variables are available and their current values
- **Debugging**: Check if specific variables are being read from the meter
- **Integration planning**: See all available data points before designing your MQTT payload

!!! note "Variable Values"
    - Variables that are not available show as `"null"` (as string)
    - Numeric values are returned as strings
    - Some variables may be empty or null if the meter doesn't provide that data
    - Variable availability depends on meter type and connection method
