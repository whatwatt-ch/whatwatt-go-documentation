---
title: Deploy Certificates
category: concepts
tags:
- deploy_certs
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Deploy Certificates

## Document Context

- **Purpose**: Guide for installing TLS certificates to Mosquitto MQTT broker with proper file permissions and ownership for secure communication
- **When to use**: After generating certificates, before configuring TLS listeners, when setting up production secure MQTT
- **Prerequisites**: Generated certificates (ca.crt, server.crt, server.key), Mosquitto installed, sudo access, understanding of Linux file permissions
- **Related to**: Certificate generation (tls-ca-ecc.md), TLS configuration (tls-conf.md), security hardening (hardening.md)
- **Validates against**: Mosquitto service requirements, Linux permission system, TLS certificate chain validation

## Key Facts

- **Directory**: `/etc/mosquitto/certs/` - Standard location for Mosquitto TLS certificates
- **Required files**: ca.crt (Certificate Authority), server.crt (broker certificate), server.key (broker private key)
- **Ownership**: root:mosquitto - Allows Mosquitto service to read certificates
- **Permissions**: 640 - Owner read/write, group read-only, no world access for security
- **Verification**: `ls -la` command to confirm proper installation and permissions

Install the generated certificates to the Mosquitto broker with proper permissions.

## Create Certificate Directory

```bash
sudo mkdir -p /etc/mosquitto/certs
```

## Copy Certificates

Copy the necessary certificates from your working directory:

```bash
# Copy CA certificate, server certificate, and server private key
sudo cp {ca.crt,server.crt,server.key} /etc/mosquitto/certs/
```

## Set Proper Ownership

The certificates need to be readable by the Mosquitto service:

```bash
sudo chown root:mosquitto /etc/mosquitto/certs/{*.crt,*.key}
```

## Set Secure Permissions

Restrict access to the certificates for security:

```bash
sudo chmod 640 /etc/mosquitto/certs/{*.crt,*.key}
```

## Verify Installation

Check that the files are in place with correct permissions:

```bash
ls -la /etc/mosquitto/certs/
```

You should see output similar to:

```txt
total 16
drwxr-xr-x 2 root mosquitto 4096 Oct  7 10:00 .
drwxr-xr-x 4 root root      4096 Oct  7 10:00 ..
-rw-r----- 1 root mosquitto  678 Oct  7 10:00 ca.crt
-rw-r----- 1 root mosquitto  678 Oct  7 10:00 server.crt
-rw-r----- 1 root mosquitto  227 Oct  7 10:00 server.key
```

## Certificate Files Purpose

| File                              | Purpose                                    |
|-----------------------------------|--------------------------------------------|
| `/etc/mosquitto/certs/ca.crt`    | Validates client certificates              |
| `/etc/mosquitto/certs/server.crt` | Broker's TLS certificate for clients      |
| `/etc/mosquitto/certs/server.key` | Broker's private key for TLS encryption   |

!!! note "Client Certificates"
    The client certificates (`whatwatt.crt` and `whatwatt.key`) will be uploaded directly to the whatwatt Go device via REST API, so they don't need to be placed on the broker.
