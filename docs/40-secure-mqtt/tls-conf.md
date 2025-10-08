---
title: Mosquitto TLS Configuration
category: concepts
tags:
- tls_conf
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Mosquitto TLS Configuration

## Document Context

- **Purpose**: Step-by-step guide for configuring Mosquitto MQTT broker with TLS encryption and mutual authentication for secure device communication
- **When to use**: Configuring production MQTT broker security, implementing mutual TLS authentication, securing IoT device communications
- **Prerequisites**: Mosquitto installed, certificates generated and deployed, basic understanding of TLS/SSL configuration, Linux system administration
- **Related to**: Certificate deployment, mutual authentication setup, MQTT broker security, TLS listener configuration
- **Validates against**: Mosquitto TLS configuration with mutual authentication and secure cipher negotiation

## Key Facts

- **TLS port**: 8883 (standard secure MQTT port)
- **Authentication method**: Mutual TLS with client certificate validation
- **Certificate requirements**: CA file, server certificate, server private key
- **Security features**: Certificate-based identity, no anonymous connections
- **Protocol support**: MQTT over TLS (not WebSockets)
- **TLS versions**: Auto-negotiated (TLS 1.3 preferred)
- **Identity mapping**: Certificate Common Name used as username
- **Configuration location**: /etc/mosquitto/conf.d/tls.conf

Configure Mosquitto to use TLS with mutual authentication.

## Create TLS Configuration File

Create `/etc/mosquitto/conf.d/tls.conf`:

```bash
sudo nano /etc/mosquitto/conf.d/tls.conf
```

Add the following configuration:

```conf
# TLS listener on port 8883
listener 8883
protocol mqtt

# Certificate files
cafile /etc/mosquitto/certs/ca.crt
certfile /etc/mosquitto/certs/server.crt
keyfile /etc/mosquitto/certs/server.key

# Mutual TLS authentication
require_certificate true
use_identity_as_username true
allow_anonymous false

# TLS version and ciphers are auto-negotiated (TLS 1.3 preferred)
```

## Configuration Explanation

| Setting                    | Purpose                                        |
|----------------------------|------------------------------------------------|
| `listener 8883`            | Listen on port 8883 for TLS connections       |
| `protocol mqtt`            | Use MQTT protocol (not WebSockets)            |
| `cafile`                   | CA certificate to validate client certificates |
| `certfile`                 | Server certificate for TLS                     |
| `keyfile`                  | Server private key for TLS                     |
| `require_certificate true` | Client must present a valid certificate        |
| `use_identity_as_username true` | Use certificate CN as username            |
| `allow_anonymous false`    | Disable anonymous connections                  |

## Apply Configuration

Restart Mosquitto to load the new configuration:

```bash
sudo systemctl restart mosquitto
```

## Verify Configuration

Check that Mosquitto is running and listening on port 8883:

```bash
sudo netstat -tlnp | grep :8883
```

Monitor the logs for any errors:

```bash
journalctl -u mosquitto -f
```

You should see logs indicating that the TLS listener is active:

```txt
mosquitto[1234]: Opening ipv4 listen socket on port 8883.
mosquitto[1234]: Opening ipv6 listen socket on port 8883.
```

!!! warning "Firewall"
    Ensure port 8883 is open in your firewall if connections come from remote hosts:
    ```bash
    sudo ufw allow 8883/tcp
    ```

!!! note "Security"
    - TLS 1.3 is preferred and auto-negotiated
    - Only secure cipher suites are used by default
    - The broker will reject connections without valid client certificates
