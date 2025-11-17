---
title: Reading Current Scaler Values
category: concepts
tags:
- scalers_current
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Reading Current Scaler Values

## Document Context

- **Purpose**: API for reading current scaler values applied to DLMS meter registers using OBIS codes for data scaling and unit conversion
- **When to use**: Understanding meter data scaling, troubleshooting value discrepancies, verifying COSEM Class 3 object scaling
- **Prerequisites**: DLMS meter communication, OBIS code knowledge, understanding of COSEM Class 3 objects and power-of-ten scaling
- **Related to**: [Custom scalers](scalers-custom.md), [Meter communication](meter-comm.md), data reporting endpoints
- **Validates against**: DLMS/COSEM standards, OBIS code specifications, meter scaling behavior in COSEM Class 3

## Key Facts

- **Endpoint**: `/api/v1/meter/scalers/current` - Reads current scaling factors for OBIS codes
- **Method**: GET - Returns JSON array of OBIS codes with their active scalers
- **Compatibility**: DLMS meters only, COSEM Class 3 objects, available since firmware 1.2.15
- **Scaling**: Power-of-ten multipliers (-3 to +3 typical range)
- **OBIS format**: Shortened C.D.E notation for recognized meter registers

--8<-- "../_partials/auth-note.md"

!!! note "DLMS Only"
    Currently, reading current scaler values is only available for meters that exchange data in DLMS format.

!!! info "COSEM Class 3"
    Scale factors apply only to COSEM Class 3 objects.

## How Scalers Work

The present value is the value that has been determined by the device itself at the detection stage, covered/overridden by a set of scalers selected by the `scalers_set` (note that the `scalers_set` does not have to cover all values).

## Endpoint Details

This endpoint allows you to read individual scale values for specific register values that the meter transmits. This API uses a shortened convention of logical name/OBIS, which is in the format C.D.E.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/meter/scalers/current` |
| **Method** | `GET` |
| **Response Content Type** | `application/json` |
| **Available Since** | Firmware version 1.2.15 |

## Response Format

The endpoint returns an array of OBIS codes with their current scaler values.

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `obis` | string | Shorthand representation of the OBIS notation (C.D.E format). Only OBIS codes recognized by the device and belonging to COSEM class 3 are included |
| `scaler` | int | Currently applied scaling factor expressed as power of ten (10^scaler) |

### Scaler Value Interpretation

| Scaler Value | Multiplier | Effect | Example |
|--------------|------------|--------|---------|
| `-3` | 0.001 | Divide by 1000 | 1000 → 1.0 |
| `-2` | 0.01 | Divide by 100 | 150 → 1.50 |
| `-1` | 0.1 | Divide by 10 | 25 → 2.5 |
| `0` | 1 | No scaling | 100 → 100 |
| `1` | 10 | Multiply by 10 | 5 → 50 |
| `2` | 100 | Multiply by 100 | 3 → 300 |
| `3` | 1000 | Multiply by 1000 | 2 → 2000 |

## Example Request

```bash
curl -s http://192.168.1.100/api/v1/meter/scalers/current
```

## Example Response

```json
[
  {
    "obis": "1.8.0",
    "scaler": 0
  },
  {
    "obis": "2.8.0",
    "scaler": 0
  },
  {
    "obis": "3.8.0",
    "scaler": 0
  },
  {
    "obis": "4.8.0",
    "scaler": 0
  },
  {
    "obis": "1.7.0",
    "scaler": 0
  },
  {
    "obis": "2.7.0",
    "scaler": 0
  },
  {
    "obis": "32.7.0",
    "scaler": 0
  },
  {
    "obis": "52.7.0",
    "scaler": 0
  },
  {
    "obis": "72.7.0",
    "scaler": 0
  },
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

## Common OBIS Codes

### Energy Values (typically scaler: 0)

- `1.8.0` - Positive active energy total
- `2.8.0` - Negative active energy total
- `3.8.0` - Positive reactive energy total
- `4.8.0` - Negative reactive energy total

### Power Values (typically scaler: 0)

- `1.7.0` - Positive active instantaneous power
- `2.7.0` - Negative active instantaneous power

### Voltage Values (typically scaler: 0)

- `32.7.0` - Voltage L1
- `52.7.0` - Voltage L2
- `72.7.0` - Voltage L3

### Current Values (typically scaler: -2)

- `31.7.0` - Current L1 (often scaled by 0.01)
- `51.7.0` - Current L2 (often scaled by 0.01)
- `71.7.0` - Current L3 (often scaled by 0.01)

Use this endpoint to understand how raw meter values are being scaled before they appear in the final report data.
