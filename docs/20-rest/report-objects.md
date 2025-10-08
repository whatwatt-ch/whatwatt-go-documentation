---
title: Report Objects
category: concepts
tags:
- report_objects
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Report Objects

## Document Context

- **Purpose**: Documents raw DLMS/COSEM objects endpoint for accessing meter-native OBIS codes and understanding available measurements
- **When to use**: Debugging meter communication, mapping custom scalers, understanding meter capabilities, developing OBIS code parsers
- **Prerequisites**: Knowledge of DLMS/COSEM protocol, OBIS code structure, energy meter communication standards
- **Related to**: Report polling endpoint, meter communication settings, OBIS reference documentation, custom scalers
- **Validates against**: Live OBIS object lists from Swiss smart meters via 192.168.99.114

## Key Facts

- **Endpoint**: /api/v1/report/objects
- **Methods**: GET only
- **Authentication**: HTTP Authentication (when device protection enabled)
- **Response format**: JSON with OBIS logical names and DLMS classes
- **Data source**: Direct from meter COSEM interface (not processed by device)
- **Use cases**: Diagnostics, custom parsing, meter capability discovery
- **OBIS classes**: Class 1 (data), Class 3 (register), Class 40 (push objects)
- **Meter dependency**: Requires active meter connection and communication

## Endpoint Details

This endpoint exposes raw DLMS/COSEM objects (OBIS codes) reported by the meter. It is useful for diagnostics, understanding available measurements, and mapping scalers/units.

| Endpoint              | `api/v1/report/objects` |
| --------------------- | ------------------------ |
| Method                | GET                      |
| Response content type | application/json         |

--8<-- "../_partials/auth-note.md"

## Example response (from device 192.168.99.114)

```json
{
  "objects": [
    {
      "logical_name": "0-8:25.9.0",
      "class": 40,
      "size": 28,
      "push_object_list": [
        { "logical_name": "0-8:25.9.0", "class": 40, "attribute": 2, "data_index": 0 },
        { "logical_name": "0-0:42.0.0", "class": 1,  "attribute": 2, "data_index": 0 },
        { "logical_name": "1-1:1.8.0", "class": 3,  "attribute": 2, "data_index": 0 },
        { "logical_name": "1-1:2.8.0", "class": 3,  "attribute": 2, "data_index": 0 },
        { "logical_name": "1-1:3.8.0", "class": 3,  "attribute": 2, "data_index": 0 },
        { "logical_name": "1-1:4.8.0", "class": 3,  "attribute": 2, "data_index": 0 },
        { "logical_name": "0-0:96.14.0", "class": 1, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:1.7.0", "class": 3,  "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:2.7.0", "class": 3,  "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:32.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:52.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:72.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:31.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:51.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-0:71.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:21.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:41.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:61.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:22.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:42.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:62.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:23.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:43.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:63.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:24.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:44.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "1-4:64.7.0", "class": 3, "attribute": 2, "data_index": 0 },
        { "logical_name": "0-0:96.13.0", "class": 1, "attribute": 2, "data_index": 0 }
      ]
    },
    { "logical_name": "0-0:42.0.0",  "class": 1, "tag": 9,  "size": 16, "value": "4C475A31303330373834383535323034" },
    { "logical_name": "1-1:1.8.0",  "class": 3, "tag": 21, "size": 8,  "value": 75133, "unit": 30, "scaler": 0 },
    { "logical_name": "1-1:2.8.0",  "class": 3, "tag": 21, "size": 8,  "value": 25414, "unit": 30, "scaler": 0 },
    { "logical_name": "1-1:3.8.0",  "class": 3, "tag": 21, "size": 8,  "value": 82328, "unit": 32, "scaler": 0 },
    { "logical_name": "1-1:4.8.0",  "class": 3, "tag": 21, "size": 8,  "value": 19481, "unit": 32, "scaler": 0 },
    { "logical_name": "0-0:96.14.0", "class": 1, "tag": 9,  "size": 8,  "value": "5241544531000000" },
    { "logical_name": "1-0:1.7.0",  "class": 3, "tag": 20, "size": 8,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-0:2.7.0",  "class": 3, "tag": 20, "size": 8,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-0:32.7.0", "class": 3, "tag": 20, "size": 8,  "value": 234,   "unit": 35, "scaler": 0 },
    { "logical_name": "1-0:52.7.0", "class": 3, "tag": 20, "size": 8,  "value": 0,     "unit": 35, "scaler": 0 },
    { "logical_name": "1-0:72.7.0", "class": 3, "tag": 20, "size": 8,  "value": 0,     "unit": 35, "scaler": 0 },
    { "logical_name": "1-0:31.7.0", "class": 3, "tag": 20, "size": 8,  "value": 0,     "unit": 33, "scaler": -2 },
    { "logical_name": "1-0:51.7.0", "class": 3, "tag": 20, "size": 8,  "value": 0,     "unit": 33, "scaler": -2 },
    { "logical_name": "1-0:71.7.0", "class": 3, "tag": 20, "size": 8,  "value": 0,     "unit": 33, "scaler": -2 },
    { "logical_name": "1-4:21.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-4:41.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-4:61.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-4:22.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-4:42.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-4:62.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 27, "scaler": 0 },
    { "logical_name": "1-4:23.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 29, "scaler": 0 },
    { "logical_name": "1-4:43.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 29, "scaler": 0 },
    { "logical_name": "1-4:63.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 29, "scaler": 0 },
    { "logical_name": "1-4:24.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 29, "scaler": 0 },
    { "logical_name": "1-4:44.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 29, "scaler": 0 },
    { "logical_name": "1-4:64.7.0", "class": 3, "tag": 6,  "size": 4,  "value": 0,     "unit": 29, "scaler": 0 },
    { "logical_name": "0-0:96.13.0", "class": 1, "tag": 9,  "size": 21, "value": "436F6E73756D6572204D6573736167652054657874" }
  ]
}
```

Tip: See [OBIS reference](../90-appendix/appendix-d.md) to interpret logical names and DLMS units.

## Field reference

Base fields for every object:

| Field                         | Type    | Description |
| ----------------------------- | ------- | ----------- |
| `objects[]`                   | array   | List of DLMS/COSEM objects present in the last report |
| `objects[].logical_name`      | string  | OBIS code in `A-B:C.D.E` notation |
| `objects[].class`             | uint    | COSEM class id (e.g., 1=Data, 3=Register, 4=Extended Register, 8=Clock, 40=Push setup) |

Class-specific fields:

- Class 1 — Data
  - `tag` (uint): DLMS data type tag
  - `size` (uint): payload length
  - `value` (string/number): value; OCTET STRINGs are hex-encoded; DATE_TIME rendered as ISO8601 local time

- Class 3 — Register (scalable values)
  - `tag` (uint), `size` (uint)
  - `value` (number)
  - `unit` (uint): DLMS unit id (see OBIS appendix)
  - `scaler` (int): power-of-ten exponent; physical = value × 10^scaler

- Class 4 — Extended Register
  - All fields of Class 3, plus:
  - `status` (object): `{ tag, size, value }`
  - `captired_time` (string): ISO8601 local timestamp captured by meter (note: key name as exposed by API)

- Class 8 — Clock
  - `value` (string): ISO8601 local time
  - `time_zone` (int)
  - `status` (int)

- Class 40 — Push setup
  - `size` (uint): number of items
  - `push_object_list` (array): items with fields `{ logical_name, class, attribute, data_index }`

## Notes

- Availability depends on the meter protocol (DLMS/COSEM). Non-COSEM meters may return fewer objects.
- For string OCTET values (tag 9), you can decode hex to ASCII to obtain text (e.g., meter identifiers, messages).
- Use [Current scalers](../50-settings/scalers-current.md) or [Custom scalers](../50-settings/scalers-custom.md) to adjust presentation units.
