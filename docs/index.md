---
title: whatwatt Go API Documentation
category: concepts
tags:
- index
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# whatwatt Go API Documentation

## Document Context

- **Purpose**: Comprehensive introduction and navigation hub for whatwatt Go API documentation and integration guides
- **When to use**: Starting point for new users, overview of all available integration methods, reference for documentation structure
- **Prerequisites**: Basic understanding of energy monitoring concepts; familiarity with REST APIs or MQTT helpful but not required
- **Related to**: All documentation sections - serves as central navigation point to specific integration guides
- **Validates against**: Real device examples from Swiss Smart Meter installations

## Key Facts

- **Device Type**: Swiss Smart Meter integration device with REST API and MQTT support
- **Compatibility**: Universal support for all Swiss Smart Meter manufacturers (Ensor, Iskraemeco, Kamstrup, Landis+Gyr, etc.)
- **Protocols**: REST API (HTTP/JSON), MQTT, Secure MQTT (TLS)
- **License model**: Core configuration is available on all editions; selected data and automation integrations require Plus or higher
- **Data Formats**: JSON responses, Server-Sent Events (SSE), CSV logging
- **Authentication**: Optional HTTP authentication when device password is set (Digest auth from firmware 1.10.X, Basic auth in earlier versions)
- **Network**: Wi-Fi and Ethernet connectivity, mDNS discovery support
- **Data Ownership**: Local device - your data stays under your control
- **Real-time Capability**: Instant energy consumption monitoring and streaming

Welcome to the comprehensive API documentation for **whatwatt Go** - the Swiss Smart Meter integration device.

## What is whatwatt Go?

whatwatt Go is a cutting-edge device that connects to any Swiss Smart Meter, enabling real-time energy consumption monitoring and data access through REST API and MQTT protocols. Made for Switzerland and Europe, it empowers users to optimize their energy consumption through instant, real-time data access.

## Key Features

- 🔌 **Universal Compatibility**: Works with all current Smart Meters from major manufacturers (Ensor, Iskraemeco, Kamstrup, Landis+Gyr, Sagemcom, Semax, NES, and Meter+Control)
- ⚡ **Real-Time Data**: Instant access to energy consumption data
- 🌐 **Multiple Protocols**: REST API and MQTT support
- 🔐 **Secure Communication**: TLS/SSL encryption support
- 📊 **Rich Data Format**: JSON responses with detailed meter information
- 🏠 **Local Control**: Your data stays with you - no cloud dependency

## Quick Start

Choose your integration method:

=== "REST API"

    Perfect for web applications and simple polling scenarios.

    ```bash
    # Check device availability and license type
    curl http://192.168.1.100/api/v1/system
    ```

    If `.device.license.type` is `PLUS` or higher, you can continue with meter polling endpoints such as `/api/v1/report`.

    **[→ REST API Guide](00-intro/first-request.md)**

=== "MQTT"

    Ideal for real-time applications and IoT integration.

  Requires an active Plus or higher license for the built-in MQTT publisher.

    ```bash
    # Subscribe on YOUR MQTT BROKER to the topic you configured in Device Settings → MQTT (publish.topic)
    # Example: broker on localhost, topic prefix 'lab/energy/'
    mosquitto_sub -h 127.0.0.1 -t "lab/energy/#" -v

    # If your broker requires username/password authentication
    # mosquitto_sub -h 127.0.0.1 -u USER -P PASS -t "lab/energy/#" -v
    ```

    **[→ MQTT Guide](30-mqtt/index.md)**

=== "Secure MQTT"

    Enterprise-grade security with TLS encryption.

  Requires an active Plus or higher license because it uses the same built-in MQTT publisher.

    ```bash
    # Connect to YOUR MQTT BROKER with TLS (mutual TLS optional)
    mosquitto_sub -h 127.0.0.1 -p 8883 -v \
      --cafile ca.crt --cert client.crt --key client.key \
      -t "lab/energy/#"
    ```

    **[→ Secure MQTT Setup](40-secure-mqtt/index.md)**

## Documentation Structure

This documentation covers everything you need to integrate with whatwatt Go:

### 🚀 Getting Started

- **[Overview](00-intro/overview.md)** - Introduction to whatwatt Go
- **[REST vs MQTT](00-intro/rest-vs-mqtt.md)** - Choose the right integration method

### 🔧 Device Information

- **[Power & Wi-Fi Requirements](10-general/power-and-wifi.md)** - Setup requirements
- **[Device Discovery](10-general/discovery.md)** - Find your device on the network
- **[System Information](10-general/system-info.md)** - Device status and configuration

### 📡 Integration Methods

- **[REST API](20-rest/polling.md)** - HTTP-based data access
- **[MQTT](30-mqtt/index.md)** - Real-time messaging protocol
- **[Secure MQTT](40-secure-mqtt/index.md)** - TLS-encrypted communication

### ⚙️ Configuration

- **[Device Settings](50-settings/rest-conventions.md)** - Complete configuration reference
- **[Wi-Fi Setup](50-settings/wifi-setup.md)** - Network configuration
- **[Actions](50-settings/actions/index.md)** - Automated HTTP/Modbus requests

### 📚 Reference

- **[HTTP Basics](90-appendix/http-basics.md)** - Understanding HTTP methods and responses
- **[curl Examples](90-appendix/curl-options.md)** - Command-line usage examples
- **[OBIS Codes](90-appendix/appendix-d.md)** - Energy measurement standards

## Energy Transition

> The Energy Transition will only succeed if we can optimize our own energy consumption. This is only possible if we know our consumption in real time and can react accordingly.

The Swiss Federal Regulation concerning electricity supply stipulates that Smart Meters must be equipped with an interface that allows retrieving measured data in real time. **whatwatt Go uses this interface to give you control over your energy data.**

## Data Ownership

**Who owns your energy consumption data?** The consumption data collected from your household belongs to **you**. You decide with whom you would like to share this data. whatwatt Go ensures your data stays local and under your control.

---

<div style="text-align: center; margin: 2rem 0;">
  <a href="00-intro/overview" class="md-button md-button--primary">
    Get Started
  </a>
  <a href="https://whatwatt.ch" class="md-button" target="_blank">
    Learn More
  </a>
</div>

!!! info "Need Help?"
    - 📧 **Support**: Visit [whatwatt.ch/en/contact](https://whatwatt.ch/en/contact)
    - 📖 **FAQ**: Check [whatwatt.ch/en/faq-and-support](https://whatwatt.ch/en/faq-and-support)
    - 🛒 **Purchase**: Available at [whatwatt.ch/en/shop](https://whatwatt.ch/en/shop)
