---
title: Generate ECDSA-P256 Certificate Chain
category: concepts
tags:
- tls_ca_ecc
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Generate ECDSA-P256 Certificate Chain

## Document Context

- **Purpose**: Complete guide for generating ECDSA-P256 certificate chain for secure MQTT communication with enhanced cryptographic security
- **When to use**: Setting up production-grade TLS encryption, creating certificate authority, generating server and client certificates for mutual authentication
- **Prerequisites**: OpenSSL command line knowledge, certificate management concepts, public key infrastructure (PKI) understanding, Linux file system permissions
- **Related to**: Certificate deployment, Mosquitto TLS configuration, mutual authentication setup, cryptographic security hardening
- **Validates against**: ECDSA-P256 certificate generation with verified certificate chain validation and proper key management

## Key Facts

- **Cryptography**: ECDSA with P-256 curve for enhanced security and performance
- **Certificate types**: Root CA, server certificate for broker, client certificate for device
- **Key management**: Secure private key generation and storage practices
- **Certificate validity**: Configurable validity periods (CA: 10 years, certificates: 1 year)
- **Chain validation**: OpenSSL verification tools for certificate chain integrity
- **Security features**: Self-signed CA, mutual TLS authentication support
- **File security**: Proper permissions and secure storage recommendations
- **Production readiness**: HSM integration notes for enterprise deployments

Create a complete certificate chain using elliptic curve cryptography for enhanced security and performance.

!!! tip "Working Directory"
    Work in a temporary directory, e.g. `~/mqtt-ca`, to keep certificates organized.

```bash
mkdir ~/mqtt-ca && cd ~/mqtt-ca
```

## 1. Generate Root CA

Create the Certificate Authority that will sign both server and client certificates:

```bash
# Generate CA private key
openssl ecparam -name prime256v1 -genkey -noout -out ca.key

# Generate self-signed CA certificate
openssl req -x509 -new -key ca.key -sha256 -days 3650 \
  -subj "/C=US/O=Lab/OU=IoT/CN=Lab ECC Root CA" \
  -out ca.crt
```

## 2. Generate Mosquitto Server Certificate

Create the server certificate for the MQTT broker:

```bash
# Generate server private key
openssl ecparam -name prime256v1 -genkey -noout -out server.key

# Generate certificate signing request
openssl req -new -key server.key \
  -subj "/C=US/O=Lab/OU=IoT/CN=mqtt.lab.local" \
  -out server.csr

# Sign the server certificate with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -sha256 -days 365 -out server.crt
```

## 3. Generate Client Certificate for WhatWatt Go

Create the client certificate for device authentication:

```bash
# Generate client private key
openssl ecparam -name prime256v1 -genkey -noout -out whatwatt.key

# Generate certificate signing request
openssl req -new -key whatwatt.key \
  -subj "/C=US/O=Lab/OU=Metering/CN=whatwatt-001" \
  -out whatwatt.csr

# Sign the client certificate with CA
openssl x509 -req -in whatwatt.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -sha256 -days 365 -out whatwatt.crt
```

## 4. Verify Generated Certificates

Check the certificate details:

```bash
# View CA certificate
openssl x509 -in ca.crt -text -noout

# View server certificate
openssl x509 -in server.crt -text -noout

# View client certificate
openssl x509 -in whatwatt.crt -text -noout

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt
openssl verify -CAfile ca.crt whatwatt.crt
```

## Generated Files

After completion, you should have:

| File            | Description                    | Usage                              |
|-----------------|--------------------------------|------------------------------------|
| `ca.crt`        | Root CA certificate            | Broker & client certificate validation |
| `ca.key`        | Root CA private key            | Signing certificates (keep secure!)  |
| `server.crt`    | Mosquitto server certificate   | Broker TLS identity               |
| `server.key`    | Mosquitto server private key   | Broker TLS encryption             |
| `whatwatt.crt`  | Client certificate             | Device mutual TLS authentication   |
| `whatwatt.key`  | Client private key             | Device TLS encryption             |

!!! warning "Security"
    - Keep private keys (`*.key`) secure and with restricted permissions
    - The CA private key should be stored safely offline after use
    - Consider using hardware security modules (HSMs) for production CA keys
