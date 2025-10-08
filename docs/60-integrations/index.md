---
title: System Integrations
category: integrations
tags:
- integrations
- home_automation
- energy_monitoring
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-08'
---

# System Integrations

## Overview

WhatWatt Go devices can be integrated with various home automation and energy management systems through REST API and MQTT protocols.

## Available Integrations

### Home Automation Systems

- **[Loxone](loxone.md)** - Complete integration guide for Loxone home automation
- **Home Assistant** - Integration via MQTT and REST (coming soon)
- **OpenHAB** - REST API integration (coming soon)

### Energy Management

- **Solar Inverters** - Direct energy data sharing
- **Battery Systems** - State of charge monitoring
- **Smart Grid** - Demand response integration

### Monitoring Platforms

- **Grafana** - Visualization and dashboards
- **InfluxDB** - Time series data storage
- **Prometheus** - Metrics collection

## Integration Methods

### REST API

- **Best for**: Polling-based systems, simple integrations
- **Protocols**: HTTP/HTTPS with optional authentication
- **Data format**: JSON
- **Update frequency**: Configurable polling intervals

### MQTT

- **Best for**: Real-time monitoring, event-driven systems
- **Protocols**: MQTT 3.1.1/5.0 with optional TLS
- **Data format**: JSON payloads
- **Update frequency**: Real-time streaming

## Getting Started

1. **Choose integration method**: REST polling vs MQTT streaming
2. **Configure device**: Set up network and authentication
3. **Follow system-specific guide**: See individual integration pages
4. **Test connection**: Verify data flow and functionality

## Common Requirements

- Device on same network or accessible via internet
- Network connectivity (WiFi or Ethernet)
- Optional: MQTT broker for MQTT integrations
- Optional: TLS certificates for secure connections
