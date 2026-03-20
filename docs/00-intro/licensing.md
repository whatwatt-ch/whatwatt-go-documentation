---
title: License & editions
category: concepts
tags:
- licensing
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---


# License & editions

This page explains how commercial licensing affects on-device REST API availability and selected runtime integration services.

## Document Context

- **Purpose**: Explains which REST features and runtime integrations are available without an additional license and which require Plus or higher
- **When to use**: Before integration planning, edition selection, procurement, or when troubleshooting `404 License required` or inactive integrations
- **Prerequisites**: Basic understanding of whatwatt Go REST API
- **Related to**: [REST API license requirements](../20-rest/license-requirements.md), [System Info](../10-general/system-info.md), [REST reference](../20-rest/reference/index.md), [MQTT Integration](../30-mqtt/index.md)
- **Validates against**: Firmware route registration and runtime license-dependent service behavior

## Key Facts

- **Licensing approach**: Base firmware is available without Plus, but selected REST endpoint groups and runtime integrations are gated
- **Required tier for advanced integrations**: Plus or higher
- **Licensed REST endpoints**: Report, report objects, variables, actions
- **Licensed runtime services**: Built-in MQTT publisher including TLS, myStrom cloud, meter proxy, Modbus TCP server, Berry script execution and auto-run
- **Runtime behavior**: Unlicensed devices return `404 License required` for gated routes, while licensed runtime services remain stopped or inactive
- **How to verify**: Check `.device.license.type` in `/api/v1/system`
- **Pricing reference**: [https://whatwatt.ch/en/pricing](https://whatwatt.ch/en/pricing)

## Summary

- Some REST features require Plus or higher.
- Core configuration and administration endpoints remain available without Plus.
- Advanced integration endpoints for reports, variables, and actions must be treated as licensed features.
- MQTT publishing, Secure MQTT, Modbus TCP, meter proxy, myStrom cloud, and Berry script execution also require Plus or higher at runtime.

For pricing and edition descriptions, see: [https://whatwatt.ch/en/pricing](https://whatwatt.ch/en/pricing)

## REST Endpoints Requiring Plus Or Higher

--8<-- "../_partials/license-plus-rest-endpoints.md"

## Runtime Features Requiring Plus Or Higher

- Built-in MQTT publishing over `mqtt://` and `mqtts://`
- Secure MQTT setup described in the TLS chapters, because it uses the same built-in MQTT client
- myStrom cloud integration
- Meter proxy service
- Modbus TCP server
- Berry script execution and auto-run

Configuration endpoints for these features can still be available on `FREE`, but the firmware keeps the services stopped until a Plus or higher license is active.

## How To Check The Active License

Check the license type in:

- `GET /api/v1/system`: inspect `.device.license.type`

If the reported type is `FREE`, the REST endpoint groups listed above are not available and the runtime features listed above remain inactive.

## Firmware Behavior On Unlicensed Devices

Without Plus or higher, the REST endpoints listed above are not available and return `404 License required`.

For runtime integrations, the firmware accepts configuration but does not activate the licensed services until the device has Plus or higher.

If you need a formal commercial statement for compliance or procurement, please refer to the pricing and commercial terms link above.
