---
title: Device Settings
category: api-endpoints
tags:
- configuration
- settings
- device-management
- system-config
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /api/v1/settings
protocols:
- HTTP
- REST
related_concepts:
- device configuration
- service management
- authentication setup
- power management
use_cases:
- device setup
- service configuration
- authentication management
- system administration
real_device_tested: true
authentication: required when device password is set
methods:
- GET
- POST
- PUT
---

# Device Settings

## Document Context

- **Purpose**: Configure device system settings, service enablement, and authentication protection
- **When to use**: For initial device setup, service configuration, security setup, or system administration
- **Prerequisites**: Network access to device; understanding of intended services and security requirements
- **Related to**: Device initialization, service management, Web UI protection, cloud integrations
- **Validates against**: Real device settings from whatwatt Go hardware

## Key Facts

- **Endpoint**: `/api/v1/settings`
- **Methods**: GET, POST, PUT
- **Authentication**: Required when device Web UI password is set
- **Dynamic apply**: Changes take effect immediately without reboot
- **Response format**: JSON with nested system and services objects
- **Sections**: `system` (device identity, protection) and `services` (cloud/local integrations)
- **No reboot needed**: Configuration changes apply dynamically
- **Error codes**: 400 (invalid config), 401 (auth required)

## Endpoint Details

This endpoint manages the device's basic system settings and enables/disables built-in services.

| Endpoint              | `api/v1/settings` |
| --------------------- | ----------------- |
| Method                | GET, POST, PUT    |
| Response content type | application/json  |

!!! info "Dynamic apply"
    Configuration changes are applied without requiring a device reboot. The Web UI and HTTP pages reload dynamically after updates. Avoid reboots during operation; only firmware upgrades trigger an automatic restart.

## Object schema

- Top-level sections
  - `system`: device-identifying properties and access protection
  - `services`: cloud/local integrations and built-in services

### Fields: system

| JSON path              | Type    | Default                 | Range/Rules                             | Notes |
| ---------------------- | ------- | ----------------------- | --------------------------------------- | ----- |
| `system.name`          | string  | ""                      | length 0..31                            | Friendly device name |
| `system.host_name`     | string  | `whatwatt_XXXXXX`       | length 0..31; must be a valid hostname  | Used on network and for realm; write rejected if invalid |
| `system.protection`    | boolean | false                   |                                         | When true and `password` set, HTTP auth is enforced |
| `system.password`      | string  | ""                      | length 0..31                            | Write-only; hidden in GET responses |
| `system.power_save`    | boolean | false                   |                                         | Lowers power consumption; see constraint below |

Constraints

- Enabling `system.power_save` is rejected while the Ethernet link is UP (request returns 400).
- `system.host_name` must be valid; invalid value causes 400.

### Fields: services

| JSON path                                 | Type     | Default             | Range/Rules                     | Notes |
| ----------------------------------------- | -------- | ------------------- | ------------------------------- | ----- |
| `services.cloud.what_watt`                | boolean  | true                |                                 | whatwatt Cloud integration |
| `services.cloud.solar_manager`            | boolean  | false or true*      |                                 | Solar Manager cloud (see note*) |
| `services.cloud.mystrom`                  | boolean  | false or true*      |                                 | myStrom cloud (see note*) |
| `services.cloud.stromkonto`               | boolean  | false               |                                 | Stromkonto toggle (exposed in GET; applied if present in body) |
| `services.local.solar_manager`            | boolean  | false or true*      |                                 | Local Solar Manager API |
| `services.broadcast`                      | boolean  | true                |                                 | mDNS broadcast (discovery) |
| `services.other_energy_provider`          | boolean  | false               |                                 | Enable other energy provider features |
| `services.report_interval`                | uint     | 30                  | 1..3600 (seconds)               | Cloud/custom reporting interval |
| `services.log`                            | boolean  | false               |                                 | Enable internal log service |
| `services.meter_proxy`                    | boolean  | false               |                                 | Enable meter proxy service |
| `services.sd.enable`                      | boolean  | false               |                                 | Store periodic reports to SD card |
| `services.sd.frequency`                   | uint     | 15                  | 1..1440 (minutes)               | SD write cadence |
| `services.modbus.enable`                  | boolean  | false               |                                 | Modbus TCP server |
| `services.modbus.port`                    | uint     | 502                 | 1..65535                        | Modbus TCP port |
| `services.berry.auto_run`                 | boolean  | false               |                                 | Auto-run Berry script on boot |
| `services.berry.run_delay`                | uint     | 300                 | 60..86400 (seconds)             | Delay before auto-run |

!!! note "Notes"
    - "false or true*" defaults become true on devices with sufficient RAM (PSRAM); otherwise false.
    - `services.cloud.stromkonto` appears in GET; if included in POST/PUT it's applied separately to Stromkonto config.

## Examples

### Read current settings

=== "No auth"
    ```bash
    curl http://whatwatt-XXXXXX.local/api/v1/settings
    ```

=== "With password"
    ```bash
    curl --anyauth -u :PASSWORD http://whatwatt-XXXXXX.local/api/v1/settings
    ```

Example response (abridged):

```json
{
  "system": {
    "name": "",
    "host_name": "whatwatt_9F8124",
    "protection": false,
    "power_save": false
  },
  "services": {
    "cloud": {
      "what_watt": true,
      "solar_manager": false,
      "mystrom": false,
      "stromkonto": false
    },
    "local": {
      "solar_manager": false
    },
    "broadcast": true,
    "other_energy_provider": false,
    "report_interval": 30,
    "log": false,
    "meter_proxy": false,
    "sd": { "enable": false, "frequency": 15 },
    "modbus": { "enable": false, "port": 502 },
    "berry": { "auto_run": false, "run_delay": 300 }
  }
}
```

### Enable Web UI protection

```json
{
  "system": {
    "protection": true,
    "password": "your-secure-password"
  }
}
```

### Configure SD card logging

```json
{
  "services": {
    "sd": { "enable": true, "frequency": 60 }
  }
}
```

### Enable Modbus TCP

```json
{
  "services": {
    "modbus": { "enable": true, "port": 502 }
  }
}
```

### Adjust cloud reporting cadence

```json
{ "services": { "report_interval": 15 } }
```

### Toggle Stromkonto cloud

```json
{ "services": { "cloud": { "stromkonto": true } } }
```

## Method semantics

- GET: returns current settings (with `system.password` hidden)
- PUT: partial update; only provided fields change
- POST: full replace; unspecified fields reset to zero/empty/false

!!! note "Recommendations"
    - Prefer PUT for targeted changes
    - For POST, include the complete desired object to avoid resetting fields unintentionally

## Error cases

- 400 Bad Request
  - Invalid `system.host_name`
  - Attempt to enable `system.power_save` while Ethernet link is active
  - Payload fails validation (types/ranges)

## See also

- [REST conventions](rest-conventions.md)
- [System Info (read-only)](../10-general/system-info.md)
