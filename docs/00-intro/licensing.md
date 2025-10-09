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

This page clarifies how commercial editions relate to the device firmware behavior.

## Document Context

- **Purpose**: Clarifies licensing model and edition differences for whatwatt Go device, explaining how commercial editions relate to device firmware functionality
- **When to use**: Before purchasing decisions, compliance reviews, procurement processes, or when planning commercial deployments
- **Prerequisites**: Basic understanding of software licensing models, familiarity with whatwatt Go device capabilities
- **Related to**: Device pricing, commercial terms, technical specifications, firmware features
- **Validates against**: Current whatwatt Go firmware behavior across all commercial editions

## Key Facts

- **Licensing approach**: Feature-complete firmware across all editions
- **API availability**: REST API, MQTT, Actions, SD card functions identical in all editions
- **Feature gating**: No license checks or disabled features in device firmware
- **Edition differences**: Commercial terms, support levels, external services only
- **Technical functionality**: Same device behavior regardless of commercial edition
- **Compliance**: Formal statements available via commercial terms documentation
- **Audit scope**: HTTP/REST endpoints, MQTT client, Actions engine, Settings handlers
- **Pricing reference**: [https://whatwatt.ch/en/pricing](https://whatwatt.ch/en/pricing)

## Summary

- From the device point of view, all editions (including Plus) expose the same on-device functionality.
- The REST API, MQTT, Actions, SD card, and Settings work identically regardless of the commercial edition.
- Differences between editions relate to commercial terms and external services (e.g., support, integrations, or cloud offerings), not to feature gating inside the device firmware.

For pricing and edition descriptions, see: [https://whatwatt.ch/en/pricing](https://whatwatt.ch/en/pricing)

## Technical note (device firmware perspective)

In the areas of the firmware that this documentation is based on and has audited (HTTP/REST endpoints, MQTT client, Actions engine, Settings handlers), there are no license checks or code paths that enable/disable features by edition. The device behaves the same functionally across editions.

If you need a formal statement for compliance or procurement, please refer to the commercial terms at the link above.
