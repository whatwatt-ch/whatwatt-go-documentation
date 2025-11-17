---
title: Actions Execution
category: concepts
tags:
- execution
- actions
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Actions Execution

## Document Context

- **Purpose**: API endpoint for executing predefined actions asynchronously with status tracking and error handling
- **When to use**: Triggering automated sequences, initiating HTTP/Modbus operations, running scheduled tasks programmatically
- **Prerequisites**: Actions defined via actions API, understanding of asynchronous execution, status monitoring concepts
- **Related to**: [Actions definition](index.md), [Status monitoring](status.md), [REST API conventions](../rest-conventions.md)
- **Validates against**: Action ID existence, execution state management, concurrent request limits (20 max)

## Key Facts

- **Endpoint**: `/api/v1/actions/call?id=<action_id>` - Execute action by ID
- **Method**: POST - Returns 202 Accepted with status tracking information
- **Execution**: Asynchronous with queued requests, supports concurrent actions
- **Status tracking**: Location header or JSON response with status_ids for monitoring
- **Limits**: 20 concurrent requests max, prevents duplicate execution of same action

--8<-- "../../_partials/auth-note.md"

## Endpoint Details

This endpoint executes a specified action that has been previously defined. Actions run asynchronously and can be monitored using the status endpoint.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/actions/call` |
| **Method** | `POST` |
| **Query Parameter** | `id=<action_id>` |

## Execution Process

1. **Action Queued**: Requests from the action are queued for asynchronous execution
2. **Status IDs Returned**:
    - When called via the HTTP page handler: returns HTTP 202 with a `Location` header pointing to `/api/v1/actions/status?id=<ids>`
    - When routed via the generic REST entry: returns HTTP 202 with a JSON body `{ "status_ids": [<id>, ...] }`
3. **Monitoring**: Use the status endpoint to track execution progress
4. **Completion**: Action completes when all requests finish

## Example Request

```bash
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=1'
```

## Expected Response (HTTP page handler)

```http
HTTP/1.1 202 Accepted
Content-Length: 0
Location: /api/v1/actions/status?id=139
X-Content-Type-Options: nosniff
Cache-Control: no-store, no-cache
```

The `Location` header contains the URL to check execution status.

## Expected Response (generic REST route)

```http
HTTP/1.1 202 Accepted
Content-Type: application/json; charset=utf-8

{ "status_ids": [139] }
```

## Response Codes

| Code | Status | Description |
|------|--------|-------------|
| **202** | Accepted | At least one request from the action has been queued for execution |
| **400** | Bad Request | The action is disabled, or all requests in the action are disabled |
| **404** | Not Found | No action found for the specified ID |
| **409** | Conflict | The action is already executing (another run still in progress) |
| **429** | Too Many Requests | Too many requests are being processed simultaneously (limit: 20 concurrent requests across all actions) |
| **500** | Internal Server Error | An unspecified issue occurred |

## Usage Examples

### Execute Different Actions

```bash
# Execute action with ID "1"
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=1'

# Execute action with ID "light_toggle"
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=light_toggle'

# Execute action with ID "modbus_write"
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=modbus_write'
```

### Extract Status ID from Response

```bash
# Execute action and extract status ID
RESPONSE=$(curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=1')
STATUS_ID=$(echo "$RESPONSE" | grep -i "location:" | sed 's/.*id=\([0-9]*\).*/\1/')
echo "Status ID: $STATUS_ID"

# Check status
curl -s "http://192.168.1.100/api/v1/actions/status?id=$STATUS_ID"
```

## Error Handling

### Action Not Found

```bash
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=nonexistent'
# Returns: 404 Not Found
```

### Action Already Running

```bash
# If action is already executing
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=1'
# Returns: 409 Conflict
```

### Queue Full

```bash
# If too many actions are queued (>20 requests)
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=1'
# Returns: 429 Too Many Requests
```

### Disabled Action

```bash
# If action has "enable": false
curl -i -X POST 'http://192.168.1.100/api/v1/actions/call?id=disabled_action'
# Returns: 400 Bad Request
```

## Best Practices

!!! tip "Status Monitoring"
    Use either the `Location` header (HTTP page handler) or the JSON `status_ids` (generic REST) to monitor execution.

!!! warning "Concurrent Execution"
    The same action ID cannot be executed concurrently. A repeated call while it runs returns HTTP 409.

!!! info "Processing limit"
    Up to 20 requests can be in progress at once (across all actions). Additional calls return 429 until some finish.

!!! note "Asynchronous Nature"
    HTTP 202 means the action was queued, not that it completed successfully. Check the status endpoint for actual results.

Use the [status endpoint](status.md) to monitor action execution progress and results.
