---
title: Production Hardening
category: concepts
tags:
- hardening
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Production Hardening

## Document Context

- **Purpose**: Production security hardening guide for MQTT broker deployments with certificate management, network security, and monitoring best practices
- **When to use**: When deploying secure MQTT in production environments, implementing security policies, preparing for compliance audits
- **Prerequisites**: Functional secure MQTT setup, understanding of PKI, network security concepts, Linux system administration
- **Related to**: Certificate deployment (deploy-certs.md), TLS configuration (tls-conf.md), certificate generation (tls-ca-ecc.md)
- **Validates against**: Security best practices, compliance requirements, production network constraints

## Key Facts

- **Hostname validation**: Use Subject Alternative Names (SAN) instead of skip_cn_check for production
- **Certificate rotation**: 90-day validity recommended with 30-day renewal warnings
- **Network isolation**: Firewall rules, VLAN separation, restricted IP ranges for broker access
- **Access control**: Topic-based ACLs, unique certificates per device, granular permissions
- **Monitoring**: Enhanced logging, log rotation, certificate expiration tracking

Security recommendations for production MQTT deployments.

## Hostname Validation

For production use, enable proper hostname validation instead of skipping CN checks.

### 1. Issue Server Certificate with SAN

When generating the server certificate, include Subject Alternative Names:

```bash
# Create a config file for SAN
cat > server.conf << EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req

[req_distinguished_name]

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = broker.example.com
DNS.2 = mqtt.example.com
IP.1 = 192.168.99.186
EOF

# Generate certificate with SAN
openssl req -new -key server.key -config server.conf \
  -subj "/C=US/O=Lab/OU=IoT/CN=broker.example.com" \
  -out server.csr

openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -sha256 -days 365 -extensions v3_req \
  -extfile server.conf -out server.crt
```

### 2. Remove skip_cn_check

Configure devices without hostname skipping:

```json
{
  "enable": true,
  "url": "mqtts://broker.example.com:8883",
  "skip_cn_check": false,
  "client_id": "whatwatt-001"
}
```

## Certificate Management

### Unique Client Certificates

Issue individual certificates for each device:

```bash
# Per-device certificate generation
for device in device-001 device-002 device-003; do
  openssl ecparam -name prime256v1 -genkey -noout -out ${device}.key
  openssl req -new -key ${device}.key \
    -subj "/C=US/O=Lab/OU=Metering/CN=${device}" \
    -out ${device}.csr
  openssl x509 -req -in ${device}.csr -CA ca.crt -CAkey ca.key \
    -CAcreateserial -sha256 -days 365 -out ${device}.crt
done
```

Benefits:

- **Granular ACLs**: Control access per device
- **Easy revocation**: Revoke individual certificates without affecting others
- **Audit trail**: Track connections per device

### Certificate Rotation

Implement automated certificate rotation:

```bash
# Example certificate rotation script
#!/bin/bash
CERT_VALIDITY_DAYS=90
WARNING_DAYS=30

for cert in /etc/ssl/devices/*.crt; do
  expiry=$(openssl x509 -in "$cert" -noout -enddate | cut -d= -f2)
  expiry_epoch=$(date -d "$expiry" +%s)
  now_epoch=$(date +%s)
  days_until_expiry=$(( (expiry_epoch - now_epoch) / 86400 ))

  if [ $days_until_expiry -lt $WARNING_DAYS ]; then
    echo "Certificate $cert expires in $days_until_expiry days"
    # Trigger renewal process
  fi
done
```

## Network Security

### Firewall Configuration

Restrict broker access to trusted networks:

```bash
# UFW example - allow only from management network
sudo ufw allow from 192.168.100.0/24 to any port 8883

# iptables example
sudo iptables -A INPUT -p tcp --dport 8883 -s 192.168.100.0/24 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8883 -j DROP
```

### VLAN Isolation

- Place MQTT broker on dedicated VLAN
- Isolate IoT devices from corporate network
- Use VLAN ACLs for additional access control

## Cipher Suite Configuration

### Restrict to Secure Ciphers (Optional)

For enhanced security, limit cipher suites:

```conf
# In /etc/mosquitto/conf.d/tls.conf
ciphers ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS
```

### TLS Version Control

Force minimum TLS version:

```conf
tls_version tlsv1.2
```

!!! note "Default Security"
    Modern Mosquitto versions default to secure settings. Only override if you have specific requirements.

## Access Control Lists (ACLs)

### Topic-Based Access Control

```conf
# In /etc/mosquitto/conf.d/acl.conf
acl_file /etc/mosquitto/acl.txt

# /etc/mosquitto/acl.txt
user whatwatt-001
topic write lab/energy/whatwatt-001
topic read lab/commands/whatwatt-001

user whatwatt-002
topic write lab/energy/whatwatt-002
topic read lab/commands/whatwatt-002
```

## Monitoring and Logging

### Enhanced Logging

```conf
# In /etc/mosquitto/conf.d/logging.conf
log_dest file /var/log/mosquitto/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
log_type debug
connection_messages true
log_timestamp true
```

### Log Rotation

```bash
# /etc/logrotate.d/mosquitto
/var/log/mosquitto/*.log {
    weekly
    missingok
    rotate 52
    compress
    notifempty
    create 644 mosquitto mosquitto
    postrotate
        /bin/kill -HUP `cat /var/run/mosquitto.pid 2> /dev/null` 2> /dev/null || true
    endscript
}
```

## Key Security Checklist

- ✅ Use unique certificates per device
- ✅ Enable hostname validation (remove `skip_cn_check`)
- ✅ Implement certificate rotation (yearly maximum)
- ✅ Restrict network access with firewalls/VLANs
- ✅ Use topic-based ACLs
- ✅ Enable comprehensive logging
- ✅ Monitor certificate expiration
- ✅ Keep CA private key offline/secure
- ✅ Regular security updates for Mosquitto
- ✅ Consider hardware security modules (HSM) for CA keys

!!! warning "CA Security"
    The Certificate Authority private key is the most critical component. Store it securely offline and use it only for certificate signing operations.
