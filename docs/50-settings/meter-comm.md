---
title: Meter Communication Settings
category: api-endpoints
tags:
- meter-communication
- serial-config
- dlms
- mbus
- p1
- protocol-setup
difficulty: advanced
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /api/v1/meter/settings
protocols:
- HTTP
- REST
- DLMS
- MBUS
- P1
related_concepts:
- meter protocols
- serial communication
- dlms encryption
- meter authentication
- protocol configuration
use_cases:
- meter setup
- protocol configuration
- encryption setup
- communication troubleshooting
real_device_tested: true
authentication: required when device password is set
methods:
- GET
- POST
- PUT
---


# Meter Communication Settings

## Document Context

- **Purpose**: Configure serial communication interface between device and smart meter
- **When to use**: For meter setup, protocol configuration, encryption/authentication setup, or communication troubleshooting
- **Prerequisites**: Knowledge of meter type and protocol; understanding of serial communication parameters
- **Related to**: Meter protocols (DLMS, DSMR, MBUS), serial interfaces, encryption setup
- **Validates against**: Real meter communication with Landis+Gyr and other meter types

## Key Facts

- **Endpoint**: `/api/v1/meter/settings`
- **Methods**: GET, POST, PUT
- **Authentication**: Required when device Web UI password is set
- **Supported protocols**: DLMS, DSMR, MBUS, KMP, MEP
- **Interface types**: P1, MBUS, TTL, MEP, UART, auto-detect
- **Auto-detection**: Automatic baudrate and protocol detection available
- **Encryption support**: DLMS encryption with 32-character hex keys
- **POST vs PUT**: POST replaces all settings, PUT updates only specified fields

## Endpoint details

Configure communication parameters with the connected meter, including serial port settings and physical layer configuration.

| Endpoint              | `api/v1/meter/settings` |
| --------------------- | ----------------------- |
| Method                | GET, POST, PUT          |
| Response content type | application/json        |

--8<-- "../_partials/auth-note.md"

## Configuration Fields

| Field                        | Type    | Default    | Range/Allowed values                                      | Description                                                                 |
| ---------------------------- | ------- | ---------- | --------------------------------------------------------- | --------------------------------------------------------------------------- |
| `.baudrate`                  | uint    | 115200     | 300..115200                                               | Data transfer rate over serial interface                                    |
| `.parity`                    | string  | none       | none, odd, even                                           | Parity control for serial transmission                                      |
| `.stop_bits`                 | string  | 1          | 1, 1.5, 2                                                | Number of stop bits in serial transmission                                  |
| `.buffer_size`               | uint8   | 64         | 1..128                                                    | Serial RX buffer size (bytes)                                               |
| `.method`                    | string  | Passive Push | Passive Push                                             | Data acquisition method                                                      |
| `.encryption`                | boolean | false      |                                                           | Enable data encryption at logical layer                                     |
| `.encryption_key`            | string  | empty      | 32 hexadecimal characters                                 | Data encryption key (GET hides the value; send 32 zeros to clear)           |
| `.authentication_key`        | string  | empty      | 32 hexadecimal characters                                 | Meter authorization key (GET hides the value; send 32 zeros to clear)       |
| `.tx_invert`                 | boolean | false      |                                                           | Reverse polarity of transmission data line                                  |
| `.rx_invert`                 | boolean | false      |                                                           | Reverse polarity of data receiving line                                     |
| `.auto_baudrate`             | boolean | true       |                                                           | Automatic serial port settings detection                                    |
| `.if_type`                   | string  | auto       | auto, p1, mbus, ttl, mep, irda, uart, p1_adapter, ttl_push | Physical interface type (auto-detect or manual)                              |
| `.protocol`                  | string  | auto       | auto, dsmr, hdlc, kmp, mep, mbus, mbtr                    | Logical protocol on the interface                                            |
| `.if_mode`                   | string  | auto       | auto, push, pull                                          | Interface I/O mode                                                           |
| `.conv_factor`               | real    | 1          | 0.001..1000                                              | Conversion coefficient for power/energy/current values                       |
| `.time_offset`               | int     | 0          | −2^31..2^31−1                                            | Meter time correction in seconds                                             |
| `.sync_time_offset_with_ntp` | boolean | false      |                                                           | Automatically adjust time offset based on NTP                                |
| `.scalers_set`               | string  | default    | default, custom, lge570                                   | Scaling scheme for meter values                                              |

## Example Request

=== "No auth"
    ```bash
    curl http://whatwatt-ABCDEF.local/api/v1/meter/settings
    ```

=== "With password"
    ```bash
    curl --anyauth -u ":PASSWORD" http://whatwatt-ABCDEF.local/api/v1/meter/settings
    ```

### Update semantics

- POST: Full replace. Fields not provided are reset to defaults (factory schema). Use when setting a complete configuration.
- PUT: Partial update. Only provided fields are changed; others remain unchanged. Use for incremental tweaks.

Examples:

```bash
# Partial update (PUT): only change interface type and protocol
curl --anyauth -u ":PASSWORD" -X PUT \
  -H "Content-Type: application/json" \
  -d '{"if_type":"p1","protocol":"dsmr"}' \
  http://whatwatt-ABCDEF.local/api/v1/meter/settings

# Full replace (POST): provide a complete configuration block
curl --anyauth -u ":PASSWORD" -X POST \
  -H "Content-Type: application/json" \
  -d '{
        "baudrate":115200,
        "parity":"none",
        "stop_bits":"1",
        "buffer_size":64,
        "method":"Passive Push",
        "encryption":false,
        "rx_invert":false,
        "tx_invert":false,
        "auto_baudrate":true,
        "if_type":"auto",
        "protocol":"auto",
        "if_mode":"auto",
        "conv_factor":1,
        "time_offset":0,
        "sync_time_offset_with_ntp":false,
        "scalers_set":"default"
      }' \
  http://whatwatt-ABCDEF.local/api/v1/meter/settings
```

## Example Response

```json
{
  "baudrate": 115200,
  "parity": "none",
  "stop_bits": "1",
  "buffer_size": 64,
  "method": "Passive Push",
  "encryption": false,
  "rx_invert": false,
  "tx_invert": false,
  "auto_baudrate": true,
  "if_type": "auto",
  "protocol": "auto",
  "if_mode": "auto",
  "conv_factor": 1,
  "time_offset": 0,
  "sync_time_offset_with_ntp": false,
  "scalers_set": "default"
}
```

## Configuration Examples

### Manual Serial Configuration

```json
{
  "auto_baudrate": false,
  "baudrate": 9600,
  "parity": "even",
  "stop_bits": "1",
  "if_type": "p1"
}
```

### Enable Encryption (DLMS/COSEM)

```json
{
  "encryption": true,
  "encryption_key": "0123456789ABCDEF0123456789ABCDEF"
}
```

### Time Synchronization

```json
{
  "time_offset": 3600,
  "sync_time_offset_with_ntp": true
}
```

### Custom Scaling

```json
{
  "scalers_set": "custom",
  "conv_factor": 1000
}
```

## Interface Types

| Type          | Description                                           |
|---------------|-------------------------------------------------------|
| `auto`        | Automatic detection of interface type                 |
| `p1`          | P1 port (DSMR)                                        |
| `mbus`        | M-Bus interface                                       |
| `ttl`         | TTL level serial interface                            |
| `mep`         | MEP (Meter Exchange Protocol)                         |
| `irda`        | Infrared optical interface                            |
| `uart`        | Generic UART                                          |
| `p1_adapter`  | External P1-to-UART adapter                           |
| `ttl_push`    | TTL interface in push mode (hardware-driven stream)   |

## Protocols

| Protocol | Notes                                 |
|----------|---------------------------------------|
| `auto`   | Auto-detect                            |
| `dsmr`   | DSMR P1                                |
| `hdlc`   | DLMS/COSEM HDLC framing                |
| `kmp`    | Kamstrup Meter Protocol                |
| `mep`    | MEP                                    |
| `mbus`   | M-Bus                                  |
| `mbtr`   | M-Bus transparent/raw                   |

## Interface Mode

| Mode   | Description                                   |
|--------|-----------------------------------------------|
| `auto` | Auto-select push/pull from interface/protocol |
| `push` | Device pushes frames; gateway listens         |
| `pull` | Gateway actively polls the meter              |

## Scaler Sets

| Set       | Description                                |
|-----------|--------------------------------------------|
| `default` | Automatic scaling detection                |
| `lge570`  | Predefined scales for Landis+Gyr E570     |
| `custom`  | User-defined scaling (see custom scalers)  |

!!! warning "Encryption Keys"
    - Keys are not returned in GET responses (they are hidden/masked)
    - Use 32 hexadecimal characters (128-bit keys)
    - To clear a key via POST/PUT, send 32 zeros (`00000000000000000000000000000000`)

!!! note "Auto-Detection"
    - `auto_baudrate` enables automatic detection of serial parameters
    - `if_type: auto` enables automatic interface type detection
    - Manual settings override auto-detection when disabled
