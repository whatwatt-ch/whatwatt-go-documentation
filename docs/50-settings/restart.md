---
title: Restart
category: concepts
tags:
- restart
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Restart

## Document Context

- **Purpose**: Remote device reboot API endpoint for troubleshooting and maintenance operations via REST API
- **When to use**: Troubleshooting connectivity issues, recovery from unresponsive state, testing system reliability
- **Prerequisites**: Administrative access, understanding that reboot interrupts data collection, rare necessity in normal operation
- **Related to**: [System information](../10-general/system-info.md), [Firmware updates](firmware-update.md), [Factory reset](factory-reset.md)
- **Validates against**: Device uptime capabilities (months of operation), 30-60 second reboot cycle timing

## Key Facts

- **Endpoint**: `/api/v1/reboot` - Triggers immediate device restart
- **Method**: POST - Returns 204 No Content on success, connection lost during reboot
- **Downtime**: 30-60 seconds typical reboot cycle with data collection interruption
- **Auto-restart**: Device never self-reboots except after firmware updates
- **Usage**: Rarely needed due to dynamic configuration and robust operation

--8<-- "../_partials/auth-note.md"

!!! info "Do you need to reboot?"
    Configuration changes apply dynamically without a reboot. The device is designed for long uninterrupted operation (months of uptime). The only routine case that triggers a reboot is a successful firmware upgrade.

!!! tip "No automatic restarts"
    The device never restarts itself during normal operation. If you see a reboot, it was explicitly requested by an API call/WebUI action or triggered at the end of a firmware update.

!!! note "Alternative Method"
    Device restart can also be performed from the device's WebUI.

!!! warning "Connection Loss"
    A reboot temporarily interrupts data collection and connectivity (typically ~30–60 seconds). To ensure uninterrupted logging, avoid rebooting unless strictly necessary.

## Endpoint Details

This endpoint allows you to reboot the device remotely. In normal operation you should not need to use it.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/reboot` |
| **Method** | `POST` |
| **Response** | `204 No Content` on success |

## Example Request

=== "No auth"
    ```bash
    curl -i -X POST http://whatwatt-XXXXXX.local/api/v1/reboot
    ```

=== "With password"
    ```bash
    curl --anyauth -u :PASSWORD -i -X POST http://whatwatt-XXXXXX.local/api/v1/reboot
    ```

## Expected Response

```http
HTTP/1.1 204 No Content
Content-Length: 0
```
