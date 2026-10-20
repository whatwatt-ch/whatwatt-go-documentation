---
title: Firewall Settings
category: concepts
tags:
- firewall
- networking
- cloud
difficulty: beginner
device_compatibility:
- all
last_verified: '2026-10-20'
real_device_tested: false
---

# Firewall Settings

Use this guide when a firewall restricts Internet access for whatwatt Go, the mobile app, or the web cockpit.
Each component needs access to the cloud from the network where it runs.

## Key Facts

- **Direction**: Allow outbound connections and their return traffic through the firewall.
- **Device connection**: HTTPS discovers the cloud broker; MQTT then connects to the returned destination.
- **Separate clients**: The device, mobile app, and web cockpit use different MQTT ports.
- **Local integration**: A user-configured MQTT broker has its own address and port.
- **Offline storage**: Local SD card logging is available without a cloud connection.

## whatwatt Cloud Connections

### Device Connection Sequence

The device connects to the cloud in two steps:

1. It contacts `app.whatwatt.ch` over HTTPS on TCP port **443** to obtain its MQTT broker address and port.
2. It connects to the MQTT broker using the destination returned by that service.

Both steps must succeed. Allowing HTTPS alone does not enable cloud reporting.
Allowing the MQTT port alone is insufficient if the device cannot obtain its broker address.

### Outbound Access by Component

The current production MQTT port assignments are:

| Source | Destination | Protocol / destination port | Purpose |
|--------|-------------|-----------------------------|---------|
| whatwatt Go | `app.whatwatt.ch` | HTTPS / TCP **443** | Obtain the device's cloud broker address and port |
| whatwatt Go | Assigned cloud MQTT broker | MQTT over TLS / TCP **8883**, or the port returned by the service | Device cloud communication and energy reports |
| Mobile app | Cloud MQTT broker | TCP **8884** | App communication with the cloud |
| Web cockpit browser | Cloud MQTT broker | TCP **8885** | Cockpit communication with the cloud |

The MQTT rules for the mobile app and web cockpit complement the HTTPS access those applications need.
This table covers device broker discovery and the MQTT connections relevant to cloud access;
it is not a complete inventory of every application service or optional integration.

Apply each rule to the network of the component that initiates the connection.
For example, a phone connected to corporate Wi-Fi needs the mobile app's cloud access from that Wi-Fi network.
Allowing only the device's traffic does not provide access for the phone or the browser.

!!! important "Broker addresses and ports can change"
    `mqtt-01.whatwatt.ch:8883` is an example of the current device broker destination, not a permanent assignment.
    Additional brokers and different ports may be introduced. Use the destination supplied by the cloud service
    for the device. If your firewall requires a fixed allowlist, confirm the supported broker hostnames and ports
    with whatwatt support and keep that allowlist up to date. Avoid rules tied to a single resolved IP address.

These connections are initiated by the device, app, or browser.
They do not require inbound port forwarding from the Internet to whatwatt Go.
Opening ports 8884 and 8885 only for the device does not enable the app or cockpit connections.

## DNS and Time Synchronization

The device also needs access to the network services used by its configuration:

| Service | Destination | Typical destination port | Requirement |
|---------|-------------|--------------------------|-------------|
| DNS | Configured DNS server | UDP/TCP **53** | Resolve the cloud service and broker hostnames |
| Time synchronization | Selected NTP server | UDP **123** | Maintain correct device time for secure connections and timestamps |

DNS and NTP servers may be provided by the local network.
An internal NTP server can be configured in [Device Settings](../50-settings/settings.md).
When the device uses public NTP servers, the firewall must permit access to the selected servers.

## Local MQTT and Other Local Interfaces

The configurable [MQTT client](../30-mqtt/mqtt-client.md) publishes to a broker chosen by the user.
Its destination is independent of the whatwatt cloud broker.
Allow access to the address and port configured for that integration.

For a self-hosted broker, also configure its inbound firewall rules to accept the intended clients.
The port **8883** examples in [Production Hardening](../40-secure-mqtt/hardening.md#firewall-configuration)
apply to that broker. They are not a complete set of whatwatt cloud access rules.

Keep REST, Modbus TCP, and other local interfaces accessible only to the local clients that need them.
Cloud connectivity does not require exposing those interfaces to the Internet.

## Troubleshooting Cloud Access

1. **Check the local network.** Confirm that the device has an IP address, a default gateway, and a working DNS server.
2. **Check HTTPS access.** Confirm that the device's network can reach `app.whatwatt.ch` on TCP port 443.
3. **Check the assigned broker.** Allow the broker hostname and destination port supplied for the device.
4. **Check the app and browser separately.** Confirm outbound access to their MQTT ports from their own networks.
5. **Check time synchronization.** Confirm that the selected NTP server is reachable and the device time is correct.
6. **Check device cloud status.** Read `/api/v1/system` and inspect `clouds.whatwatt.enabled`,
   `clouds.whatwatt.connected`, and `clouds.whatwatt.registered` when present.
   See [System Info](system-info.md) for access and authentication examples.

A Wi-Fi or Ethernet connection proves local network access; it does not prove that every cloud connection succeeds.
Successful device cloud status also does not prove that the app or browser can reach the cloud.
If setup still fails, reproduce the problem and review the firewall's blocked outbound connections
for the device, phone, and browser separately. App diagnostic logs can help whatwatt support identify
which cloud connection is failing.

## Operation Without Internet Access

Cloud reporting and cloud access from the app or web cockpit require their cloud connections.
For local data collection, see [SD Card Configuration](../50-settings/sdcard/configuration.md)
and [SD Recorder Mode](../50-settings/sdcard/recorder-mode.md).
Configure and verify local logging before leaving the device to collect data offline.
