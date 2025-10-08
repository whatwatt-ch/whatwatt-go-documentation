---
title: Quick Subscribe
category: concepts
tags:
- quick_subscribe
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Quick Subscribe

## Document Context

- **Purpose**: Command-line testing guide for secure MQTT broker using mosquitto_sub with TLS client certificate authentication
- **When to use**: Testing secure MQTT setup before device configuration, troubleshooting connection issues, verifying certificate authentication
- **Prerequisites**: Mosquitto client tools installed, generated certificates available, running secure MQTT broker
- **Related to**: MQTT broker setup (index.md), certificate deployment (deploy-certs.md), device provisioning (provision-payload.md)
- **Validates against**: Mosquitto broker TLS configuration, client certificate authentication, topic subscription functionality

## Key Facts

- **Tool**: mosquitto_sub - Command-line MQTT subscriber for testing
- **Port**: 8883 - Standard secure MQTT port with TLS
- **Authentication**: Client certificate (whatwatt.crt) + private key (whatwatt.key) + CA validation
- **Topic pattern**: lab/energy/# - Wildcard subscription for all energy data
- **Verification**: --insecure flag skips hostname validation for local testing

Test the secure MQTT setup using the command line client tools.

## Subscribe with TLS Client Certificate

Use `mosquitto_sub` to test the TLS connection with client certificate authentication:

```bash
mosquitto_sub -h 127.0.0.1 -p 8883 -v \
  --cafile ca.crt \
  --cert whatwatt.crt \
  --key whatwatt.key \
  --insecure \
  -t 'lab/energy/#'
```

## Command Explanation

| Parameter           | Purpose                                          |
|---------------------|--------------------------------------------------|
| `-h 127.0.0.1`     | Connect to localhost                            |
| `-p 8883`           | Use TLS port                                    |
| `-v`                | Verbose output (show topics)                   |
| `--cafile ca.crt`   | CA certificate to validate server              |
| `--cert whatwatt.crt` | Client certificate for authentication       |
| `--key whatwatt.key`  | Client private key                            |
| `--insecure`        | Skip hostname verification                     |
| `-t 'lab/energy/#'` | Subscribe to topic pattern                     |

## Example Output

If successful, you should see:

```txt
Client whatwatt-001 sending CONNECT
Client whatwatt-001 received CONNACK (0)
Client whatwatt-001 sending SUBSCRIBE (Mid: 1, Topic: lab/energy/#, QoS: 0)
Client whatwatt-001 received SUBACK
```

When the WhatWatt Go device publishes data, you'll see messages like:

```txt
lab/energy/whatwatt-001 {"P_In": 1.234, "P_Out": 0.000}
```

## Troubleshooting

### Connection Refused

```txt
Error: Connection refused
```

**Solution**: Check that Mosquitto is running and listening on port 8883:

```bash
sudo systemctl status mosquitto
sudo netstat -tlnp | grep :8883
```

### Certificate Verification Failed

```txt
Error: A TLS error occurred.
```

**Solutions**:

- Verify certificate paths are correct
- Check certificate validity: `openssl x509 -in whatwatt.crt -text -noout`
- Ensure certificates are signed by the same CA

### Authentication Failed

```txt
Connection Refused: not authorised.
```

**Solutions**:

- Verify client certificate is signed by the CA specified in `cafile`
- Check Mosquitto logs: `journalctl -u mosquitto -f`
- Ensure `require_certificate true` is set in Mosquitto config

!!! tip "Testing Without Device"
    Use this method to verify your MQTT broker setup before configuring the WhatWatt Go device.
