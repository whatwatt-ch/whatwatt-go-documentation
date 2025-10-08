---
title: Secure MQTT Integration
category: concepts
tags:
- index
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Secure MQTT Integration

## Document Context

- **Purpose**: Complete guide for implementing secure MQTT integration with WhatWatt Go using TLS encryption, mutual authentication, and certificate-based security
- **When to use**: Production deployments requiring encrypted communication, enterprise security requirements, regulated environments, sensitive data protection
- **Prerequisites**: Linux system administration, certificate management, MQTT broker configuration, network security concepts, OpenSSL command usage
- **Related to**: Certificate generation, Mosquitto broker setup, TLS configuration, device provisioning, production security hardening
- **Validates against**: Complete secure MQTT workflow with real WhatWatt Go device and Mosquitto 2.0.21+ broker setup

## Key Facts

- **Security level**: Mutual TLS authentication with ECDSA-P256 certificates
- **Broker requirements**: Mosquitto 2.0.21+ with TLS support enabled
- **Certificate types**: CA root, server certificate, client certificate for device
- **Authentication method**: Certificate-based mutual authentication (no username/password)
- **Encryption**: TLS 1.2+ with strong cipher suites
- **Network validation**: IP address-based (hostname validation disabled for flexibility)
- **File permissions**: Strict certificate file permissions for security
- **Production ready**: Includes hardening recommendations and security best practices

## Scope

This chapter shows how to connect a WhatWatt Go device to a local Mosquitto 2.0.21 broker using ECDSA certificates, mutual-TLS, and IP addresses (no hostname validation). All certificates are stored in `/etc/mosquitto/certs/`. Optional production-grade notes are included at the end.

## Prerequisites

| Component     | Version / Notes                     |
| ------------- | ----------------------------------- |
| Ubuntu/Debian | fresh install, sudo user            |
| Mosquitto     | 2.0.21+ (apt repo)                  |
| OpenSSL       | 3.x (included)                      |
| WhatWatt Go   | firmware ≥ 1.7.6, REST API enabled |
| Python        | ≥ 3.8 (for provisioning script)     |

## Overview

The secure MQTT setup involves:

1. **Install Mosquitto** - MQTT broker with TLS support
2. **Generate certificates** - ECDSA-P256 certificate chain (CA, server, client)
3. **Deploy certificates** - Install certificates with proper permissions
4. **Configure Mosquitto** - Enable TLS listener with mutual authentication
5. **Test connection** - Verify setup with command line tools
6. **Provision device** - Configure WhatWatt Go via REST API
7. **Hardening** - Production security recommendations

!!! warning "Security Note"
    This setup uses mutual TLS authentication for maximum security. Both the broker verifies the client certificate, and the client can verify the broker certificate.
