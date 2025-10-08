---
title: Wi-Fi Protected Setup (WPS)
category: concepts
tags:
- wps
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Wi-Fi Protected Setup (WPS)

## Document Context

- **Purpose**: Wi-Fi Protected Setup (WPS) API endpoint documentation for simplified wireless network pairing via button press
- **When to use**: Initial device setup, connecting to new Wi-Fi networks, avoiding manual password entry for non-technical users
- **Prerequisites**: WPS-enabled router/access point, understanding of Wi-Fi networking, device network connectivity
- **Related to**: Wi-Fi setup (wifi-setup.md), Wi-Fi scanning (wifi-scan.md), network configuration methods
- **Validates against**: WPS protocol standards, 2-minute timeout behavior, automatic station mode configuration

## Key Facts

- **Endpoint**: `/api/v1/wifi/wps` - Initiates WPS pairing process
- **Method**: POST - Starts pairing, 204 No Content on success
- **Timeout**: 2 minutes automatic pairing window
- **Modes**: Works in client, access point, or Wi-Fi disabled states
- **Security**: Convenience vs. security trade-off, consider disabling WPS after pairing

--8<-- "../_partials/auth-note.md"

!!! note "Alternative Methods"
    - WPS pairing can also be initiated by pressing the physical button on the device
    - WPS can be started from the device's WebUI

!!! warning "Connection Recommendation"
    Enabling WPS pairing over Ethernet is not recommended for optimal performance.

## What is WPS?

Wi-Fi Protected Setup (WPS) is a network security standard that facilitates the connection between a router and wireless devices. It simplifies the process of connecting to a secure wireless network by enabling users to press a physical button on the router to pair devices. The goal of WPS is to make it easier for non-technical users to connect devices to their Wi-Fi network without entering long passphrases.

## Endpoint Details

This endpoint allows you to start pairing using WPS (Wi-Fi Protected Setup).

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/wifi/wps` |
| **Method** | `POST` |
| **Response** | `204 No Content` on success |

## Pairing Process

### Supported Modes

WPS pairing works in multiple device modes:

- **Client Mode**: Device connects to existing Wi-Fi network
- **Access Point Mode**: Device acts as Wi-Fi hotspot
- **Wi-Fi Disabled**: WPS can be enabled even when Wi-Fi is turned off

### Automatic Timeout

- Pairing automatically turns off after **2 minutes** if:
  - The pairing button is not pressed on the Access Point or Router
  - There is a connection problem
  - No successful pairing occurs

### Pairing Results

#### Successful Pairing

- Automatically configures the device to operate in **station/client mode**
- Device connects to the selected Wi-Fi network
- Network credentials are saved for future use

#### Failed Pairing

- **If device was already paired**: Reverts to previous Wi-Fi settings
- **If started from access point mode**: Turns off Wi-Fi completely

## Example Request

```bash
curl -i -X POST http://192.168.1.100/api/v1/wifi/wps
```

### Expected Response

```http
HTTP/1.1 204 No Content
Content-Length: 0
```

## Usage Instructions

1. **Start WPS on Device**: Send POST request to `/api/v1/wifi/wps`
2. **Activate WPS on Router**: Press the WPS button on your router/access point
3. **Wait for Connection**: The devices will automatically pair within 2 minutes
4. **Verify Connection**: Check device Wi-Fi status to confirm successful pairing

## Troubleshooting

### Common Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Pairing timeout | Router WPS not activated | Press WPS button on router within 2 minutes |
| Connection fails | Router doesn't support WPS | Use manual Wi-Fi setup instead |
| No response | Network connectivity issues | Check device network connection |
| Reverts to previous settings | WPS authentication failed | Check router WPS settings and try again |

### Status Checking

After initiating WPS, you can check the connection status using:

```bash
# Check current Wi-Fi status
curl -s http://192.168.1.100/api/v1/system | jq '.wifi'
```

## Security Considerations

!!! warning "WPS Security"
    While WPS simplifies connection, it may have security implications:
    - Some WPS implementations have known vulnerabilities
    - Consider disabling WPS on router after pairing if not regularly used
    - Manual configuration with strong passwords is more secure

!!! tip "Best Practice"
    Use WPS for initial setup convenience, then disable it on your router for enhanced security.
