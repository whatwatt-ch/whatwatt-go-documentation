---
title: MQTT Template
category: concepts
tags:
- template
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# MQTT Template

## Document Context

- **Purpose**: Explains MQTT payload template system for customizing published message format with embedded device and meter variables
- **When to use**: Configuring MQTT message payloads, integrating with specific IoT platforms, customizing data formats for downstream systems
- **Prerequisites**: Basic JSON syntax, understanding of MQTT message publishing, familiarity with energy meter data fields (OBIS codes)
- **Related to**: MQTT client configuration, local variables endpoint, energy measurements, system information fields
- **Validates against**: Template variable resolution with real meter data and system information

## Key Facts

- **Template syntax**: ${variable_name} for embedding predefined variables
- **Message format**: Text-based (typically JSON) with variable substitution
- **Variable types**: Measurement variables (numeric) and system variables (text/numeric)
- **Variable resolution**: Unresolved variables remain as literal ${name} strings
- **Data validation**: Some variables may be null/empty if not provided by meter
- **Output format**: Valid JSON after variable substitution
- **Predefined variables**: Cannot define custom variables, only use system-provided ones
- **Error handling**: Template errors result in literal variable strings in output

## Template Description

The message published by the client is defined using a template. The message format can be anything but always text.

You can embed variables in the template, which can be both measurement and system variables. A variable in a template is embedded in a section starting with a dollar sign, followed by an opening curly brace, the variable name, and a closing curly brace: **`${variable_name}`**

The available variables are predefined - you cannot define your own at this time.

!!! warning "Variable Resolution"
    If a variable appears in the template that is not resolved, then the variable will not be replaced and the entire `${some_undefined_variable}` string will be in the output message. Be careful when integrating with your system - some variables may be `null` (numeric) or empty string (text) if not sent by the meter.

## Example Template

```json
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

!!! note
    This is not valid JSON until all variables are resolved. Note that some variables are always numeric (written as text) and some are text - in JSON payload you need to enclose text variables in quotes.

## Example Generated Message

After variable substitution, the template generates a valid JSON message:

```json
{
  "sys_id": "A842E39F8124",
  "meter_id": "636192",
  "time": 1725281386,
  "tariff": 0,
  "power_in": 1.1,
  "power_out": 0,
  "energy_in": 123.4,
  "energy_out": 0
}
```

## Available Variables

The first column Name usually refers to short OBIS form part C.D.E. Keep in mind that the meter does not send all fields. The value returned for a network interface depends on which one is connected.

### Energy Variables

| Variable           | Type   | Unit  | Description                                                  |
| ------------------ | ------ | ----- | ------------------------------------------------------------ |
| `1_8_0`            | double | kWh   | Positive active energy (A+) total                           |
| `energy.in`        | double | kWh   | Positive active energy (A+) total                           |
| `1_8_1`            | double | kWh   | Positive active energy (A+) in tariff T1                    |
| `1_8_2`            | double | kWh   | Positive active energy (A+) in tariff T2                    |
| `2_8_0`            | double | kWh   | Negative active energy (A-) total                           |
| `energy.out`       | double | kWh   | Negative active energy (A-) total                           |
| `2_8_1`            | double | kWh   | Negative active energy (A-) in tariff T1                    |
| `2_8_2`            | double | kWh   | Negative active energy (A-) in tariff T2                    |

### Power Variables

| Variable           | Type   | Unit  | Description                                                  |
| ------------------ | ------ | ----- | ------------------------------------------------------------ |
| `1_7_0`            | double | kW    | Positive active instantaneous power (A+)                    |
| `power.in`         | double | kW    | Positive active instantaneous power (A+)                    |
| `21_7_0`           | double | kW    | Positive active instantaneous power (A+) in phase L1        |
| `41_7_0`           | double | kW    | Positive active instantaneous power (A+) in phase L2        |
| `61_7_0`           | double | kW    | Positive active instantaneous power (A+) in phase L3        |
| `2_7_0`            | double | kW    | Negative active instantaneous power (A-)                    |
| `power.out`        | double | kW    | Negative active instantaneous power (A-)                    |
| `22_7_0`           | double | kW    | Negative active instantaneous power (A-) in phase L1        |
| `42_7_0`           | double | kW    | Negative active instantaneous power (A-) in phase L2        |
| `62_7_0`           | double | kW    | Negative active instantaneous power (A-) in phase L3        |

### Reactive Power & Energy

| Variable           | Type   | Unit   | Description                                                 |
| ------------------ | ------ | ------ | ----------------------------------------------------------- |
| `3_7_0`            | double | kvar   | Positive reactive instantaneous power (Q+)                 |
| `4_7_0`            | double | kvar   | Negative reactive instantaneous power (Q-)                 |
| `3_8_0`            | double | kvarh  | Positive reactive energy (Q+) total                        |
| `4_8_0`            | double | kvarh  | Negative reactive energy (Q-) total                        |
| `5_8_0`            | double | kvarh  | Imported inductive reactive energy Q1 total                |
| `6_8_0`            | double | kvarh  | Imported capacitive reactive energy Q2 total               |
| `7_8_0`            | double | kvarh  | Exported inductive reactive energy Q3 total                |
| `8_8_0`            | double | kvarh  | Exported capacitive reactive energy Q4 total               |

### Voltage & Current

| Variable           | Type   | Unit  | Description                                                  |
| ------------------ | ------ | ----- | ------------------------------------------------------------ |
| `32_7_0`           | double | V     | Instantaneous voltage (U) in phase L1                       |
| `52_7_0`           | double | V     | Instantaneous voltage (U) in phase L2                       |
| `72_7_0`           | double | V     | Instantaneous voltage (U) in phase L3                       |
| `31_7_0`           | double | A     | Instantaneous current (I) in phase L1                       |
| `51_7_0`           | double | A     | Instantaneous current (I) in phase L2                       |
| `71_7_0`           | double | A     | Instantaneous current (I) in phase L3                       |
| `s31_7_0`          | double | A     | Signed instantaneous current (I) in phase L1                |
| `s51_7_0`          | double | A     | Signed instantaneous current (I) in phase L2                |
| `s71_7_0`          | double | A     | Signed instantaneous current (I) in phase L3                |

### System & Meter Variables

| Variable           | Type   | Unit     | Description                                                 |
| ------------------ | ------ | -------- | ----------------------------------------------------------- |
| `timestamp`        | uint   |          | UTC UNIX timestamp                                          |
| `tariff`           | uint   |          | Current tariff (1, 2)                                      |
| `conv_factor`      | double |          | Conversion coefficient for power/energy/current values     |
| `13_7_0`           | double |          | Instantaneous power factor                                  |
| `meter.date_time`  | string | ISO8601  | Report date time in local time                             |
| `meter.id`         | string |          | Meter ID                                                    |
| `meter.type`       | string |          | Meter type                                                  |
| `meter.vendor`     | string |          | Meter vendor                                                |
| `meter.model`      | string |          | Model of meter                                              |
| `meter.interface`  | string |          | Physical interface (P1, TTL, MBUS, MEP)                   |
| `meter.protocol`   | string |          | Protocol (DSMR, DLMS, KMP, MEP)                           |
| `meter.protocol_ver`| string|          | Meter protocol version                                      |
| `meter.status`     | string |          | Connection status (NOT CONNECTED, NO DATA, OK, etc.)      |
| `sys.name`         | string |          | Name of device (settable via WebUI)                       |
| `sys.id`           | string |          | whatwatt Go system identifier                              |
| `sys.firmware`     | string |          | Firmware version                                            |
| `sys.date_time`    | string | ISO8601  | System local time                                           |

### Network Interface Variables

| Variable           | Type   | Unit  | Description                                                  |
| ------------------ | ------ | ----- | ------------------------------------------------------------ |
| `wifi.mode`        | string |       | Wi-Fi operation mode (off, sta, ap, apsta, nan)            |
| `wifi.sta.status`  | string |       | Connection status (disabled, disconnected, error, ok)      |
| `wifi.sta.ssid`    | string |       | Name of connected Wi-Fi network                             |
| `wifi.sta.rssi`    | int    | dBm   | Wi-Fi received signal strength indication                   |
| `wifi.sta.ip`      | string | IPv4  | IPv4 address assigned to Wi-Fi interface                   |
| `eth.state`        | string |       | Status of Ethernet (up, down)                              |
| `eth.ip`           | string | IPv4  | IPv4 address assigned to Ethernet interface                |

### Hardware Variables

| Variable              | Type   | Unit  | Description                                              |
| --------------------- | ------ | ----- | -------------------------------------------------------- |
| `plug.interface`      | string |       | Physical interface connected (NONE, P1, TTL, MBUS, MEP) |
| `plug.voltage.usb`    | double | V     | USB voltage                                              |
| `plug.voltage.p1`     | double | V     | P1 voltage                                               |
| `plug.voltage.mbus`   | double | V     | M-Bus voltage                                            |
