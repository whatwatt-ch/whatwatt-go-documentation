---
title: REST API License Requirements
category: concepts
tags:
- licensing
- rest-api
- editions
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# REST API License Requirements

## Document Context

- **Purpose**: Documents which REST endpoints require an active Plus or higher license and how the firmware behaves when the license is missing
- **When to use**: Integration planning, troubleshooting `404 License required`, choosing device edition, validating feature availability before deployment
- **Prerequisites**: Basic familiarity with REST endpoints and HTTP status codes
- **Related to**: [License & editions](../00-intro/licensing.md), [REST reference](reference/index.md), [System Info](../10-general/system-info.md)
- **Validates against**: Firmware route registration in the device HTTP server

## Key Facts

- **License scope**: Only part of the REST API is gated; the rest of the device configuration API remains available without Plus
- **Required tier**: Plus or higher
- **Firmware behavior**: Gated routes return `404 License required` using the original HTTP method of the endpoint
- **How to verify**: Check `.device.license.type` in `/api/v1/system`
- **Maintenance model**: One central list is used here and linked from endpoint pages
- **Scope note**: This page covers REST only; MQTT and selected runtime services are listed on the license overview page

## Endpoints Requiring Plus Or Higher

--8<-- "../_partials/license-plus-rest-endpoints.md"

## How To Check License State

Check the license type in:

- `GET /api/v1/system`: inspect `.device.license.type`

If the device reports `FREE`, the endpoint groups listed above are not available.

## What Happens Without The Required License

Without Plus or higher, the endpoints listed above are not available and return `404 License required`.

## Integration Guidance

- For a universal connectivity check, use `/api/v1/system`
- Use `/api/v1/report` only when Plus or higher is confirmed
- If your integration depends on reports, variables, or actions, treat Plus as a prerequisite
