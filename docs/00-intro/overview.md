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
last_verified: '2026-07-14'
api_endpoints:
- overview
protocols:
- REST
- MQTT
- Modbus
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

whatwatt Go is a compact smart-meter interface device. It reads measurement data from a compatible electricity meter, parses the meter protocol into a common internal representation, and exposes the processed data through several local integration interfaces.

## Key Facts

- **Integration methods**: REST API, MQTT client, Modbus TCP slave, Berry scripting, Actions
- **Primary protocols**: HTTP/1.1, MQTT 3.1.1, Modbus TCP, Server-Sent Events (SSE)
- **Authentication**: HTTP Authentication (when device protection enabled)
- **Data formats**: JSON responses, CSV logging, MQTT JSON payloads, Modbus registers
- **Network requirements**: Local network access (mDNS discovery supported)
- **Real-time capability**: Sub-second updates via SSE streaming and MQTT
- **Energy data types**: Instantaneous power, cumulative energy, voltage, current, tariff information, power factor
- **Device compatibility**: All whatwatt Go hardware revisions with firmware 1.2+

## Integration Methods

whatwatt Go can be integrated into systems using several methods. Each method offers unique advantages and is suited for different scenarios.

### REST API

HTTP-based request-response for on-demand reads, device configuration, and status information. Supports JSON responses and optional SSE streaming for continuous updates without polling.

- **Best for**: Web applications, dashboards, simple integrations, configuration access
- **Data format**: JSON
- **Streaming**: SSE (`/api/v1/stream`) for live updates
- **[→ REST Polling](../20-rest/polling.md)** · **[→ REST Streaming](../20-rest/streaming.md)**

### MQTT

The device operates as an MQTT client and publishes measurement data to a broker configured by the user. Ideal for real-time applications and IoT integration.

- **Best for**: Home automation, IoT platforms, event-driven architectures
- **Data format**: JSON payloads, configurable via payload templates
- **Security**: TLS support with optional mutual TLS
- **[→ MQTT Guide](../30-mqtt/index.md)** · **[→ Secure MQTT](../40-secure-mqtt/index.md)**

### Modbus TCP

The device can emulate a Modbus TCP slave, exposing measurement data as Modbus registers. This enables integration with industrial systems, energy management controllers, EV chargers, and photovoltaic inverters that communicate over Modbus TCP.

- **Best for**: SCADA systems, EV chargers, inverters, industrial controllers
- **Function codes**: `04` — Read Input Registers, `03` — Read Holding Registers (from FW 2.0.2)
- **Register map**: Default layout (Siemens PAC2200 compatible) or fully custom configuration
- **Data types**: Configurable per register — `float`, `int`, `long`, `short`, `double`, `string`
- **Word order**: Configurable per register set — `msw` (default) or `lsw`
- **Templates**: Ready-to-load layouts for Siemens PAC2200, Carlo Gavazzi EM24_E1, Huawei DTSU666-H, Huawei DDSU666-H, Huawei SmartLogger, Huawei EMMA, Fronius Smart Meter 63A, Herholdt M3PRO, SunSpec Model 203, SunSpec Model 213, and Janitza B604
- **[→ Modbus TCP Guide](../35-modbus/index.md)** · **[→ Modbus Templates](../35-modbus/examples.md)**

### Berry Scripting

Firmware 2.0.0 introduces a Berry scripting engine for implementing integration logic directly on the device. Scripts can react to meter reports, execute periodic functions, make HTTP or HTTPS requests, perform Modbus TCP transactions, and call selected local APIs.

- **Best for**: Custom on-device automation, protocol bridging, conditional logic
- **Capabilities**: HTTP/HTTPS requests, Modbus TCP transactions, local API calls, timer functions
- **[→ Berry Scripting Guide](../55-berry/index.md)**

### Actions

Configured HTTP or Modbus operations triggered by meter data — no scripting required. Actions provide a simpler alternative to Berry scripting for common automation tasks.

- **Best for**: Webhooks, notifications, simple Modbus commands
- **[→ Actions Guide](../50-settings/actions/index.md)**

## Choosing an Integration Method

| Need | Recommended method |
|------|-------------------|
| On-demand data reads | REST API polling |
| Continuous live updates without a broker | REST SSE streaming |
| Real-time push to IoT platform | MQTT |
| Industrial / register-based system | Modbus TCP |
| Custom on-device logic | Berry scripting |
| Simple automated HTTP/Modbus calls | Actions |

For a detailed comparison of REST and MQTT, see **[REST vs MQTT](rest-vs-mqtt.md)**.

## Supported Smart Meters

whatwatt Go supports smart meters from major manufacturers including Ensor, Iskraemeco, Kamstrup, Landis+Gyr, Meter+Control, Echelon/NES, Sagemcom, Semax/Elster, Kaifa, Siemens, and smart-me. Interfaces include P1, M-Bus, TTL/KMP, and pMEP.

See the **[homepage](../index.md#supported-smart-meters)** for the full compatibility table.

## Firmware and Feature Availability

Feature availability depends on the installed firmware version, device configuration, and applicable commercial edition:

| Feature | Introduced in |
|---------|--------------|
| REST API — system info & configuration | FW 1.2 |
| REST API — meter report polling | FW 1.2 |
| Modbus TCP slave | FW 1.2.20 |
| SSE streaming | FW 2.0 |
| Read Holding Registers (function 03) | FW 2.0.2 |
| Area-level constants, word order, detailed GET output | FW 2.0.2 |
| Berry scripting engine | FW 2.0.0 |
| `net.ip`, `11.7.0`, `energy.active`, `energy.reactive` register identifiers | FW 2.7.0 |

Check the installed firmware with:

```bash
curl http://192.168.1.100/api/v1/system
```

See **[Availability and Licensing](../20-rest/license-requirements.md)** for details on which features require specific license tiers.
