---
title: First Request
category: concepts
tags:
- first_request
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# First request

## Document Context

- **Purpose**: Provides quick-start guide with minimal curl commands to verify whatwatt Go device connectivity and demonstrate basic data retrieval
- **When to use**: First-time device setup, connectivity testing, API proof-of-concept, new developer onboarding
- **Prerequisites**: Device on local network, curl installed, basic command line knowledge
- **Related to**: Device discovery, authentication setup, REST API polling, system information
- **Validates against**: Live device responses via /api/v1/system and /api/v1/report endpoints

## Key Facts

- **Quick test endpoints**: /api/v1/system (device info), /api/v1/report (energy data)
- **Methods**: GET requests only
- **Authentication**: Optional (required only if device protection enabled)
- **Response format**: JSON with device metadata and energy measurements
- **Network discovery**: Use mDNS hostname whatwatt-XXXXXX.local or IP address
- **No meter required**: System endpoint works without meter connection
- **Meter required**: Report endpoint needs connected energy meter for meaningful data
- **Next steps**: Choose REST polling vs. MQTT streaming based on use case

This page shows two minimal requests to verify connectivity and see live data, then points you to full guides.

--8<-- "../_partials/auth-note.md"

## 1) System information (device)

```bash
# Replace host with your device hostname or IP
curl http://whatwatt-XXXXXX.local/api/v1/system
```

- Fast health check and basic metadata
- For details: see [System Info](../10-general/system-info.md)

## 2) Current report (meter)

```bash
# Returns the latest parsed report from the meter
curl http://whatwatt-XXXXXX.local/api/v1/report
```

- You’ll see power, energy, and meter fields when a meter is connected
- For polling details: see [REST → Polling](../20-rest/polling.md)
- For live streaming: see [REST → Streaming](../20-rest/streaming.md)

## Next steps

- Prefer REST? Start with [REST → Conventions](../50-settings/rest-conventions.md) and [Polling](../20-rest/polling.md)
- Prefer MQTT? Start with [MQTT → Overview](../30-mqtt/index.md) and [Template](../30-mqtt/template.md)
