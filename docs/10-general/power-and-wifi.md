---
title: Power And Wifi
category: concepts
tags:
- power_and_wifi
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---


# Power And Wifi

## Document Context

- **Purpose**: Explains power management considerations when using WhatWatt Go with Wi-Fi connectivity and meter-supplied power (M-Bus)
- **When to use**: Device installation planning, power troubleshooting, Wi-Fi connectivity issues, system optimization
- **Prerequisites**: Basic understanding of M-Bus power supply, Wi-Fi networking concepts, device power requirements
- **Related to**: Meter communication settings, Wi-Fi configuration, API polling frequency, service management
- **Validates against**: Device voltage monitoring via .device.plug.v_scap field in system responses

## Key Facts

- **Power source**: M-Bus interface from energy meter (limited power budget)
- **Critical voltage**: Monitor .device.plug.v_scap - maintain above 4.5V
- **Wi-Fi impact**: Distance to router affects power consumption significantly
- **API frequency**: Frequent HTTP calls can cause power-related shutdowns
- **Service optimization**: Disable unnecessary services to reduce power draw
- **MQTT considerations**: Cloud connectivity may require power management
- **Troubleshooting**: Device shutdown indicates power budget exceeded
- **Best practices**: Balance functionality with available power resources

## Device connected via Wi-Fi and powered by the meter

When powering the device via the meter interface only (especially via MBUS) and using Wi-Fi, keep in mind the limited power resources of the device. Do not call the HTTP API too often because in extreme cases the system will shut down for a certain period of time.

If you notice that the device turns off when working with the cloud via MQTT, disable unnecessary services and reduce the frequency of sending reports.

Also keep in mind that the distance from the Wi-Fi router matters in regards to the energy consumption.

!!! warning "Power Management"
    - Avoid frequent HTTP API calls when powered via M-Bus
    - Monitor `.device.plug.v_scap` voltage - should not drop below 4.5V
    - Reduce service frequency and disabled unnecessary services if voltage drops
    - Consider Wi-Fi router distance for power efficiency
