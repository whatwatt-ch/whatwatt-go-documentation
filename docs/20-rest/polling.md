---
title: Polling
category: api-endpoints
tags:
- polling
- data-retrieval
- energy-data
- rest-api
- measurements
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /api/v1/report
protocols:
- HTTP
- REST
related_concepts:
- energy measurements
- OBIS codes
- polling intervals
- data collection
use_cases:
- periodic data collection
- energy monitoring
- historical snapshots
- system integration
real_device_tested: true
authentication: required when device password is set
---

# Polling

## Document Context

- **Purpose**: Retrieve current energy measurements and meter status via REST API
- **When to use**: When you need current energy data, periodic monitoring, or system integration via HTTP
- **Prerequisites**: Device network connectivity; understanding of energy measurement concepts helpful
- **Related to**: Real-time streaming (SSE), CSV data logging, MQTT integration
- **Validates against**: Real device responses from multiple meter types

## Key Facts

- **Endpoint**: `/api/v1/report`
- **Method**: GET only
- **Authentication**: Required when device Web UI password is set
- **Response format**: JSON with OBIS-based field names
- **Typical response time**: <100ms
- **Rate limits**: None (but avoid excessive polling)
- **Error codes**: 401 (auth required), 404 (not found), 500 (internal error)
- **Data freshness**: Reflects latest meter reading (usually within 20 seconds)

## Endpoint Details

Reading measurements from the meter is possible by calling the API `api/v1/report` with the GET method.

| Endpoint              | `api/v1/report`  |
| --------------------- | ---------------- |
| Method                | GET              |
| Response content type | application/json |

--8<-- "../_partials/auth-note.md"

## Example response for Landis+Gyr LGZ (MBUS)

```json
{
    "report": {
        "id": 7892,
        "interval": 6.749,
        "tariff": 1,
        "date_time": "2025-10-07T14:26:10Z",
        "date_time_local": "2025-10-07T14:26:10+02:00",
        "date_time_utc": "2025-10-07T12:26:10Z",
        "instantaneous_power": {
            "active": {
                "positive": {
                    "total": 0,
                    "l1": 0,
                    "l2": 0,
                    "l3": 0
                },
                "negative": {
                    "total": 0,
                    "l1": 0,
                    "l2": 0,
                    "l3": 0
                }
            },
            "reactive": {
                "positive": {
                    "l1": 0,
                    "l2": 0,
                    "l3": 0
                },
                "negative": {
                    "l1": 0,
                    "l2": 0,
                    "l3": 0
                }
            }
        },
        "voltage": {
            "l1": 234,
            "l2": 0,
            "l3": 0
        },
        "current": {
            "l1": 0,
            "l2": 0,
            "l3": 0
        },
        "energy": {
            "active": {
                "positive": {
                    "total": 75.133
                },
                "negative": {
                    "total": 25.414
                }
            },
            "reactive": {
                "positive": {
                    "total": 82.328
                },
                "negative": {
                    "total": 19.481
                }
            }
        },
        "conv_factor": 1
    },
    "meter": {
        "status": "OK",
        "interface": "MBUS",
        "protocol": "DLMS",
        "logical_name": "LGZ1030784855204",
        "vendor": "Landis+Gyr",
        "prefix": "LGZ"
    },
    "system": {
        "id": "ECC9FF5C7F14",
        "date_time": "2025-10-07T14:26:24Z",
        "date_time_local": "2025-10-07T14:26:24+02:00",
        "date_time_utc": "2025-10-07T12:26:24Z",
        "boot_id": "7CDC08FD",
        "time_since_boot": 338155
    }
}
```

## Example response for Ensor eRS801 (P1)

```json
{
    "report": {
        "id": 72,
        "interval": 0.997,
        "tariff": 1,
        "date_time": "2025-10-07T14:29:41Z",
        "date_time_local": "2025-10-07T14:29:41+02:00",
        "date_time_utc": "2025-10-07T12:29:41Z",
        "instantaneous_power": {
            "active": {
                "positive": {
                    "total": 0.015,
                    "l1": 0.015,
                    "l2": 0,
                    "l3": 0
                },
                "negative": {
                    "total": 0,
                    "l1": 0,
                    "l2": 0,
                    "l3": 0
                }
            }
        },
        "voltage": {
            "l1": 234.01,
            "l2": 36.12,
            "l3": 36.48
        },
        "current": {
            "l1": 0.26,
            "l2": 0,
            "l3": 0
        },
        "energy": {
            "active": {
                "positive": {
                    "total": 190.01,
                    "t1": 120.133,
                    "t2": 69.877
                },
                "negative": {
                    "total": 0,
                    "t1": 0,
                    "t2": 0
                }
            }
        },
        "conv_factor": 1,
        "volume": [
            {
                "bus": 1,
                "meter_id": "20000741"
            }
        ]
    },
    "meter": {
        "status": "OK",
        "interface": "P1",
        "protocol": "DSMR",
        "protocol_version": "5.0",
        "logical_name": "ESR51030712084367",
        "id": "1ESR0012084367",
        "model": "1ESR0012084367",
        "vendor": "Ensor",
        "prefix": "ESR"
    },
    "system": {
        "id": "ECC9FF5C7F14",
        "date_time": "2025-10-07T14:29:42Z",
        "date_time_local": "2025-10-07T14:29:42+02:00",
        "date_time_utc": "2025-10-07T12:29:42Z",
        "boot_id": "7CDC08FD",
        "time_since_boot": 338352
    }
}
```

The API returns an object containing three main sub-objects: **report**, **meter**, and **system**. The report object includes real-time measurements. The meter object provides details about the meter, and the system object describes the system.

!!! note
    Fields within the report object may vary, and the presence of certain fields depends on the data sent by the meter.

## Field reference

| Field                                               | Type    | Unit                                                         | Description                                                  |
| --------------------------------------------------- | ------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `.report.id`                                        | uint    |                                                              | Report incremental identifier                                |
| `.report.interval`                                  | double  | s                                                            | Report period                                                |
| `.report.tariff`                                    | uint    |                                                              | 1 - t1, 2 - t2                                               |
| `.report.date_time`                                 | ISO8601 |                                                              | Time when report was generated in local time. The default time zone is European time zone. CET-1CEST,M3.5.0,M10.5.0/3 |
| `.report.date_time_local`                           | ISO8601 |                                                              | Report timestamp in local time zone with timezone offset    |
| `.report.date_time_utc`                             | ISO8601 |                                                              | Report timestamp in UTC time zone                           |
| `.report.instantaneous_power.active.positive.total`   | double  | kW                                                           | Positive active instantaneous power (A+)                     |
| `.report.instantaneous_power.active.positive.l1`      | double  | kW                                                           | Positive active instantaneous power (A+) in phase L1         |
| `.report.instantaneous_power.active.positive.l2`      | double  | kW                                                           | Positive active instantaneous power (A+) in phase L2         |
| `.report.instantaneous_power.active.positive.l3`      | double  | kW                                                           | Positive active instantaneous power (A+) in phase L3         |
| `.report.instantaneous_power.active.negative.total`   | double  | kW                                                           | Negative active instantaneous power (A-)                     |
| `.report.instantaneous_power.active.negative.l1`      | double  | kW                                                           | Negative active instantaneous power (A-)in phase L1          |
| `.report.instantaneous_power.active.negative.l2`      | double  | kW                                                           | Negative active instantaneous power (A-)in phase L2          |
| `.report.instantaneous_power.active.negative.l3`      | double  | kW                                                           | Negative active instantaneous power (A-)in phase L3          |
| `.report.instantaneous_power.reactive.positive.total` | double  | kvar                                                         | Positive reactive instantaneous power(Q+)                    |
| `.report.instantaneous_power.reactive.positive.l1`    | double  | kvar                                                         | Positive reactive instantaneous power(Q+) in phase L1        |
| `.report.instantaneous_power.reactive.positive.l2`    | double  | kvar                                                         | Positive reactive instantaneous power(Q+) in phase L2        |
| `.report.instantaneous_power.reactive.positive.l3`    | double  | kvar                                                         | Positive reactive instantaneous power(Q+) in phase L3        |
| `.report.instantaneous_power.reactive.negative.total` | double  | kvar                                                         | Negative reactive instantaneous power(Q-)                    |
| `.report.instantaneous_power.reactive.negative.l1`    | double  | kvar                                                         | Negative reactive instantaneous power(Q-) in phase L1        |
| `.report.instantaneous_power.reactive.negative.l2`    | double  | kvar                                                         | Negative reactive instantaneous power(Q-) in phase L2        |
| `.report.instantaneous_power.reactive.negative.l3`    | double  | kvar                                                         | Negative reactive instantaneous power(Q-) in phase L3        |
| `.report.instantaneous_power.apparent.total`          | double  | kVA                                                          | Apparent instantaneous power (S+)                            |
| `.report.voltage.l1`                                  | double  | V                                                            | Instantaneous voltage (U) in phase L1                        |
| `.report.voltage.l2`                                  | double  | V                                                            | Instantaneous voltage (U) in phase L2                        |
| `.report.voltage.l3`                                  | double  | V                                                            | Instantaneous voltage (U) in phase L3                        |
| `.report.current.l1`                                  | double  | A                                                            | Instantaneous current (I) in phase L1                        |
| `.report.current.l2`                                  | double  | A                                                            | Instantaneous current (I) in phase L2                        |
| `.report.current.l3`                                  | double  | A                                                            | Instantaneous current (I) in phase L3                        |
| `.report.energy.active.positive.total`                | double  | kWh                                                          | Positive active energy (A+) total                            |
| `.report.energy.active.positive.t1`                   | double  | kWh                                                          | Positive active energy (A+) in tariff T1                     |
| `.report.energy.active.positive.t2`                   | double  | kWh                                                          | Positive active energy (A+) in tariff T2                     |
| `.report.energy.active.negative.total`                | double  | kWh                                                          | Negative active energy (A-) total                            |
| `.report.energy.active.negative.t1`                   | double  | kWh                                                          | Negative active energy (A-) in tariff T1                     |
| `.report.energy.active.negative.t2`                   | double  | kWh                                                          | Negative active energy (A-) in tariff T2                     |
| `.report.energy.reactive.positive.total`              | double  | kvarh                                                        | Positive reactive energy (Q+) total                          |
| `.report.energy.reactive.positive.t1`                 | double  | kvarh                                                        | Positive reactive energy (Q+) in tariff T1                   |
| `.report.energy.reactive.positive.t2`                 | double  | kvarh                                                        | Positive reactive energy (Q+) in tariff T2                   |
| `.report.energy.reactive.negative.total`              | double  | kvarh                                                        | Negative reactive energy (Q-) total                          |
| `.report.energy.reactive.negative.t1`                 | double  | kvarh                                                        | Negative reactive energy (Q-) in tariff T1                   |
| `.report.energy.reactive.negative.t2`                 | double  | kvarh                                                        | Negative reactive energy (Q-) in tariff T2                   |
| `.report.energy.reactive.imported.inductive.total`    | double  | kvarh                                                        | Imported inductive reactive energy in 1st quadrant (Q1) total |
| `.report.energy.reactive.imported.inductive.t1`       | double  | kvarh                                                        | Imported inductive reactive energy in 1st quadrant (Q1) in tariff T1 |
| `.report.energy.reactive.imported.inductive.t2`       | double  | kvarh                                                        | Imported inductive reactive energy in 1st quadrant (Q1) in tariff T2 |
| `.report.energy.reactive.imported.capacitive.total`   | double  | kvarh                                                        | Imported capacitive reactive energy in 2nd quadrant (Q2) total |
| `.report.energy.reactive.imported.capacitive.t1`      | double  | kvarh                                                        | Imported capacitive reactive energy in 2nd quadrant (Q2) in tariff T1 |
| `.report.energy.reactive.imported.capacitive.t2`      | double  | kvarh                                                        | Imported capacitive reactive energy in 2nd quadrant (Q2) in tariff T2 |
| `.report.energy.reactive.exported.inductive.total`    | double  | kvarh                                                        | Exported inductive reactive energy in 3rd quadrant (Q3) total |
| `.report.energy.reactive.exported.inductive.t1`       | double  | kvarh                                                        | Exported inductive reactive energy in 3rd quadrant (Q3) in tariff T1 |
| `.report.energy.reactive.exported.inductive.t2`       | double  | kvarh                                                        | Exported inductive reactive energy in 3rd quadrant (Q3) in tariff T2 |
| `.report.energy.reactive.exported.capacitive.total`   | double  | kvarh                                                        | Exported capacitive reactive energy in 4th quadrant (Q4) total |
| `.report.energy.reactive.exported.capacitive.t1`      | double  | kvarh                                                        | Exported capacitive reactive energy in 4th quadrant (Q4) in tariff T1 |
| `.report.energy.reactive.exported.capacitive.t2`      | double  | kvarh                                                        | Exported capacitive reactive energy in 4th quadrant (Q4) in tariff T2 |
| `.report.max_demand.active.positive.total`            | double  | kW                                                           | Positive active maximum demand (A+) total                    |
| `.report.max_demand.active.positive.t1`               | double  | kW                                                           | Positive active maximum demand (A+) in tariff T1             |
| `.report.max_demand.active.positive.t2`               | double  | kW                                                           | Positive active maximum demand (A+) in tariff T2             |
| `.report.max_demand.active.negative.total`            | double  | kW                                                           | Negative active maximum demand (A-) total                    |
| `.report.max_demand.active.negative.t1`               | double  | kW                                                           | Negative active maximum demand (A-) in tariff T1             |
| `.report.max_demand.active.negative.t2`               | double  | kW                                                           | Negative active maximum demand (A-) in tariff T2             |
| `.report.power_factor`                                 | double  |                                                              | Instantaneous power factor                                   |
| `.report.conv_factor`                                  | uint    |                                                              | Conversion coefficient, the value of the integer by which instantaneous power, energy, current, max demand will be multiplied |
| `.report.volume[].bus`                                 | uint    |                                                              | Bus number for multi-meter installations                     |
| `.report.volume[].meter_id`                            | string  |                                                              | Meter identifier for multi-meter installations               |
| `.report.volume[].date_time`                           | ISO8601 |                                                              | Timestamp (local time) when the volume entry was captured     |
| `.report.volume[].cumulative`                          | double  |                                                              | Cumulative counter reported by the sub-meter on the bus (unit depends on device) |
| `.meter.status`                                        | string  | NOT CONNECTED<br/>NO DATA<br/>RECOGNITION<br/>OK<br/>ENCRYPTION KEY<br/>KEY REQUIRED<br/>NOT RECOGNIZED | Meter connection status |
| `.meter.interface`                                     | string  | P1<br/>TTL<br/>MBUS                                         | Physical interface                                           |
| `.meter.protocol`                                      | string  | DSMR<br/>DLMS<br/>KMP<br/>MEP                               | Logical interface                                            |
| `.meter.protocol_version`                              | string  |                                                              | Communication protocol version                               |
| `.meter.id`                                            | string  |                                                              | Meter identifier (as reported by the device)                 |
| `.meter.model`                                         | string  |                                                              | Meter model (as reported by the device)                      |
| `.meter.logical_name`                                  | string  |                                                              | Meter logical name                                           |
| `.meter.vendor`                                        | string  |                                                              | Meter supplier name, if identifiable                         |
| `.meter.prefix`                                        | string  |                                                              | 3 letter vendor prefixes                                     |
| `.system.id`                                           | string  |                                                              | WhatWatt Go unique identifier                                |
| `.system.date_time`                                    | ISO8601 |                                                              | Local date time for time zone                                |
| `.system.date_time_local`                              | ISO8601 |                                                              | System timestamp in local time zone with timezone offset    |
| `.system.date_time_utc`                                | ISO8601 |                                                              | System timestamp in UTC time zone                           |
| `.system.boot_id`                                      | string  |                                                              | Random string generated after each reboot                    |
| `.system.time_since_boot`                              | double  | s                                                            | Time in second since boot                                    |

## Common Issues & Solutions

### Issue: HTTP 401 Unauthorized

- **Symptoms**: `curl` returns "401 Unauthorized" or "Authentication required"
- **Root cause**: Device has Web UI password protection enabled
- **Diagnosis**: Check device settings - if `system.protection: true`, authentication is required
- **Solution**: Use authentication with device password
- **Code pattern**: `curl --anyauth -u ":YOUR_PASSWORD" http://device/api/v1/report`
- **Related**: [HTTP Digest Authentication Guide](../90-appendix/digest-cheatsheet.md)

### Issue: Empty or zero values in response

- **Symptoms**: Many fields return `0` or `null` values
- **Root cause**: Meter doesn't provide all OBIS objects or communication issue
- **Diagnosis**: Check `meter.status` field - should be "OK"
- **Solution**:
  - If `meter.status != "OK"`: Check physical meter connection
  - If status is "OK": Meter model simply doesn't provide those measurements
- **Code pattern**: `if (data.meter.status === "OK" && data.report.energy.active.positive.total > 0)`
- **Related**: Different meter models provide different data sets

### Issue: Stale data or old timestamps

- **Symptoms**: `date_time` field shows old timestamp (>1 minute ago)
- **Root cause**: Meter communication interruption or device time sync issue
- **Diagnosis**: Compare `report.date_time_utc` with current time
- **Solution**:
  - Check physical meter connection (MBUS, P1 cable)
  - Verify device time synchronization (NTP)
  - Restart meter communication via device settings
- **Code pattern**: `time_diff = current_utc - parse_timestamp(data.report.date_time_utc)`
- **Related**: [Meter Communication Settings](../50-settings/meter-comm.md)

### Issue: Inconsistent field availability

- **Symptoms**: Some API calls include certain fields, others don't
- **Root cause**: Different meter types provide different OBIS objects
- **Diagnosis**: Check `meter.interface` and `meter.protocol` to understand meter type
- **Solution**: Use defensive programming - check field existence before accessing
- **Code pattern**:

```python
def safe_get_power(data):
    try:
        return data["report"]["instantaneous_power"]["active"]["positive"]["total"]
    except KeyError:
        return None  # Field not available for this meter type
```

- **Related**: OBIS code availability varies by meter manufacturer

### Issue: Three-phase vs single-phase confusion

- **Symptoms**: Phase L2/L3 values always zero on single-phase meters
- **Root cause**: Single-phase meters only provide L1 measurements
- **Diagnosis**: Check if `voltage.l2` and `voltage.l3` are consistently zero
- **Solution**: For single-phase systems, use only `total` and `l1` values
- **Code pattern**: `total_power = data.report.instantaneous_power.active.positive.total`
- **Related**: Meter installation type determines available phases

### Issue: Network connectivity problems

- **Symptoms**: Connection timeouts, DNS resolution failures
- **Root cause**: Device not reachable on network
- **Diagnosis**:
  - Ping device IP address
  - Check mDNS name resolution: `ping whatwatt-XXXXXX.local`
  - Verify device is on same network segment
- **Solution**:
  - Use device discovery tools
  - Check WiFi/Ethernet settings
  - Verify network firewall rules
- **Code pattern**: Include proper timeout and retry logic in HTTP clients
- **Related**: [Device Discovery](../10-general/discovery.md), [Network Setup](../50-settings/wifi-setup.md)

## Usage Patterns

### Pattern: Real-time energy monitoring dashboard

**Use case**: Display current power consumption and generation
**Method**: Periodic REST API polling
**Code**:

```python
import requests
from requests.auth import HTTPDigestAuth
import time

def get_live_power(device_ip, password=None):
    """Get current power import/export values"""
    auth = HTTPDigestAuth("", password) if password else None

    try:
        response = requests.get(
            f"http://{device_ip}/api/v1/report",
            auth=auth,
            timeout=5
        )
        response.raise_for_status()
        data = response.json()

        if data["meter"]["status"] != "OK":
            return None, f"Meter status: {data['meter']['status']}"

        power_data = {
            "import_kw": data["report"]["instantaneous_power"]["active"]["positive"]["total"],
            "export_kw": data["report"]["instantaneous_power"]["active"]["negative"]["total"],
            "voltage_l1": data["report"]["voltage"]["l1"],
            "timestamp": data["report"]["date_time_utc"]
        }
        return power_data, None

    except requests.RequestException as e:
        return None, f"Network error: {e}"
    except KeyError as e:
        return None, f"Data format error: {e}"

# Usage example
while True:
    power, error = get_live_power("192.168.1.100", "device_password")
    if power:
        print(f"Import: {power['import_kw']:.3f} kW, Export: {power['export_kw']:.3f} kW")
    else:
        print(f"Error: {error}")
    time.sleep(30)  # Poll every 30 seconds
```

**Expected result**: Live power readings every 30 seconds
**Error handling**: Graceful handling of network issues and meter communication problems

### Pattern: Energy usage analysis and reporting

**Use case**: Calculate daily/monthly energy consumption
**Method**: REST API polling with data aggregation
**Code**:

```python
import requests
from datetime import datetime, timedelta
import json

class EnergyMonitor:
    def __init__(self, device_ip, password=None):
        self.device_ip = device_ip
        self.auth = HTTPDigestAuth("", password) if password else None
        self.last_energy = None

    def get_current_energy(self):
        """Get current cumulative energy readings"""
        response = requests.get(
            f"http://{self.device_ip}/api/v1/report",
            auth=self.auth
        )
        data = response.json()

        return {
            "timestamp": datetime.fromisoformat(data["report"]["date_time_utc"].replace("Z", "+00:00")),
            "imported_kwh": data["report"]["energy"]["active"]["positive"]["total"],
            "exported_kwh": data["report"]["energy"]["active"]["negative"]["total"]
        }

    def calculate_period_usage(self, hours=24):
        """Calculate energy usage over specified period"""
        current = self.get_current_energy()

        if self.last_energy is None:
            self.last_energy = current
            return None  # Need baseline measurement

        # Calculate differences
        time_diff = (current["timestamp"] - self.last_energy["timestamp"]).total_seconds() / 3600

        if time_diff >= hours:
            usage = {
                "period_hours": time_diff,
                "imported_kwh": current["imported_kwh"] - self.last_energy["imported_kwh"],
                "exported_kwh": current["exported_kwh"] - self.last_energy["exported_kwh"],
                "net_kwh": (current["imported_kwh"] - self.last_energy["imported_kwh"]) -
                          (current["exported_kwh"] - self.last_energy["exported_kwh"])
            }
            self.last_energy = current
            return usage

        return None  # Not enough time elapsed

# Usage
monitor = EnergyMonitor("192.168.1.100", "password")
usage = monitor.calculate_period_usage(24)  # Daily usage
if usage:
    print(f"Daily usage: {usage['net_kwh']:.2f} kWh net")
```

### Pattern: Solar system monitoring

**Use case**: Track solar production and self-consumption
**Method**: REST API with solar-specific data extraction
**Code**:

```python
def analyze_solar_system(device_ip, password=None):
    """Analyze solar system performance"""
    auth = HTTPDigestAuth("", password) if password else None

    response = requests.get(f"http://{device_ip}/api/v1/report", auth=auth)
    data = response.json()

    # Current values
    import_power = data["report"]["instantaneous_power"]["active"]["positive"]["total"]
    export_power = data["report"]["instantaneous_power"]["active"]["negative"]["total"]

    # Cumulative values
    total_imported = data["report"]["energy"]["active"]["positive"]["total"]
    total_exported = data["report"]["energy"]["active"]["negative"]["total"]

    # Solar analysis
    solar_analysis = {
        "currently_producing": export_power > 0,
        "current_production_kw": export_power,
        "current_consumption_kw": import_power,
        "current_self_consumption_kw": max(0, import_power - export_power) if export_power > 0 else import_power,
        "lifetime_production_kwh": total_exported,
        "lifetime_consumption_kwh": total_imported,
        "net_meter_reading": total_imported - total_exported
    }

    return solar_analysis

# Usage
solar_data = analyze_solar_system("192.168.1.100")
print(f"Solar producing: {solar_data['currently_producing']}")
print(f"Production: {solar_data['current_production_kw']:.3f} kW")
print(f"Self-consumption: {solar_data['current_self_consumption_kw']:.3f} kW")
```

### Pattern: Three-phase load balancing analysis

**Use case**: Monitor electrical load distribution across phases
**Method**: REST API with per-phase data analysis
**Code**:

```python
def analyze_phase_balance(device_ip, password=None):
    """Analyze three-phase load distribution"""
    auth = HTTPDigestAuth("", password) if password else None

    response = requests.get(f"http://{device_ip}/api/v1/report", auth=auth)
    data = response.json()

    # Extract per-phase data
    power = data["report"]["instantaneous_power"]["active"]["positive"]
    voltage = data["report"]["voltage"]
    current = data["report"]["current"]

    phases = {
        "L1": {
            "power_kw": power["l1"],
            "voltage_v": voltage["l1"],
            "current_a": current["l1"]
        },
        "L2": {
            "power_kw": power["l2"],
            "voltage_v": voltage["l2"],
            "current_a": current["l2"]
        },
        "L3": {
            "power_kw": power["l3"],
            "voltage_v": voltage["l3"],
            "current_a": current["l3"]
        }
    }

    # Calculate balance metrics
    total_power = power["total"]
    phase_powers = [phases[p]["power_kw"] for p in phases]
    active_phases = [p for p in phase_powers if p > 0]

    if len(active_phases) > 1:
        max_phase = max(phase_powers)
        min_phase = min([p for p in phase_powers if p > 0])
        imbalance_pct = ((max_phase - min_phase) / max_phase) * 100 if max_phase > 0 else 0
    else:
        imbalance_pct = 0

    return {
        "phases": phases,
        "total_power_kw": total_power,
        "active_phases": len(active_phases),
        "imbalance_percent": imbalance_pct,
        "is_balanced": imbalance_pct < 10  # Less than 10% imbalance
    }

# Usage
balance = analyze_phase_balance("192.168.1.100")
print(f"Phase imbalance: {balance['imbalance_percent']:.1f}%")
if not balance["is_balanced"]:
    print("Warning: Significant phase imbalance detected")
```

---

## Semantic Field Map

Understanding the JSON response structure for RAG and data processing:

### Power Measurements Group (Real-time Values)

- `report.instantaneous_power.active.positive.total` → **semantic_name**: "current_import_power" → **meaning**: "Instantaneous power consumption from grid" → **unit**: "kW" → **type**: "real_time_measurement"
- `report.instantaneous_power.active.negative.total` → **semantic_name**: "current_export_power" → **meaning**: "Instantaneous power fed back to grid" → **unit**: "kW" → **type**: "real_time_measurement"
- `report.instantaneous_power.reactive.positive` → **semantic_name**: "current_reactive_power_positive" → **meaning**: "Inductive reactive power consumption" → **unit**: "kvar" → **type**: "real_time_measurement"

### Energy Counters Group (Cumulative Values)

- `report.energy.active.positive.total` → **semantic_name**: "total_energy_imported" → **meaning**: "Cumulative energy consumed from grid since meter installation" → **unit**: "kWh" → **type**: "cumulative_counter"
- `report.energy.active.negative.total` → **semantic_name**: "total_energy_exported" → **meaning**: "Cumulative energy fed back to grid since meter installation" → **unit**: "kWh" → **type**: "cumulative_counter"
- `report.energy.reactive.positive.total` → **semantic_name**: "total_reactive_energy_positive" → **meaning**: "Cumulative positive reactive energy" → **unit**: "kvarh" → **type": "cumulative_counter"

### Electrical Parameters Group (Per-Phase Values)

- `report.voltage.l1, .l2, .l3` → **semantic_name**: "line_voltages" → **meaning**: "RMS voltage for each phase" → **unit**: "V" → **type**: "real_time_measurement"
- `report.current.l1, .l2, .l3` → **semantic_name**: "line_currents" → **meaning**: "RMS current for each phase" → **unit**: "A" → **type**: "real_time_measurement"
- `report.instantaneous_power.active.positive.l1, .l2, .l3` → **semantic_name**: "per_phase_power" → **meaning**: "Power consumption per individual phase" → **unit**: "kW" → **type**: "real_time_measurement"

### Device Status Group

- `meter.status` → **semantic_name**: "meter_communication_status" → **meaning**: "Health of communication with energy meter" → **unit**: "enum" → **type**: "status_indicator" → **values**: ["OK", "NO DATA", "RECOGNITION", etc.]
- `meter.interface` → **semantic_name**: "meter_interface_type" → **meaning**: "Physical connection method to meter" → **unit**: "enum" → **type**: "device_metadata" → **values**: ["MBUS", "P1", "TTL", "MEP"]
- `meter.protocol` → **semantic_name**: "meter_protocol_type" → **meaning**: "Communication protocol used" → **unit**: "enum" → **type**: "device_metadata" → **values**: ["DLMS", "DSMR", "KMP", "MEP"]

### Temporal Data Group

- `report.date_time_utc` → **semantic_name**: "measurement_timestamp_utc" → **meaning**: "When meter reading was taken (UTC)" → **unit**: "ISO-8601" → **type**: "timestamp"
- `report.id` → **semantic_name**: "report_sequence_number" → **meaning**: "Sequential reading number since device boot" → **unit**: "integer" → **type**: "sequence_metadata"
- `report.interval` → **semantic_name**: "seconds_since_last_reading" → **meaning**: "Time elapsed since previous meter reading" → **unit**: "seconds" → **type**: "timing_metadata"

### System Metadata Group

- `system.id` → **semantic_name**: "device_unique_identifier" → **meaning**: "Unique hardware identifier of WhatWatt Go device" → **unit**: "hex_string" → **type**: "device_metadata"
- `system.time_since_boot` → **semantic_name**: "device_uptime_seconds" → **meaning**: "Seconds since device last restarted" → **unit**: "seconds" → **type**: "system_metadata"
- `meter.logical_name` → **semantic_name**: "meter_serial_number" → **meaning**: "Unique identifier of the energy meter" → **unit**: "string" → **type**: "device_metadata"

**RAG Processing Patterns**:

- **Energy consumption analysis**: Compare `energy.active.positive.total` over time for usage trends
- **Solar production monitoring**: Use `energy.active.negative.total` and `instantaneous_power.active.negative.total` for solar systems
- **Power quality assessment**: Monitor `voltage` and `current` values for electrical system health
- **Real-time monitoring**: Focus on `instantaneous_power` fields for live energy flow
- **Data validation**: Always check `meter.status == "OK"` before processing measurements
- **Multi-phase analysis**: Use per-phase data (l1, l2, l3) for load balancing insights

---
