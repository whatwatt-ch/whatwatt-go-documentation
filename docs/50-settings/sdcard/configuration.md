---
title: Configuration
category: concepts
tags:
- sdcard
- configuration
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---


# Configuration

## Document Context

- **Purpose**: SD card logging service configuration for automated report saving with customizable frequency settings
- **When to use**: Enabling local data storage, configuring backup logging, setting up offline data collection
- **Prerequisites**: SD card inserted and formatted, understanding of services configuration, CSV format knowledge
- **Related to**: Services configuration (services.md), SD card usage (usage-examples.md), file listing (listing.md)
- **Validates against**: SD card availability, frequency range constraints (1-1440 seconds), filesystem write capabilities

## Key Facts

- **Configuration**: services.sd.enable (boolean) and services.sd.frequency (1-1440 seconds)
- **File format**: YYYYMMDD.CSV daily files with automatic date-based naming
- **Frequency**: 1-1440 seconds interval for report writing (default 15 seconds)
- **Default state**: Disabled by default, requires explicit enablement via WebUI or REST API
- **Integration**: Part of device services system with centralized enable/disable control

Configure SD card logging via the services endpoint.

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `.services.sd.enable` | boolean | `false` | - | Enable/disable saving reports to SD card |
| `.services.sd.frequency` | uint | `15` | 1..1440 | Frequency in seconds for writing reports to SD |

CSV report files are named `YYYYMMDD.CSV`. By default the service is disabled; enable it in the WebUI or with REST.
