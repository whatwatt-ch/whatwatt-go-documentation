---
title: System Information
category: api-endpoints
tags:
- system-info
- device-status
- hardware-info
- diagnostics
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- /api/v1/system
protocols:
- HTTP
- REST
related_concepts:
- device identification
- hardware diagnostics
- connection status
- meter information
use_cases:
- device discovery
- health monitoring
- troubleshooting
- inventory management
real_device_tested: true
authentication: required when device password is set
---


# System Information

## Document Context

- **Purpose**: Retrieve comprehensive device information including hardware status, network connectivity, and meter details
- **When to use**: For device discovery, health monitoring, troubleshooting, or inventory management
- **Prerequisites**: Network connectivity to device; no special knowledge required
- **Related to**: Device configuration, network setup, meter communication status
- **Validates against**: Real device data from whatwatt Go hardware

## Key Facts

- **Endpoint**: `/api/v1/system`
- **Method**: GET only
- **Authentication**: Required when device Web UI password is set
- **Response format**: JSON with nested objects (device, clouds, services, meter, wifi, ethernet, sd_card)
- **Typical response time**: <50ms
- **Error codes**: 401 (auth required), 500 (internal error)
- **Information includes**: Hardware specs, firmware version, network status, meter connectivity, cloud service status

## Endpoint Details

System information can be read using HTTP. To do this, make a GET request with the path `api/v1/system`.

| Endpoint              | `api/v1/system`  |
| --------------------- | ---------------- |
| Method                | GET              |
| Response content type | application/json |

--8<-- "../_partials/auth-note.md"

## Example request

=== "No auth"
    ```bash
    curl http://whatwatt-ABCDEF.local/api/v1/system
    ```

=== "With password"
    ```bash
    curl --anyauth -u ":PASSWORD" http://whatwatt-ABCDEF.local/api/v1/system
    ```

## Example response

```json
{
    "device": {
        "name": "",
        "id": "ECC9FF5C7F14",
        "model": "WW_Go_1.2",
        "firmware": "1.10.0",
        "build": "11b8102-68dfd692",
        "upgrade_capable": true,
        "date": "2025-10-07",
        "time": "14:20:52",
        "time_since_boot": 337837,
        "last_reboot": {
            "date": "2025-10-03",
            "time": "16:30:29"
        },
        "plug": {
            "v_usb": 5.16,
            "v_mbus": 13.94,
            "v_p1": 2.83,
            "v_scap": 4.87
        },
        "license": {
            "type": "PLUS",
            "activation_date": "2025-09-24T11:05:41Z"
        }
    },
    "clouds": {
        "whatwatt": {
            "enabled": true,
            "connected": true,
            "registered": true
        },
        "mystrom": {
            "enabled": false,
            "status": "DISABLED"
        },
        "solar_manager": {
            "enabled": false,
            "connected": false
        },
        "mqtc": {
            "enabled": false,
            "connected": false
        },
        "stromkonto": {
            "enabled": false,
            "connected": false
        }
    },
    "services": {
        "berry": {
            "execution_status": {
                "state": "IDLE"
            }
        }
    },
    "meter": {
        "status": "OK",
        "interface": "MBUS",
        "id": "",
        "manufacturer": "Landis+Gyr",
        "type": "LGZ1030784855204",
        "model": "",
        "protocol": "DLMS",
        "protocol_version": "",
        "report_interval": 6.794,
        "enc_en": false,
        "auth_en": false,
        "tariff": 1,
        "date": "2025-10-07",
        "time": "14:20:52"
    },
    "wifi": {
        "ssid": "sjj",
        "bssid": "DC15C84FBAB6",
        "channel": 13,
        "ht": "20",
        "rssi": -29,
        "signal": 100,
        "auth_mode": "WPA2-WPA3",
        "pairwise_cipher": "CCMP",
        "group_cipher": "CCMP",
        "phy": "bgn",
        "wps": false,
        "country": "CH",
        "mac": "ECC9FF5C7F14",
        "ip": "192.168.99.114",
        "mask": "255.255.255.0",
        "gateway": "192.168.99.1",
        "dns": "192.168.0.1",
        "status": "OK",
        "mode": "STA"
    },
    "ethernet": {
        "mac": "ECC9FF5C7F17",
        "status": "Up",
        "ip": "192.168.0.40",
        "mask": "255.255.255.0",
        "gateway": "192.168.0.1",
        "dns": "192.168.0.1"
    },
    "sd_card": {
        "installed": true,
        "type": "SDHC/SDXC",
        "size": 7618,
        "speed": 20
    }
}
```

## Field reference

| Field                            | Type                             | Range                                                        | Description                                                  |
| -------------------------------- | -------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `.device.name`                   | string                           | 0..31                                                        | You can set device name used Web UI System > Name          |
| `.device.id`                     | string                           | 12 upper-case hexadecimal letters                           | The unique identifier of device                             |
| `.device.model`                  | string                           |                                                              | The model of device                                         |
| `.device.firmware`               | string                           |                                                              | Firmware version installed on device                        |
| `.device.build`                  | string                           |                                                              | Firmware build identifier                                   |
| `.device.upgrade_capable`        | boolean                          |                                                              | Is device capable of over-the-air firmware updates         |
| `.device.date`                   | string                           | YYYY-MM-DD                                                   | System date in local time zone                              |
| `.device.time`                   | string                           | HH:MM:SS                                                     | System time in local time zone                              |
| `.device.time_since_reboot`      | int                              |                                                              | Seconds from last reboot                                    |
| `.device.last_reboot.date`       | string                           | YYYY-MM-DD                                                   | Date of last reboot in local time zone                      |
| `.device.last_reboot.time`       | string                           | HH:MM:SS                                                     | Time of last reboot in local time zone                      |
| `.device.plug.v_usb`             | double                           |                                                              | USB voltage                                                 |
| `.device.plug.v_mbus`            | double                           |                                                              | M-Bus voltage                                               |
| `.device.plug.v_p1`              | double                           |                                                              | P1 voltage                                                  |
| `.device.plug.v_scap`            | double                           |                                                              | Super capacitor voltage. Should not drop below 4.5V when powering via M-bus |
| `.device.license.type`           | string                           | PLUS<br/>PRO                                                | Device license type                                         |
| `.device.license.activation_date`| string                           | ISO 8601 format                                             | License activation date in UTC                              |
| `.clouds.whatwatt.enabled`       | boolean                          |                                                              | Status is the whatwatt cloud enabled                        |
| `.clouds.whatwatt.connected`     | boolean                          |                                                              | Status is there a connection to the cloud whatwatt          |
| `.clouds.whatwatt.registered`    | boolean                          |                                                              | Status if device is registered with whatwatt cloud          |
| `.clouds.mystrom.enabled`        | boolean                          |                                                              | Status if myStrom Cloud is enabled                          |
| `.clouds.mystrom.status`         | string                           | DISABLED<br/>DISCONNECTED<br/>WAITING TIME<br/>CONNECTING<br/>DO HANDSHAKE<br/>CONNECTED<br/>REGISTERED | myStrom Service Status                                      |
| `.clouds.solar_manager.enabled`  | boolean                          |                                                              | Status if Solar Manager Cloud is enabled                    |
| `.clouds.solar_manager.connected`| boolean                          |                                                              | Status: whether there is a connection to the Solar Manager cloud |
| `.clouds.mqtc.enabled`           | boolean                          |                                                              | Status if the local MQTT client is enabled                  |
| `.clouds.mqtc.connected`         | boolean                          |                                                              | Status if the local MQTT client is connected                |
| `.clouds.stromkonto.enabled`    | boolean                          |                                                              | Status if Stromkonto integration is enabled                 |
| `.clouds.stromkonto.connected`  | boolean                          |                                                              | Status if connected to Stromkonto service                   |
| `.services.berry.execution_status.state` | string                   | IDLE<br/>RUNNING<br/>ERROR                                  | Berry script execution status                               |
| `.meter.status`                  | string                           | NOT CONNECTED<br/>NO DATA<br/>RECOGNITION<br/>OK<br/>ENCRYPTION KEY<br/>KEY REQUIRED<br/>NOT RECOGNIZED | Meter connection status                                     |
| `.meter.interface`               | string                           | NONE<br/>P1<br/>MBUS<br/>TTL<br/>MEP                        | Type of meter interface used, physical layer                |
| `.meter.id`                      | string                           |                                                              | Meter identifier                                            |
| `.meter.manufacturer`            | string                           |                                                              | Meter manufacturer if specified                             |
| `.meter.type`                    | string                           |                                                              | Meter type if specified                                     |
| `.meter.model`                   | string                           |                                                              | Meter model if specified                                    |
| `.meter.protocol`                | string                           | DSMR<br/>DLMS<br/>KMP<br/>MEP<br/>MBUS                      | Data protocol, logical layer                                |
| `.meter.protocol_version`        | string                           |                                                              | Meter protocol version if specified                         |
| `.meter.report_interval`         | double                           |                                                              | Meter report interval                                       |
| `.meter.enc_en`                  | boolean                          |                                                              | Is encryption enabled on meter communication                |
| `.meter.auth_en`                 | boolean                          |                                                              | Is authentication enabled on meter communication            |
| `.meter.tariff`                  | uint                             | 1, 2                                                         | Current tariff on meter if specified                        |
| `.meter.date`                    | string                           |                                                              | Date on meter in local time zone                            |
| `.meter.time`                    | string                           |                                                              | Time on meter in local time zone                            |
| `.wifi.ssid`                     | string                           | 1..32                                                        | The SSID (Service Set Identifier) is the name of a Wi-Fi network |
| `.wifi.bssid`                    | string                           | 12 upper-case hexadecimal letters                           | The BSSID (Basic Service Set Identifier) is the MAC address of wireless access point |
| `.wifi.channel`                  | uint                             | 1..13                                                        | Wi-Fi channel frequency range                               |
| `.wifi.ht`                       | string                           | 20<br/>40+<br/>40-                                          | Wi-Fi HT (High Throughput) mode from 802.11n standard      |
| `.wifi.rssi`                     | int                              | dBm                                                          | Received Signal Strength Indicator in decibels             |
| `.wifi.signal`                   | uint                             | 0..100                                                       | Wi-Fi signal strength in percent                            |
| `.wifi.auth_mode`                | string                           | open<br/>WEP<br/>WPA<br/>WPA2<br/>WPA-WPA2<br/>EAP<br/>WPA3<br/>WPA2-WPA3<br/>WAPI<br/>OWE<br/>WPA3-ENT | Wi-Fi authentication mode                                   |
| `.wifi.pairwise_cipher`          | string                           |                                                              | Encryption method for unicast communication                 |
| `.wifi.group_cipher`             | string                           | none<br/>WEP40<br/>WEP104<br/>TKIP<br/>CCMP<br/>TKIP-CCMP<br/>AES-CMAC-128<br/>SMS4<br/>GCMP<br/>GCMP256<br/>AES-GMAC-128<br/>AES-GMAC-256<br/>unknown | Encryption method for multicast and broadcast              |
| `.wifi.phy`                      | string                           | bgn                                                          | Physical layer specification                                |
| `.wifi.wps`                      | boolean                          | true or false                                                | Wi-Fi Protected Setup status                                |
| `.wifi.country`                  | string                           | 2 characters                                                 | Wi-Fi country code for regulatory domain                    |
| `.wifi.mac`                      | string                           | 12 upper-case hexadecimal letters                           | MAC address of network interface controller                 |
| `.wifi.ip`                       | string                           | IPv4 format                                                  | IPv4 address assigned to interface                          |
| `.wifi.mask`                     | string                           | IPv4 format                                                  | Network mask for subnet division                            |
| `.wifi.gateway`                  | string                           | IPv4 format                                                  | Gateway IP address for external networks                    |
| `.wifi.dns`                      | string                           | IPv4 format                                                  | DNS server IP address                                       |
| `.wifi.status`                   | string                           | OK<br/>Error<br/>Disabled<br/>Disconnected                 | Wi-Fi interface status                                      |
| `.wifi.mode`                     | string                           | STA                                                          | Wi-Fi operating mode                                        |
| `.ethernet.mac`                  | string                           | 12 upper-case hexadecimal letters                           | Ethernet interface MAC address                              |
| `.ethernet.ip`                   | string                           | IPv4 format                                                  | Ethernet IPv4 address                                       |
| `.ethernet.mask`                 | string                           | IPv4 format                                                  | Ethernet network mask                                       |
| `.ethernet.gateway`              | string                           | IPv4 format                                                  | Ethernet gateway IP                                         |
| `.ethernet.dns`                  | string                           | IPv4 format                                                  | Ethernet DNS server IP                                      |
| `.ethernet.status`               | string                           | Up<br/>Down                                                  | Ethernet interface status                                   |
| `.sd_card.installed`             | boolean                          |                                                              | Is a microSD card installed in the system                   |
| `.sd_card.type`                  | string                           |                                                              | Type of microSD card                                        |
| `.sd_card.size`                  | uint                             |                                                              | Logical size of the microSD card                            |
| `.sd_card.speed`                 | uint                             |                                                              | Card bus frequency in MHz                                   |
