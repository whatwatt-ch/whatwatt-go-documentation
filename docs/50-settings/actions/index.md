---
title: Actions Definition
category: concepts
tags:
- actions
- index
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Actions Definition

## Document Context

- **Purpose**: Actions API definition for configuring automated HTTP/Modbus request sequences with constants, timeouts, and asynchronous execution
- **When to use**: Automating device interactions, triggering external systems, implementing complex workflows, integrating with third-party services
- **Prerequisites**: HTTP/REST API knowledge, optional Modbus understanding, firmware 1.6.1+, action design planning
- **Related to**: Action execution (execution.md), action status monitoring (status.md), REST conventions (rest-conventions.md)
- **Validates against**: Action definition schema, HTTP/Modbus protocol requirements, timeout constraints, payload size limits

## Key Facts

- **Endpoint**: `/api/v1/actions` - Define, retrieve, and delete automated action sequences
- **Methods**: GET (retrieve), POST (define), DELETE (remove) - JSON configuration format
- **Components**: Constants for reuse, HTTP requests with headers/payloads, Modbus operations
- **Constraints**: 15-char action IDs, 1023-char payloads, 4 HTTP headers max, 0.1-10s timeouts
- **Execution**: Asynchronous processing with status monitoring and built-in error handling

--8<-- "../../_partials/auth-note.md"

!!! info "Firmware Requirement"
    This API is available since firmware version 1.6.1

!!! note "Alternative Method"
    Actions can also be configured from the device's WebUI.

## Endpoint Details

This API provides a structured way to define and execute automated actions consisting of HTTP/Modbus requests. The execution mechanism ensures asynchronous processing, with built-in mechanisms for monitoring execution status.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/actions` |
| **Methods** | `GET`, `POST`, `DELETE` |
| **Response Content Type** | `application/json` |

## Methods

- **GET** – Retrieve the definition of actions
- **POST** – Define new actions
- **DELETE** – Delete existing actions definition

## Configuration Structure

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `const` | object | No | Optional constants definition (IP addresses, values, etc.) |
| `actions` | array | Yes | Array of action definitions |

### Constants Object

Constants can be defined for reuse throughout action definitions:

| Field Type | Supported | Description |
|------------|-----------|-------------|
| `string` | ✅ | Text values, URLs, IP addresses |
| `number` | ✅ | Numeric values |
| `boolean` | ✅ | True/false values |
| `null` | ✅ | Null values |
| `object` | ❌ | Not supported |
| `array` | ❌ | Not supported |

**Usage**: Reference constants using `${constant_name}` syntax in `http.url`, `http.payload`, `modbus.host`, and `modbus.value` fields. Constants are not expanded in HTTP header names/values.

### Action Definition

| Field | Type | Required | Range | Description |
|-------|------|----------|-------|-------------|
| `id` | string | Yes | 1..15 chars | Unique action identifier (name or numeric ID) |
| `enable` | boolean | No | - | Defaults to `true`. Set to `false` to disable action |
| `requests` | array | Yes | - | List of requests to execute |

### HTTP Request Fields

| Field | Type | Required | Range | Description |
|-------|------|----------|-------|-------------|
| `http.enable` | boolean | No | - | Defaults to `true`. Set to `false` to disable request |
| `http.url` | string | Yes | 8..255 chars | Target URL. Constants may be used |
| `http.method` | string | No | GET, POST, PUT, DELETE | HTTP method. Defaults to `GET` |
| `http.payload` | string | No | 0..1023 chars | Request body (POST/PUT only) |
| `http.headers.*` | object | No | - | Up to 4 HTTP headers (name + value ≤ 253 chars) |
| `http.timeout` | float | No | 0.1..10 | Request timeout in seconds. Defaults to 5s |

### Modbus Request Fields

| Field | Type | Required | Range | Description |
|-------|------|----------|-------|-------------|
| `modbus.enable` | boolean | No | - | Defaults to `true`. Set to `false` to disable |
| `modbus.host` | string | Yes | 4..63 chars | Target hostname or IP address |
| `modbus.port` | uint | No | 1..65535 | TCP port. Defaults to 502 |
| `modbus.unit_id` | uint | No | 0..255 | Modbus Unit ID. Defaults to 0 |
| `modbus.func` | uint | Yes | 5, 6, 15, 16 | Modbus function code |
| `modbus.address` | uint | Yes | 0..65535 | Starting data address (zero-based) |
| `modbus.type` | string | No | Various | Data type. Defaults to `hex` |
| `modbus.value` | string | Yes | 1..492 chars | Value to write (format depends on type) |
| `modbus.timeout` | float | No | 0.1..10 | Request timeout. Defaults to 5s |

### Modbus Function Codes

| Code | Name | Description |
|------|------|-------------|
| `5` | Write Single Coil | Write one coil (ON/OFF) |
| `6` | Write Single Register | Write one 16-bit register |
| `15` | Write Multiple Coils | Write multiple coils |
| `16` | Write Multiple Registers | Write multiple 16-bit registers |

### Modbus Data Types

| Type | Input Format | Storage | Example |
|------|--------------|---------|---------|
| `hex` | Even-length hex string | Raw bytes | `0809A0B0` |
| `short` | 16-bit integer | 1 register, big-endian | `1234`, `-1234` |
| `int` | 32-bit integer | 2 registers, big-endian | `123456` |
| `long` | 64-bit integer | 4 registers, big-endian | `1234567890` |
| `float` | 32-bit float | 2 registers, IEEE-754 | `-1.23` |
| `double` | 64-bit double | 4 registers, IEEE-754 | `3.14159` |

### Modbus Value Guidelines

| Function | Recommended Type & Value |
|----------|-------------------------|
| **5 (Single Coil)** | `short` with `0`/`1` or `hex` with `0000`/`00FF` |
| **6 (Single Register)** | `short` (integer) or `hex` (2 bytes) |
| **15 (Multiple Coils)** | `hex` notation (4 hex chars = 1 register) |
| **16 (Multiple Registers)** | Any type (`hex`, `short`, `int`, `float`, `double`) |

## Example Configuration

```json
{
  "const": {
    "bulb": "192.168.99.101",
    "switch": "192.168.99.151",
    "bri": "20"
  },
  "actions": [
    {
      "id": "1",
      "requests": [
        {
          "http": {
            "url": "http://192.168.0.21/api/v1/device/self",
            "method": "POST",
            "payload": "action=toggle",
            "headers": {
              "Content-Type": "application/x-www-form-urlencoded"
            }
          }
        },
        {
          "http": {
            "url": "http://${switch}/toggle"
          }
        }
      ]
    },
    {
      "id": "2",
      "requests": [
        {
          "http": {
            "url": "http://${bulb}/light/0?turn=on&brightness=${bri}&temp=3000"
          }
        }
      ]
    },
    {
      "id": "3",
      "requests": [
        {
          "http": {
            "url": "http://${bulb}/light/0",
            "method": "POST",
            "payload": "turn=off",
            "timeout": 2
          }
        }
      ]
    },
    {
      "id": "4",
      "requests": [
        {
          "modbus": {
            "host": "192.168.99.179",
            "port": 1502,
            "unit_id": 1,
            "func": 16,
            "address": 10,
            "type": "short",
            "value": "${bri}",
            "timeout": 2
          }
        }
      ]
    }
  ]
}
```

## Response Codes

| Code | Description |
|------|-------------|
| **200 OK** | Successful retrieval or modification |
| **204 No Content** | Successful deletion |
| **404 Not Found** | Actions have not been set or have been deleted |
| **400 Bad Request** | Invalid request format |

## Limitations

!!! warning "Size Limit"
    The action definition object cannot exceed **8191 bytes**

!!! warning "Header Limit"
    Maximum 4 HTTP headers per request, with name + value ≤ 253 characters

!!! info "Performance"
    Actions execute asynchronously to avoid blocking the device
