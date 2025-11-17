---
title: Custom Meter Scalers
category: concepts
tags:
- scalers_custom
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Custom Meter Scalers

## Document Context

- **Purpose**: Custom scaler configuration API for overriding DLMS meter scaling factors using OBIS codes with wildcard support
- **When to use**: Normalizing units across different meters, correcting meter scaling issues, standardizing data for analysis
- **Prerequisites**: DLMS meter setup, OBIS code understanding, knowledge of COSEM Class 3 objects and meter data units
- **Related to**: [Current scalers](scalers-current.md), [Meter communication](meter-comm.md), device settings configuration
- **Validates against**: COSEM Class 3 object requirements, OBIS code validation, scaler range limits (-6 to +6)

## Key Facts

- **Endpoint**: `/api/v1/meter/scalers/custom` - Configure custom scaling factors for meter data
- **Methods**: GET (read), POST (set) - JSON array of OBIS/scaler pairs
- **OBIS format**: C.D.E notation with wildcard support (255 for all E values)
- **Scaler range**: -6 to +6 power-of-ten multipliers for unit conversion
- **Priority**: Custom scalers override device-detected scalers when configured

--8<-- "../_partials/auth-note.md"

!!! note "DLMS Only"
    These settings operate exclusively for messages in the DLMS format.

!!! info "COSEM Class 3"
    Scale factors apply only to COSEM Class 3 objects.

!!! note "Alternative Method"
    Custom scalers can also be configured from the device's WebUI.

## Endpoint Details

This endpoint allows for the setting of individual scaling values for specific register values transmitted by the meter. This API uses a shortened convention of logical name/OBIS, which is in the format C.D.E.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/meter/scalers/custom` |
| **Methods** | `GET`, `POST` |
| **Response Content Type** | `application/json` |

## Configuration Fields

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `obis` | string | 0..254.0..254.0..255 | C.D.E part of the logical OBIS code (e.g., "1.8.0"). Use "255" as wildcard for all E values (e.g., "1.8.255" applies to all tariffs) |
| `scaler` | int | -6..6 | Scaler value expressed as power of ten (10^scaler) |

### OBIS Wildcard Usage

| OBIS Pattern | Effect | Example |
|--------------|--------|---------|
| `1.8.0` | Apply to specific register | Only positive active energy total |
| `1.8.255` | Apply to all E values | All positive active energy registers (T0, T1, T2, etc.) |
| `32.7.255` | Apply to all voltage phases | All voltage measurements |

### Scaler Value Effects

| Scaler | Multiplier | Use Case | Example |
|--------|------------|----------|---------|
| `-6` | 0.000001 | Micro units | µA, µV |
| `-3` | 0.001 | Milli units | mA, mV |
| `-2` | 0.01 | Centi units | Currency (cents) |
| `-1` | 0.1 | Deci units | Decimal precision |
| `0` | 1 | No scaling | Default |
| `1` | 10 | Deka units | - |
| `2` | 100 | Hecto units | - |
| `3` | 1000 | Kilo units | kW, kWh |
| `6` | 1000000 | Mega units | MW, MWh |

## Examples

### Read Current Custom Scalers

```bash
curl -s http://192.168.1.100/api/v1/meter/scalers/custom
```

**Response:**

```json
[
  {
    "obis": "1.7.0",
    "scaler": -1
  },
  {
    "obis": "2.7.0",
    "scaler": -1
  }
]
```

### Set Custom Scalers

```bash
curl -X POST -H "Content-Type: application/json" \
     -d '[
       {
         "obis": "1.7.0",
         "scaler": -2
       },
       {
         "obis": "1.8.255",
         "scaler": 3
       }
     ]' \
     http://192.168.1.100/api/v1/meter/scalers/custom
```

### Common Configuration Examples

#### Scale All Energy Values to kWh

```json
[
  {
    "obis": "1.8.255",
    "scaler": 3
  },
  {
    "obis": "2.8.255",
    "scaler": 3
  }
]
```

#### Scale All Current Values to Amperes

```json
[
  {
    "obis": "31.7.0",
    "scaler": -2
  },
  {
    "obis": "51.7.0",
    "scaler": -2
  },
  {
    "obis": "71.7.0",
    "scaler": -2
  }
]
```

#### Scale Power Values to kW

```json
[
  {
    "obis": "1.7.0",
    "scaler": 3
  },
  {
    "obis": "2.7.0",
    "scaler": 3
  }
]
```

## Practical Use Cases

### Unit Conversion

- Convert Wh to kWh by setting scaler to `3`
- Convert mA to A by setting scaler to `-3`
- Convert centivolts to volts by setting scaler to `-2`

### Meter Compatibility

- Some meters report values in different base units
- Custom scalers normalize values across different meter types
- Ensures consistent units in reports and MQTT messages

### Data Processing

- Pre-scale values for specific applications
- Reduce computation load in client applications
- Standardize units for data analysis

## Important Notes

!!! warning "Validation Required"
    - Only OBIS codes belonging to COSEM class 3 should be defined
    - Invalid OBIS codes will be rejected
    - Scaler values outside -6..6 range are not permitted

!!! tip "Best Practice"
    - Test scalers with known meter values before production use
    - Document custom scaler configurations for maintenance
    - Use wildcards (255) carefully to avoid unintended scaling

!!! info "Priority"
    Custom scalers override device-detected scalers when both are present.
