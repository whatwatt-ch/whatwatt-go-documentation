---
title: Overview
category: concepts
tags:
- introduction
- overview
- getting-started
- api-basics
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- overview
protocols:
- REST
- MQTT
- HTTP
related_concepts:
- energy monitoring
- smart metering
- iot device
- api integration
use_cases:
- getting started
- understanding capabilities
- choosing integration method
- project planning
real_device_tested: false
---

# Overview

## Document Context

- **Purpose**: Provides comprehensive overview of whatwatt Go device integration capabilities and API methods for energy monitoring applications
- **When to use**: Starting point for developers planning whatwatt Go integration, choosing between REST API and MQTT protocols
- **Prerequisites**: Basic understanding of HTTP APIs and MQTT messaging protocols, familiarity with energy monitoring concepts
- **Related to**: REST API polling, MQTT streaming, device discovery, authentication methods
- **Validates against**: whatwatt Go device capabilities across firmware versions 1.2+

## Key Facts

- **Integration methods**: REST API over HTTP + MQTT client connection
- **Primary protocols**: HTTP/1.1, MQTT 3.1.1, Server-Sent Events (SSE)
- **Authentication**: HTTP Authentication (when device protection enabled)
- **Data formats**: JSON responses, CSV logging, MQTT JSON payloads
- **Network requirements**: Local network access (mDNS discovery supported)
- **Real-time capability**: Sub-second updates via SSE streaming and MQTT
- **Energy data types**: Instantaneous power, cumulative energy, voltage, current, tariff information
- **Device compatibility**: All whatwatt Go hardware revisions with firmware 1.2+

The whatwatt Go device can be integrated into systems using two primary methods: the MQTT client connection and local REST API over HTTP. Each method offers unique advantages and is suited for different scenarios, particularly concerning network reliability, bandwidth usage, and ease of integration.

This site documents both integration methods with detailed guides, examples, and reference materials.

## Integration Methods

Both integration methods ensure that the device can be seamlessly incorporated into various systems, enhancing its functionality and utility:

- **MQTT client connection** - ideal for applications requiring real-time power usage monitoring and efficient network usage
- **REST API over HTTP** - offers a simple and widely compatible integration method

Use the left navigation to browse guides and reference materials for each integration method.
