---
title: Loxone Integration
category: integrations
tags:
- loxone
- home_automation
- energy_monitoring
- smart_home
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-08'
---

# Loxone Integration

## Document Context

- **Purpose**: Complete integration guide for connecting WhatWatt Go devices with Loxone home automation system for energy monitoring and control
- **When to use**: Smart home setups with Loxone Miniserver, energy management automation, consumption monitoring, load balancing scenarios
- **Prerequisites**: Loxone Miniserver Gen 1/2, Loxone Config software, WhatWatt Go device on network, basic Loxone programming knowledge
- **Related to**: HTTP virtual inputs, energy monitoring blocks, data visualization, automation triggers based on energy consumption
- **Validates against**: Live energy data from WhatWatt Go REST API integrated into Loxone monitoring and automation logic

## Key Facts

- **Integration method**: HTTP REST API polling via Loxone Virtual HTTP Input
- **Update frequency**: Configurable polling interval (recommended: 30-60 seconds)
- **Data format**: JSON energy measurements parsed by Loxone
- **Authentication**: Optional HTTP digest authentication support
- **Monitoring capabilities**: Real-time power, energy counters, voltage, current, frequency
- **Automation potential**: Load shedding, solar optimization, peak demand management
- **Visualization**: Built-in Loxone energy monitoring widgets
- **Error handling**: Connection monitoring and fallback logic

This guide shows how to integrate WhatWatt Go energy monitoring into Loxone for comprehensive smart home energy management.

## Overview

The WhatWatt Go device integrates seamlessly with Loxone home automation systems through the REST API. This enables real-time energy monitoring, automated load control, and intelligent energy management within your Loxone smart home.

## Prerequisites

### Hardware

- Loxone Miniserver (Gen 1 or Gen 2)
- WhatWatt Go device (firmware 1.2+)
- Stable network connection for both devices

### Software

- Loxone Config (latest version)
- Access to Loxone configuration

### Network Setup

- Both devices on same network or accessible via routing
- HTTP connectivity from Miniserver to WhatWatt Go
- Optional: Static IP for WhatWatt Go device

## Step 1: Prepare WhatWatt Go Device

### 1.1 Find Device IP Address

Use device discovery to find your WhatWatt Go:

```bash
# Method 1: mDNS hostname
ping whatwatt-XXXXXX.local

# Method 2: Network scan
nmap -sn 192.168.1.0/24 | grep -A2 -B2 whatwatt
```

### 1.2 Test API Access

Verify REST API responds correctly:

```bash
# Test system endpoint
curl http://DEVICE_IP/api/v1/system

# Test energy data
curl http://DEVICE_IP/api/v1/report
```

Expected response format:

```json
{
  "timestamp": "2025-10-08T15:30:45Z",
  "power": {
    "total": 2456.7,
    "l1": 823.4,
    "l2": 891.2,
    "l3": 742.1
  },
  "energy": {
    "import": 1234567.8,
    "export": 98765.4
  },
  "voltage": {
    "l1": 231.2,
    "l2": 230.8,
    "l3": 232.1
  }
}
```

## Step 2: Configure Loxone Integration

### 2.1 Create Virtual HTTP Input

1. **Open Loxone Config**
2. **Navigate to Periphery → Virtual Inputs**
3. **Add new Virtual HTTP Input**:
   - **Name**: `WhatWatt_Energy`
   - **Address**: `http://DEVICE_IP/api/v1/report`
   - **Update Cycle**: `60` seconds (adjust as needed)
   - **Format**: `JSON`

### 2.2 Configure HTTP Settings

In the Virtual HTTP Input properties:

- **Method**: `GET`
- **Content-Type**: `application/json`
- **Timeout**: `30` seconds
- **Authentication**: Set if device has authentication enabled

### 2.3 Parse JSON Response

Add multiple Virtual HTTP Input Commands to extract data:

| Command Name | JSON Path | Description |
|--------------|-----------|-------------|
| `Power_Total` | `power.total` | Total power consumption (W) |
| `Power_L1` | `power.l1` | Phase L1 power (W) |
| `Power_L2` | `power.l2` | Phase L2 power (W) |
| `Power_L3` | `power.l3` | Phase L3 power (W) |
| `Energy_Import` | `energy.import` | Imported energy (Wh) |
| `Energy_Export` | `energy.export` | Exported energy (Wh) |
| `Voltage_L1` | `voltage.l1` | Phase L1 voltage (V) |

## Step 3: Create Energy Monitoring Logic

### 3.1 Add Energy Monitor Block

1. **Navigate to Building Structure**
2. **Add Energy Monitor Block**
3. **Configure inputs**:
   - Connect `Power_Total` to power input
   - Connect `Energy_Import` to meter input

### 3.2 Create Analog Memory for Values

Add Analog Memory blocks for each measurement:

```txt
Power_Total → Analog Memory → "Current_Power"
Energy_Import → Analog Memory → "Total_Energy"
Voltage_L1 → Analog Memory → "Voltage_L1"
```

### 3.3 Add Monitoring Logic

Create monitoring logic for:

- **High consumption alerts**
- **Power quality monitoring**
- **Energy cost calculation**
- **Load balancing triggers**

## Step 4: Visualization and Controls

### 4.1 Energy Dashboard

Create a room in Loxone Config for energy monitoring:

1. **Add Room**: "Energy Monitoring"
2. **Add Controls**:
   - **State Display**: Current power consumption
   - **Analog Display**: Real-time power values
   - **Info Box**: Daily/monthly energy totals
   - **Chart**: Power consumption history

### 4.2 Alerts and Notifications

Configure push notifications:

```txt
Power_Total > 5000W → Push Message: "High power consumption detected"
Voltage_L1 < 220V → Push Message: "Low voltage on L1"
```

## Step 5: Advanced Automation

### 5.1 Load Shedding

Create automatic load shedding based on consumption:

```txt
IF Power_Total > 4000W AND Solar_Available < 1000W
THEN
  Switch OFF non-essential loads
  Send notification
```

### 5.2 Solar Optimization

Optimize energy usage with solar production:

```txt
IF Solar_Production > Power_Consumption + 500W
THEN
  Start heat pump
  Start EV charging
```

### 5.3 Peak Demand Management

Prevent expensive peak demand charges:

```txt
IF 15min_Average_Power > Peak_Threshold
THEN
  Reduce loads by priority
  Delay non-critical operations
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No data received | Network connectivity | Check IP address and network |
| Timeout errors | Slow response | Increase timeout value |
| JSON parse errors | Wrong API endpoint | Verify `/api/v1/report` endpoint |
| Authentication failed | Wrong credentials | Check device authentication settings |

### Debug Steps

1. **Test API manually**: Use curl/browser to verify API response
2. **Check Loxone logs**: Monitor for HTTP request errors
3. **Verify JSON format**: Ensure response matches expected structure
4. **Network diagnostics**: Ping test between devices

### Error Monitoring

Add error handling in Loxone:

```txt
IF HTTP_Status ≠ 200
THEN
  Set error flag
  Send notification
  Use last known values
```

## Performance Optimization

### Update Frequency

- **Real-time monitoring**: 30-60 seconds
- **Historical data**: 5-10 minutes
- **Billing purposes**: 15 minutes

### Network Optimization

- Use static IP for WhatWatt Go
- Consider QoS settings for reliable communication
- Monitor network latency

## Example Automation Scenarios

### Scenario 1: Smart EV Charging

```txt
IF Solar_Production > House_Consumption + 2000W
AND EV_Connected = TRUE
THEN
  Start EV charging at available solar power
```

### Scenario 2: Heat Pump Optimization

```txt
IF Time = 06:00 AND Forecast_Solar > 3000W
THEN
  Pre-heat house using night tariff
  Prepare for solar heating
```

### Scenario 3: Battery Management

```txt
IF Grid_Power > 0 AND Battery_SOC < 20%
THEN
  Charge battery from grid (night tariff)
ELSE IF Solar_Excess > 1000W
THEN
  Charge battery from solar
```

## Security Considerations

- **Network security**: Keep devices on private network
- **Authentication**: Enable device authentication if accessible from internet
- **Regular updates**: Keep firmware updated
- **Monitoring**: Log access attempts and unusual patterns

## Next Steps

- **Expand monitoring**: Add more WhatWatt Go devices for detailed monitoring
- **Energy optimization**: Implement advanced load balancing algorithms
- **Cost tracking**: Integrate with utility billing data
- **Predictive control**: Use weather forecasts for heating/cooling optimization

## Support and Resources

- **Loxone Documentation**: Energy monitoring best practices
- **Community Forum**: Share automation ideas and troubleshooting
- **Professional Setup**: Consider Loxone Partner for complex installations
