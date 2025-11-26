---
title: Wi-Fi Network Setup
category: api-endpoints
tags:
- wifi
- network-setup
- station-mode
- connectivity
- wireless
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /api/v1/wifi/sta/settings
protocols:
- HTTP
- REST
related_concepts:
- wireless networking
- station mode
- dhcp
- static ip
- network configuration
use_cases:
- device connectivity
- network setup
- wifi configuration
- remote deployment
real_device_tested: true
authentication: required when device password is set
methods:
- GET
- POST
- PUT
- DELETE
---

# Wi-Fi Network Setup

## Document Context

- **Purpose**: Configure device Wi-Fi connectivity to join existing wireless networks
- **When to use**: For wireless deployment, network connectivity setup, or changing wireless networks
- **Prerequisites**: Knowledge of target network credentials; understanding of static vs DHCP IP assignment
- **Related to**: Network connectivity, device deployment, remote access setup
- **Validates against**: Real Wi-Fi configuration on whatwatt Go devices

## Key Facts

- **Endpoint**: `/api/v1/wifi/sta/settings`
- **Methods**: GET, POST, PUT, DELETE
- **Authentication**: Required when device Web UI password is set
- **Station mode**: Connects to existing Wi-Fi networks (not access point mode)
- **IP assignment**: Supports both DHCP and static IP configuration
- **DELETE action**: Removes Wi-Fi config and disables client
- **Power control**: Configurable transmission power (0-21 dBm)
- **Network types**: Supports open and secured networks (WPA/WPA2/WPA3)

## Endpoint Details

Configure Wi-Fi connection settings for station mode (connecting to existing network).

| Endpoint              | `api/v1/wifi/sta/settings` |
| --------------------- | -------------------------- |
| Method                | GET, POST, PUT, DELETE     |
| Response content type | application/json           |

--8<-- "../_partials/auth-note.md"

## Configuration Fields

| Field        | Type    | Default      | Range  | Description                                          |
| ------------ | ------- | ------------ | ------ | ---------------------------------------------------- |
| `.enable`    | boolean | false        |        | Enable Wi-Fi station mode                           |
| `.name`      | string  | empty string | 1..32  | Wi-Fi network name (SSID) to connect to             |
| `.password`  | string  | empty string | 8..64  | Wi-Fi password (optional for open networks)         |
| `.static_ip` | boolean | false        |        | Use static IP instead of DHCP                       |
| `.ip`        | string  | 0.0.0.0      |        | Static IP address (if static_ip enabled)            |
| `.netmask`   | string  | 0.0.0.0      |        | Network mask (if static_ip enabled)                 |
| `.gateway`   | string  | 0.0.0.0      |        | Gateway address (if static_ip enabled)              |
| `.dns`       | string  | 0.0.0.0      |        | DNS server address (if static_ip enabled)           |
| `.max_tx_power` | float   | 17           | 0..21  | Wi-Fi transmission power in dBm (resolution: 0.5)   |

## Example Request

=== "No auth"
    ```bash
    curl http://whatwatt-ABCDEF.local/api/v1/wifi/sta/settings
    ```

=== "With password"
    ```bash
    curl --anyauth -u ":PASSWORD" http://whatwatt-ABCDEF.local/api/v1/wifi/sta/settings
    ```

## Example Response

```json
{
  "enable": true,
  "name": "sjj",
  "static_ip": false,
  "ip": "0.0.0.0",
  "netmask": "0.0.0.0",
  "gateway": "0.0.0.0",
  "dns": "0.0.0.0",
  "max_tx_power": 17
}
```

## Configuration Examples

### Basic Wi-Fi Connection (DHCP)

```json
{
  "enable": true,
  "name": "MyWiFiNetwork",
  "password": "MySecurePassword123"
}
```

### Static IP Configuration

```json
{
  "enable": true,
  "name": "MyWiFiNetwork",
  "password": "MySecurePassword123",
  "static_ip": true,
  "ip": "192.168.1.100",
  "netmask": "255.255.255.0",
  "gateway": "192.168.1.1",
  "dns": "8.8.8.8"
}
```

### Open Network (No Password)

```json
{
  "enable": true,
  "name": "OpenWiFi"
}
```

### Low Power Configuration

```json
{
  "enable": true,
  "name": "MyWiFiNetwork",
  "password": "MySecurePassword123",
  "max_tx_power": 10
}
```

## Delete Configuration

Use DELETE method to erase Wi-Fi configuration and shutdown the client:

=== "DELETE (no auth)"
    ```bash
    curl -X DELETE http://whatwatt-ABCDEF.local/api/v1/wifi/sta/settings
    ```

=== "DELETE (with password)"
    ```bash
    curl -X DELETE --anyauth -u ":PASSWORD" http://whatwatt-ABCDEF.local/api/v1/wifi/sta/settings
    ```

## Static IP Guidelines

When using static IP configuration:

### IP Address Ranges

- **Avoid DHCP range**: Most routers use 192.168.X.100-200 for DHCP
- **Safe static ranges**: 192.168.X.2-99 or 192.168.X.201-254
- **Check conflicts**: Ensure no other device uses the same IP

### Required Fields for Static IP

All of these must be set when `static_ip: true`:

- `ip` - Device IP address
- `netmask` - Usually `255.255.255.0`
- `gateway` - Router IP (usually `192.168.X.1`)
- `dns` - DNS server (can use `8.8.8.8` or router IP)

## Power Considerations

### Transmission Power (`max_tx_power`)

- **Default**: 17 dBm (recommended for most situations)
- **Low power**: Reduce to 10-15 dBm when powered via M-Bus only
- **High power**: Increase to 20 dBm for better range (if sufficient power available)
- **Resolution**: 0.5 dBm steps

!!! warning "Power Supply"
    When powered only via M-Bus interface, high transmission power may cause system instability. Monitor `.device.plug.v_scap` voltage and reduce power if voltage drops below 4.5V.

!!! note "Password Format"
    - **Standard**: 8-64 character password
    - **Hexadecimal**: 64 hexadecimal characters for advanced use
    - **Open networks**: Leave password empty
