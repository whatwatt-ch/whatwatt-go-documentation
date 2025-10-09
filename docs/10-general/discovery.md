---
title: Discovery
category: concepts
tags:
- discovery
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---


# Discovery

## Document Context

- **Purpose**: Explains mDNS/DNS-SD device discovery for locating whatwatt Go devices on local networks without knowing IP addresses
- **When to use**: Network setup, device commissioning, troubleshooting connectivity, automated device detection
- **Prerequisites**: Understanding of local networks, familiarity with mDNS/Bonjour/Avahi concepts
- **Related to**: Network configuration, device setup, HTTP service access, Modbus TCP setup
- **Validates against**: Live mDNS broadcasts from whatwatt Go devices with firmware 1.2+

## Key Facts

- **Discovery protocol**: mDNS/DNS-SD (Bonjour/Avahi compatible)
- **Hostname pattern**: whatwatt-XXXXXX.local (XXXXXX = last 6 hex digits of device ID)
- **HTTP service**: _http._tcp on port 80 with Web UI instance name
- **Modbus service**: _modbus._tcp on port 502 (when enabled)
- **TXT records**: Device ID (12-hex uppercase), device type (100)
- **Service subtype**: _server for HTTP (shows as "Web Site" in browsers)
- **Network requirement**: Device and client on same local network/VLAN
- **Auto-discovery**: Enables zero-configuration device access

## Finding the device on your local network

Devices advertise themselves via mDNS/DNS‑SD.

- Hostname: `whatwatt-<XXXXXX>.local`
- Prefix `whatwatt` is lowercase, suffix `XXXXXX` is the last 6 hexadecimal UPPERCASE digits of the device ID
- HTTP service: `_http._tcp` with instance name `whatwatt Go <XXXXXX> WebUI`
- TXT records: `id=<12-hex uppercase device ID>`, `type=100`
- Subtype: `_server` (some browsers show “Web Site” badges)
- Modbus (optional): `_modbus._tcp` with instance name `ModbusTCP Slave <XXXXXX>` on configured port (default 502)

## Example result

```txt
ens38 IPv4 whatwatt Go 9F8124 WebUI Web Site local
hostname = [whatwatt-9F8124.local]
address  = [192.168.99.176]
port     = [80]
txt      = ["id=A842E39F8124" "type=100"]
```

If Modbus is enabled you may also see:

```txt
ens38 IPv4 ModbusTCP Slave 9F8124 _modbus._tcp local
hostname = [whatwatt-9F8124.local]
port     = [502]
```

## Summary

- Hostname pattern: `whatwatt-XXXXXX.local` (XXXXXX = last 6 hex digits of device ID)
- Services: `_http._tcp` (always), `_modbus._tcp` (when Modbus is enabled)
- TXT (HTTP): `id=<12-hex>`, `type=100`
- Ports: 80 (HTTP), 502 (Modbus default)
