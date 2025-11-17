---
title: Ethernet Configuration
category: concepts
tags:
- ethernet
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Ethernet Configuration

## Document Context

- **Purpose**: Ethernet network configuration API for managing wired connectivity including DHCP and static IP settings
- **When to use**: Setting up wired network connectivity, configuring static IP addresses, troubleshooting network issues, deployment planning
- **Prerequisites**: Basic networking knowledge (IP addresses, subnet masks, gateways), understanding of DHCP vs static IP concepts
- **Related to**: [Wi-Fi setup](wifi-setup.md), [Network discovery](../10-general/discovery.md), device settings configuration
- **Validates against**: IPv4 network configuration standards, DHCP client behavior, static IP validation requirements

## Key Facts

- **Endpoint**: `/api/v1/eth/settings` - Ethernet network configuration management
- **Methods**: GET (read), POST (overwrite), PUT (update) - Full configuration control
- **Network modes**: DHCP automatic assignment or static IP with manual configuration
- **Required fields**: IP, netmask, gateway, DNS when using static IP configuration
- **Default state**: Ethernet enabled with DHCP (static_ip: false)

--8<-- "../_partials/auth-note.md"

!!! note "Alternative Method"
    Ethernet settings can also be configured from the device's WebUI.

## Endpoint Details

This endpoint allows you to configure the Ethernet connection settings including static IP configuration and DHCP options.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/api/v1/eth/settings` |
| **Methods** | `GET`, `POST`, `PUT` |
| **Response Content Type** | `application/json` |

## Configuration Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enable` | boolean | `true` | Enable/disable Ethernet port |
| `static_ip` | boolean | `false` | Use static IP instead of DHCP client |
| `ip` | string | `"0.0.0.0"` | Static IP address (IPv4 format) |
| `netmask` | string | `"0.0.0.0"` | Subnet mask (IPv4 format) |
| `gateway` | string | `"0.0.0.0"` | Gateway address (IPv4 format) |
| `dns` | string | `"0.0.0.0"` | DNS server address (IPv4 format) |

## Network Configuration Types

### DHCP Configuration (Automatic)

Most home and office networks use DHCP for automatic IP assignment:

```json
{
  "enable": true,
  "static_ip": false,
  "ip": "0.0.0.0",
  "netmask": "0.0.0.0",
  "gateway": "0.0.0.0",
  "dns": "0.0.0.0"
}
```

### Static IP Configuration

For networks requiring fixed IP addresses:

```json
{
  "enable": true,
  "static_ip": true,
  "ip": "192.168.1.201",
  "netmask": "255.255.255.0",
  "gateway": "192.168.1.1",
  "dns": "8.8.8.8"
}
```

## Examples

### Get Current Configuration

=== "No auth"
    ```bash
    curl -s http://192.168.1.100/api/v1/eth/settings
    ```

=== "With password"
    ```bash
    curl -s --anyauth -u ":PASSWORD" http://192.168.1.100/api/v1/eth/settings
    ```

**Response:**

```json
{
  "enable": true,
  "static_ip": false,
  "ip": "0.0.0.0",
  "netmask": "0.0.0.0",
  "gateway": "0.0.0.0",
  "dns": "0.0.0.0"
}
```

### Enable Ethernet with DHCP

```bash
curl -X PUT -H "Content-Type: application/json" \
     -d '{
       "enable": true,
       "static_ip": false
     }' \
     http://192.168.1.100/api/v1/eth/settings
```

### Configure Static IP

```bash
curl -X PUT -H "Content-Type: application/json" \
     -d '{
       "enable": true,
       "static_ip": true,
       "ip": "192.168.1.201",
       "netmask": "255.255.255.0",
       "gateway": "192.168.1.1",
       "dns": "8.8.8.8"
     }' \
     http://192.168.1.100/api/v1/eth/settings
```

### Disable Ethernet

```bash
curl -X PUT -H "Content-Type: application/json" \
     -d '{"enable": false}' \
     http://192.168.1.100/api/v1/eth/settings
```

## Static IP Guidelines

### Address Assignment

!!! warning "Address Conflicts"
    When setting static addressing, address collision can occur. Ensure no other device uses the same IP address.

**Safe Static IP Ranges:**

- **Below DHCP range**: `192.168.1.2` - `192.168.1.99` (if DHCP uses 100-200)
- **Above DHCP range**: `192.168.1.201` - `192.168.1.254` (if DHCP uses 100-200)
- **Check router settings**: Verify DHCP range in router configuration

### Common Network Configurations

#### Home Network (192.168.1.x)

```json
{
  "enable": true,
  "static_ip": true,
  "ip": "192.168.1.201",
  "netmask": "255.255.255.0",
  "gateway": "192.168.1.1",
  "dns": "8.8.8.8"
}
```

#### Office Network (192.168.0.x)

```json
{
  "enable": true,
  "static_ip": true,
  "ip": "192.168.0.150",
  "netmask": "255.255.255.0",
  "gateway": "192.168.0.1",
  "dns": "192.168.0.1"
}
```

#### Corporate Network (10.0.x.x)

```json
{
  "enable": true,
  "static_ip": true,
  "ip": "10.0.1.100",
  "netmask": "255.255.0.0",
  "gateway": "10.0.1.1",
  "dns": "10.0.1.1"
}
```

## Field Requirements

### Static IP Requirements

When `static_ip: true`, the following fields **must** be set to non-zero values:

| Field | Requirement | Example |
|-------|-------------|---------|
| `ip` | Device IP address | `"192.168.1.201"` |
| `netmask` | Subnet mask | `"255.255.255.0"` |
| `gateway` | Router/gateway IP | `"192.168.1.1"` |
| `dns` | DNS server IP | `"8.8.8.8"` or `"192.168.1.1"` |

### DNS Configuration Options

| DNS Setting | Use Case | Example |
|-------------|----------|---------|
| `"8.8.8.8"` | Google DNS (external) | Reliable public DNS |
| `"1.1.1.1"` | Cloudflare DNS (external) | Fast public DNS |
| `"192.168.1.1"` | Router DNS (local) | Use router for DNS resolution |
| Custom DNS | Corporate networks | Internal DNS servers |

## Troubleshooting

### Connection Issues

```bash
# Test connectivity after configuration change

ping -c 3 192.168.1.201

# Check if IP is reachable
curl -s http://192.168.1.201/api/v1/system

# Verify no IP conflicts
nmap -sP 192.168.1.201
```

### Configuration Validation

```bash
# Verify settings were applied
curl -s http://192.168.1.100/api/v1/eth/settings | jq '.'

# Check system network status
curl -s http://192.168.1.100/api/v1/system | jq '.ethernet'
```

### Common Problems

| Issue | Cause | Solution |
|-------|-------|---------|
| Cannot access device | IP conflict | Check for duplicate IPs on network |
| No internet access | Wrong gateway/DNS | Verify gateway and DNS settings |
| Configuration rejected | Invalid IP format | Use proper IPv4 format (x.x.x.x) |
| Settings not persistent | Configuration not saved | Use PUT/POST method, not GET |

## Best Practices

!!! tip "Network Planning"
    - Document IP assignments to avoid conflicts
    - Use consistent IP ranges for static devices
    - Test configuration before applying to production

!!! warning "Backup Access"
    - Keep Wi-Fi enabled as backup connection method
    - Note current IP before making changes
    - Have physical access available if needed

!!! info "Performance"
    - Ethernet typically provides more stable connection than Wi-Fi
    - Consider cable quality and length for reliable connections
    - Use static IP for servers and automation systems
