---
title: Setup Script
category: concepts
tags:
- setup_script
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Setup Script

## Document Context

- **Purpose**: Automated Python script for configuring whatwatt Go devices with MQTT TLS settings via REST API with parameterized options
- **When to use**: Bulk device provisioning, automated deployment workflows, consistent configuration across multiple devices
- **Prerequisites**: Python 3 with requests library, generated certificates available, whatwatt Go devices accessible via network
- **Related to**: [Manual provisioning](provision-payload.md), [Certificate generation](tls-ca-ecc.md), MQTT setup verification
- **Validates against**: whatwatt Go REST API /api/v1/mqtt/settings endpoint, certificate file format requirements

## Key Facts

- **Language**: Python 3 with requests library for HTTP API calls
- **Configuration**: Command-line arguments for device IP, broker settings, certificates, topic configuration
- **Automation**: Parameterized script suitable for batch provisioning and CI/CD integration
- **Error handling**: Network timeouts, HTTP errors, missing files, JSON validation
- **Certificate loading**: Automatic file reading and embedding in JSON payload

Automated Python script to configure whatwatt Go devices with MQTT TLS settings.

## Script Code

Save as `setup_mqtt.py`:

```python
#!/usr/bin/env python3
"""Configure a whatwatt Go device over REST.

Example:
python setup_mqtt.py --device 192.168.99.176 --broker 192.168.99.186 \
  --topic lab/energy/whatwatt-001 --id whatwatt-001
"""
import argparse, pathlib, requests, json, sys

def args():
    p = argparse.ArgumentParser()
    p.add_argument("--device", default="192.168.99.176",
                   help="whatwatt Go device IP")
    p.add_argument("--broker", default="192.168.99.186",
                   help="MQTT broker IP")
    p.add_argument("--port", type=int, default=8883,
                   help="MQTT broker port")
    p.add_argument("--id", default="whatwatt-001",
                   help="MQTT client ID")
    p.add_argument("--topic", default="lab/energy/whatwatt-001",
                   help="MQTT topic")
    p.add_argument("--template",
                   default='{"P_In": ${1_7_0}, "P_Out": ${2_7_0}}',
                   help="MQTT payload template")
    p.add_argument("--ca", default="ca.crt",
                   help="CA certificate file")
    p.add_argument("--cert", default="whatwatt.crt",
                   help="Client certificate file")
    p.add_argument("--key", default="whatwatt.key",
                   help="Client private key file")
    return p.parse_args()

def main():
    a = args()
    api = f"http://{a.device}/api/v1/mqtt/settings"

    data = {
        "enable": True,
        "url": f"mqtts://{a.broker}:{a.port}",
        "skip_cn_check": True,
        "client_id": a.id,
        "publish": {"topic": a.topic, "template": a.template},
        "broker": {"certificate": pathlib.Path(a.ca).read_text()},
        "client": {
            "certificate": pathlib.Path(a.cert).read_text(),
            "key": pathlib.Path(a.key).read_text()
        }
    }

    try:
        r = requests.post(api, json=data, timeout=10)
        r.raise_for_status()
        print("Success:", json.dumps(r.json(), indent=2))
    except (requests.RequestException, OSError) as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Make Executable

```bash
chmod +x setup_mqtt.py
```

## Usage Examples

### Basic Usage

```bash
python setup_mqtt.py --device 192.168.99.176 --broker 192.168.99.186
```

### Custom Configuration

```bash
python setup_mqtt.py \
  --device 192.168.1.100 \
  --broker mqtt.example.com \
  --port 8883 \
  --id sensor-001 \
  --topic sensors/energy/001 \
  --template '{"timestamp": ${timestamp}, "power": ${1_7_0}, "energy": ${1_8_0}}'
```

### Specify Certificate Files

```bash
python setup_mqtt.py \
  --device 192.168.99.176 \
  --ca /path/to/ca.crt \
  --cert /path/to/device.crt \
  --key /path/to/device.key
```

## Command Line Options

| Option       | Default                           | Description                    |
|--------------|-----------------------------------|--------------------------------|
| `--device`   | `192.168.99.176`                | whatwatt Go device IP address |
| `--broker`   | `192.168.99.186`                | MQTT broker IP address        |
| `--port`     | `8883`                           | MQTT broker port              |
| `--id`       | `whatwatt-001`                   | MQTT client ID                |
| `--topic`    | `lab/energy/whatwatt-001`        | MQTT topic for publishing     |
| `--template` | `{"P_In": ${1_7_0}, "P_Out": ${2_7_0}}` | Payload template      |
| `--ca`       | `ca.crt`                         | CA certificate file path      |
| `--cert`     | `whatwatt.crt`                   | Client certificate file path  |
| `--key`      | `whatwatt.key`                   | Client private key file path  |

## Success Response

On successful configuration:

```json
{
  "enable": true,
  "url": "mqtts://192.168.99.186:8883",
  "skip_cn_check": true,
  "client_id": "whatwatt-001",
  "publish": {
    "topic": "lab/energy/whatwatt-001",
    "template": "{\"P_In\": ${1_7_0}, \"P_Out\": ${2_7_0}}"
  },
  "password_len": 0
}
```

## Error Handling

The script handles common errors:

- **Network errors**: Connection timeout, DNS resolution
- **HTTP errors**: 4xx/5xx responses from device
- **File errors**: Missing certificate files
- **JSON errors**: Invalid configuration format

!!! tip "Batch Configuration"
    Use this script in loops or with configuration management tools to provision multiple devices automatically.
