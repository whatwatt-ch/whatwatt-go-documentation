---
title: Wi-Fi Network Scan
category: concepts
tags:
- wifi_scan
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Wi-Fi Network Scan

## Document Context

- **Purpose**: Wi-Fi network discovery API endpoint for scanning nearby wireless networks with detailed signal and security information
- **When to use**: Before configuring Wi-Fi settings, troubleshooting connectivity, site surveys, selecting optimal networks
- **Prerequisites**: Device with Wi-Fi capability, understanding of Wi-Fi standards and security modes
- **Related to**: Wi-Fi setup (wifi-setup.md), WPS pairing (wps.md), network configuration settings
- **Validates against**: IEEE 802.11 standards, WPA/WPA2/WPA3 security modes, regulatory domain compliance

## Key Facts

- **Endpoint**: `/api/v1/wifi/scan` - Discovers nearby Wi-Fi networks
- **Method**: GET - Returns JSON array of detected networks
- **Signal measurement**: RSSI (-127 to 0 dBm) and signal percentage (0-100%)
- **Security info**: Authentication modes, cipher types, WPS support
- **Network details**: SSID, BSSID, channel, PHY standards, country codes

--8<-- "../_partials/auth-note.md"

!!! warning "Connection Recommendation"
    Scanning Wi-Fi networks over Ethernet is not recommended for optimal performance.

!!! note "Alternative Method"
    Wi-Fi scanning can also be performed from the device's WebUI.

## Endpoint Details

This endpoint allows you to search for nearby Wi-Fi networks.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/wifi/scan` |
| **Method** | `GET` |
| **Response Content Type** | `application/json` |

## Example Request

=== "No auth"
    ```bash
    curl -s http://192.168.1.100/api/v1/wifi/scan
    ```

=== "With password"
    ```bash
    curl -s --anyauth -u ":PASSWORD" http://192.168.1.100/api/v1/wifi/scan
    ```

## Response Format

The endpoint returns an array of detected Wi-Fi networks with detailed information about each network.

### Network Fields

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `ssid` | string | 1..32 | Network name (Service Set Identifier) - the identifier that devices use to connect to the correct wireless network |
| `bssid` | string | 12 hex chars | MAC address of the access point (Basic Service Set Identifier) - uniquely identifies each access point |
| `channel` | uint | 1..13 | Wi-Fi channel - specific frequency range within a Wi-Fi band used for communication |
| `ht` | string | 20, 40+, 40- | High Throughput mode from 802.11n standard using MIMO technology |
| `rssi` | int | -127..0 | Received Signal Strength Indicator in dBm (closer to zero = stronger signal) |
| `signal` | uint | 0..100 | Wi-Fi signal strength as percentage |
| `auth_mode` | string | Various | Authentication mode (open, WEP, WPA, WPA2, WPA3, etc.) |
| `pairwise_cipher` | string | Various | Encryption method for unicast communication between device and access point |
| `group_cipher` | string | Various | Encryption method for multicast and broadcast communications |
| `phy` | string | bgn | Physical layer standards supported |
| `wps` | string | true/false | Wi-Fi Protected Setup support |
| `country` | string | 2 chars | Country code determining regulatory domain for the device |

### Authentication Modes

| Mode | Description |
|------|-------------|
| `open` | No authentication required |
| `WEP` | Wired Equivalent Privacy (legacy, not secure) |
| `WPA` | Wi-Fi Protected Access |
| `WPA2` | Wi-Fi Protected Access 2 |
| `WPA-WPA2` | Mixed WPA/WPA2 mode |
| `EAP` | Extensible Authentication Protocol |
| `WPA3` | Wi-Fi Protected Access 3 (latest) |
| `WPA2-WPA3` | Mixed WPA2/WPA3 mode |
| `WPA3-ENT` | WPA3 Enterprise |

### Group Cipher Types

| Cipher | Description |
|--------|-------------|
| `none` | No encryption |
| `WEP40`/`WEP104` | WEP with 40/104-bit keys |
| `TKIP` | Temporal Key Integrity Protocol |
| `CCMP` | Counter Mode with CBC-MAC Protocol |
| `AES-CMAC-128` | AES Cipher-based MAC |
| `GCMP`/`GCMP256` | Galois/Counter Mode Protocol |
| `SMS4` | Chinese national standard |

## Example Response

```json
[
  {
    "ssid": "HomeNetwork",
    "bssid": "AA:BB:CC:DD:EE:FF",
    "channel": 6,
    "ht": "40+",
    "rssi": -45,
    "signal": 85,
    "auth_mode": "WPA2-WPA3",
    "pairwise_cipher": "CCMP",
    "group_cipher": "CCMP",
    "phy": "bgn",
    "wps": "true",
    "country": "US"
  },
  {
    "ssid": "GuestWiFi",
    "bssid": "11:22:33:44:55:66",
    "channel": 11,
    "ht": "20",
    "rssi": -67,
    "signal": 45,
    "auth_mode": "open",
    "pairwise_cipher": "none",
    "group_cipher": "none",
    "phy": "bgn",
    "wps": "false",
    "country": "US"
  }
]
```

## Signal Strength Guidelines

| RSSI (dBm) | Signal Quality | Typical Performance |
|------------|----------------|-------------------|
| -30 to 0 | Excellent | Maximum performance |
| -50 to -30 | Very Good | Very reliable connection |
| -60 to -50 | Good | Reliable for most uses |
| -70 to -60 | Fair | May experience some issues |
| -80 to -70 | Poor | Unreliable connection |
| -90 to -80 | Very Poor | Minimal connectivity |
| Below -90 | No Signal | Connection not possible |

Use this endpoint to discover available networks before configuring Wi-Fi settings through the `/api/v1/settings` endpoint.
