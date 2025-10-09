---
title: Install Mosquitto & Clients
category: concepts
tags:
- install_mosquitto
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Install Mosquitto & Clients

## Document Context

- **Purpose**: Step-by-step installation guide for Mosquitto MQTT broker with TLS support and client tools for secure MQTT communication testing
- **When to use**: Initial setup of secure MQTT infrastructure, preparing broker environment for whatwatt Go integration, development environment setup
- **Prerequisites**: Ubuntu/Debian Linux system with sudo privileges, basic Linux package management knowledge, systemd service management
- **Related to**: TLS certificate generation, broker configuration, secure MQTT client testing, service verification
- **Validates against**: Mosquitto 2.0.21+ installation with verified service status and client tool availability

## Key Facts

- **Package requirements**: mosquitto, mosquitto-clients, openssl packages
- **Installation method**: APT package manager on Ubuntu/Debian systems
- **Service management**: Systemd automatic startup and service control
- **TLS support**: OpenSSL integration for certificate operations
- **Client tools**: mosquitto_pub, mosquitto_sub for testing and debugging
- **Service verification**: systemctl status validation for proper installation
- **Default configuration**: Basic MQTT broker without security (pre-TLS setup)
- **Next steps**: Certificate generation and TLS configuration required for security

Install Mosquitto MQTT broker with TLS support and client tools for testing.

## Installation

```bash
sudo apt update
sudo apt install --yes mosquitto mosquitto-clients openssl
```

## Verify Installation

Mosquitto starts automatically after installation. Verify the service is running:

```bash
systemctl status mosquitto
```

You should see output indicating the service is active and running:

```txt
● mosquitto.service - Mosquitto MQTT Broker
     Loaded: loaded (/lib/systemd/system/mosquitto.service; enabled; vendor preset: enabled)
     Active: active (running) since...
```

## Default Configuration

By default, Mosquitto runs on port 1883 without authentication or encryption. We'll configure TLS and mutual authentication in the following steps.

!!! note "Service Management"
    - Start: `sudo systemctl start mosquitto`
    - Stop: `sudo systemctl stop mosquitto`
    - Restart: `sudo systemctl restart mosquitto`
    - Check logs: `journalctl -u mosquitto -f`
