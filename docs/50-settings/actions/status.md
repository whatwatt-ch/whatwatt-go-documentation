---
title: Actions Status
category: concepts
tags:
- actions
- status
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Actions Status

--8<-- "../../_partials/auth-note.md"

## Document Context

- **Purpose**: Action execution status monitoring API for tracking progress and results of asynchronous HTTP/Modbus requests
- **When to use**: Monitoring action execution progress, checking completion status, debugging failed requests, automated status polling
- **Prerequisites**: Active action executions with status IDs, understanding of HTTP/Modbus status codes, asynchronous execution concepts
- **Related to**: [Action execution](execution.md), [Action definition](index.md), asynchronous monitoring patterns
- **Validates against**: HTTP status code standards, Modbus protocol status codes, execution timing measurements

## Key Facts

- **Endpoint**: `/api/v1/actions/status?id=<status_id>[,<status_id>]` - Monitor execution progress by status ID
- **Method**: GET with comma-separated status IDs - Query multiple executions simultaneously
- **Status tracking**: HTTP codes (2xx success, 4xx/5xx errors), Modbus codes (1 success), -1 while running
- **Execution details**: Action ID, status ID, result code, execution time in seconds
- **Monitoring pattern**: Poll status endpoint until code ≠ -1 for completion detection

## Endpoint Details

This endpoint retrieves execution status for specified request IDs. Use this to monitor the progress and results of action executions.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/actions/status` |
| **Method** | `GET` |
| **Query Parameter** | `id=<status_id>[,<status_id>]` |
| **Response Content Type** | `application/json` |

## Response Format

The endpoint returns an array of status objects, one for each request ID.

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `action_id` | string | The action ID corresponding to this status entry |
| `id` | uint | Execution status ID (from the Location header) |
| `code` | int | Result code: HTTP status for HTTP requests; negative values for Modbus/connection errors; `-1` while running |
| `exe_time` | float | Execution time in seconds (0 while running) |

## Example Usage

### Single Status Check

```bash
curl -s 'http://192.168.1.100/api/v1/actions/status?id=139'
```

**Response:**

```json
[
  {
    "action_id": "1",
    "id": 139,
    "code": 200,
    "exe_time": 0.133
  }
]
```

### Multiple Status Check

```bash
curl -s 'http://192.168.1.100/api/v1/actions/status?id=139,140,141'
```

**Response:**

```json
[
  {
    "action_id": "1",
    "id": 139,
    "code": 200,
    "exe_time": 0.133
  },
  {
    "action_id": "2",
    "id": 140,
    "code": 404,
    "exe_time": 1.205
  },
  {
    "action_id": "1",
    "id": 141,
    "code": -1,
    "exe_time": 0.000
  }
]
```

## Status Code Interpretation

### HTTP Status Codes (HTTP requests)

Standard HTTP response codes indicate the success/failure of HTTP action requests:

| Code Range | Meaning | Examples |
|------------|---------|----------|
| **2xx** | Success | 200 OK, 204 No Content |
| **4xx** | Client Error | 400 Bad Request, 404 Not Found |
| **5xx** | Server Error | 500 Internal Server Error |
| `-1` | Running | Request is still in progress |
| `≤0` (other) | Network/Connection Issue | Cannot connect, timeout |

### Modbus Status Codes (Modbus requests)

For Modbus requests, specific codes indicate different types of issues:

#### Success

| Code | Description |
|------|-------------|
| `1` | Success |

#### Connection Issues

| Code | Description |
|------|-------------|
| `-1` | Generic issue |
| `-16` | Cannot resolve host |
| `-17` | Cannot connect |
| `-19` | Cannot create connection |

#### Protocol Issues

| Code | Description |
|------|-------------|
| `-2` | Response packet too long |
| `-3` | Response receive timeout |
| `-4` | Response receive error |
| `-5` | Invalid PDU length in response |
| `-7` | Request sent error |
| `-8` | Invalid response header |
| `-9` | Transaction ID mismatch |
| `-10` | Function mismatch |
| `-12` | Unit ID mismatch |
| `-13` | Response frame too short |
| `-14` | Response body mismatch |
| `-15` | Cannot process response |

#### Modbus Exceptions (Device Responses)

| Code | Description |
|------|-------------|
| `-101` | Illegal function |
| `-102` | Illegal data address |
| `-103` | Illegal data value |
| `-104` | Slave device failure |
| `-105` | Acknowledge |
| `-106` | Slave device busy |
| `-107` | Negative acknowledge |
| `-108` | Memory parity error |
| `-110` | Gateway path unavailable |
| `-111` | Gateway target device failed to respond |

## Monitoring Workflow

### Complete Action Monitoring

```bash
#!/bin/bash

# 1. Execute action and capture response
RESPONSE=$(curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=1')

# 2. Extract status ID from Location header
STATUS_ID=$(echo "$RESPONSE" | grep -i "location:" | sed 's/.*id=\([0-9]*\).*/\1/')

if [ -n "$STATUS_ID" ]; then
    echo "Action queued with status ID: $STATUS_ID"

    # 3. Poll status until completion
    while true; do
        STATUS=$(curl -s "http://192.168.1.100/api/v1/actions/status?id=$STATUS_ID")
        CODE=$(echo "$STATUS" | jq -r '.[0].code')
        EXE_TIME=$(echo "$STATUS" | jq -r '.[0].exe_time')

        echo "Status: Code=$CODE, Time=${EXE_TIME}s"

        if [ "$CODE" != "null" ] && [ "$CODE" != "0" ]; then
            echo "Action completed"
            break
        fi

        sleep 1
    done
else
    echo "Failed to extract status ID from response"
fi
```

### Batch Status Monitoring

```bash
# Check multiple executions at once
STATUS_IDS="139,140,141,142"
curl -s "http://192.168.1.100/api/v1/actions/status?id=$STATUS_IDS" | jq '
  .[] |
  "Action \(.action_id): \(
    if .code > 0 then
      "✓ Success (HTTP \(.code))"
    elif .code == 0 then
      "⏳ Running..."
    else
      "✗ Failed (\(.code))"
    end
  ) - \(.exe_time)s"
'
```

## Best Practices

!!! tip "Status ID Source"
  Use status IDs from the execution response (Location header or JSON body). Avoid guessing IDs.

!!! info "Polling Interval"
    Poll status every 1-2 seconds for responsive monitoring without overwhelming the device.

!!! warning "Status Retention"
  The device keeps a rolling buffer of recent statuses (up to 40 entries). Check status promptly.

!!! note "Multiple Requests"
  Each request in an action generates a separate status entry. Use the set of returned IDs to track all requests.

Use this endpoint in conjunction with [action execution](execution.md) to implement robust action monitoring and error handling.
