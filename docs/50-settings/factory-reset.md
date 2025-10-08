---
title: Factory Reset
category: concepts
tags:
- factory_reset
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Factory Reset

## Document Context

- **Purpose**: Factory reset API endpoint for restoring device to original state with complete configuration erasure
- **When to use**: Device troubleshooting, preparing for redeployment, resolving persistent configuration issues, security reset
- **Prerequisites**: Administrative access, understanding of irreversible data loss, backup of critical configurations if needed
- **Related to**: Device restart (restart.md), firmware updates (firmware-update.md), initial device setup procedures
- **Validates against**: Factory state restoration requirements, configuration persistence boundaries, security reset protocols

## Key Facts

- **Endpoint**: `/api/v1/restore` - Triggers complete factory reset operation
- **Method**: POST - Returns 204 No Content on success, irreversible operation
- **Data loss**: ALL user settings, configurations, networks, passwords, certificates erased
- **Preservation**: Firmware version, hardware info, factory certificates remain intact
- **Alternative access**: Physical button, WebUI option, API endpoint - multiple reset methods

--8<-- "../_partials/auth-note.md"

!!! danger "Data Loss Warning"
    Factory reset will permanently erase ALL user settings, configurations, and data. This action cannot be undone!

!!! note "Alternative Methods"
    - Physical button press on the device
    - Factory reset from the device's WebUI

## Endpoint Details

This endpoint allows you to restore your device to factory settings, erasing all user configuration and returning the device to its original state.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/restore` |
| **Method** | `POST` |
| **Response** | `204 No Content` on success |

## What Gets Reset

### Configuration Reset

- ✅ **Network Settings**: Wi-Fi credentials, static IP configuration
- ✅ **MQTT Settings**: Broker configuration, credentials, topics
- ✅ **Service Settings**: All service configurations and schedules
- ✅ **User Accounts**: WebUI passwords and authentication
- ✅ **Custom Settings**: Actions, scalers, meter configurations
- ✅ **Certificates**: TLS certificates and security settings

## Example Request

=== "No auth"
    ```bash
    curl -i -X POST http://192.168.1.100/api/v1/restore
    ```

=== "With password"
    ```bash
    curl -i -X POST --anyauth -u ":PASSWORD" http://192.168.1.100/api/v1/restore
    ```

## Expected Response

```http
HTTP/1.1 204 No Content
Content-Length: 0
```

## Best Practices

!!! tip "Configuration Backup"
    Always backup current configuration before factory reset for potential restoration.

!!! warning "Network Planning"
    Plan how to reconnect to the device after reset, as network settings will be erased.

!!! caution "Physical Access"
    Ensure physical access to the device in case network recovery fails.

!!! info "Documentation"
    Document current settings and configuration before reset for easier reconfiguration.
