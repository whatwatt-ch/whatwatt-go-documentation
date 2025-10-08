---
title: Appendix D
category: concepts
tags:
- appendix_d
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---


# OBIS Codes Reference

## Document Context

- **Purpose**: Comprehensive OBIS code reference for DLMS/COSEM smart meter data identification including energy, power, voltage, and current measurements
- **When to use**: Configuring meter scalers, interpreting meter data, setting up MQTT templates, troubleshooting DLMS communication
- **Prerequisites**: Understanding of DLMS/COSEM protocol, smart meter concepts, electrical measurement terminology
- **Related to**: Meter scalers (scalers-current.md, scalers-custom.md), meter communication (meter-comm.md), MQTT templates
- **Validates against**: DLMS/COSEM standard specifications, IEC 62056 series, smart meter manufacturer implementations

## Key Facts

- **Standard**: DLMS/COSEM Object Identification System for standardized meter data access
- **Categories**: Energy (1.8.x, 2.8.x), reactive energy (3.8.x, 4.8.x), instantaneous power (1.7.x, 2.7.x), voltage/current (32.7.x, 31.7.x)
- **Tariff support**: Multi-tariff measurements (T1, T2) and total values (T0)
- **Phase identification**: L1, L2, L3 phase-specific measurements for three-phase systems
- **Units**: Wh (energy), W (power), var/varh (reactive), V (voltage), A (current)

The following table provides a description of selected OBIS codes used in energy metering systems. These codes are standardized identifiers for various energy measurements and meter parameters according to the DLMS/COSEM standard.

## Energy Values

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 1.8.0 | Positive active energy (A+) total | Wh |
| 1.8.1 | Positive active energy (A+) in tariff T1 | Wh |
| 1.8.2 | Positive active energy (A+) in tariff T2 | Wh |
| 2.8.0 | Negative active energy (A-) total | Wh |
| 2.8.1 | Negative active energy (A-) in tariff T1 | Wh |
| 2.8.2 | Negative active energy (A-) in tariff T2 | Wh |

## Reactive Energy

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 3.8.0 | Positive reactive energy (Q+) total | varh |
| 3.8.1 | Positive reactive energy (Q+) in tariff T1 | varh |
| 3.8.2 | Positive reactive energy (Q+) in tariff T2 | varh |
| 4.8.0 | Negative reactive energy (Q-) total | varh |
| 4.8.1 | Negative reactive energy (Q-) in tariff T1 | varh |
| 4.8.2 | Negative reactive energy (Q-) in tariff T2 | varh |

## Quadrant Energy

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 5.8.0 | Imported inductive reactive energy in 1st quadrant (Q1) total | varh |
| 5.8.1 | Imported inductive reactive energy in 1st quadrant (Q1) in tariff T1 | varh |
| 5.8.2 | Imported inductive reactive energy in 1st quadrant (Q1) in tariff T2 | varh |
| 6.8.0 | Imported capacitive reactive energy in 2nd quadrant (Q2) total | varh |
| 6.8.1 | Imported capacitive reactive energy in 2nd quadrant (Q2) in tariff T1 | varh |
| 6.8.2 | Imported capacitive reactive energy in 2nd quadrant (Q2) in tariff T2 | varh |
| 7.8.0 | Exported inductive reactive energy in 3rd quadrant (Q3) total | varh |
| 7.8.1 | Exported inductive reactive energy in 3rd quadrant (Q3) in tariff T1 | varh |
| 7.8.2 | Exported inductive reactive energy in 3rd quadrant (Q3) in tariff T2 | varh |
| 8.8.0 | Exported capacitive reactive energy in 4th quadrant (Q4) total | varh |
| 8.8.1 | Exported capacitive reactive energy in 4th quadrant (Q4) in tariff T1 | varh |
| 8.8.2 | Exported capacitive reactive energy in 4th quadrant (Q4) in tariff T2 | varh |

## Maximum Demand

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 1.6.0 | Positive active maximum demand (A+) total | Wh |
| 1.6.1 | Positive active maximum demand (A+) in tariff T1 | Wh |
| 1.6.2 | Positive active maximum demand (A+) in tariff T2 | Wh |
| 2.6.0 | Negative active maximum demand (A-) total | Wh |
| 2.6.1 | Negative active maximum demand (A-) in tariff T1 | Wh |
| 2.6.2 | Negative active maximum demand (A-) in tariff T2 | Wh |

## Instantaneous Power

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 1.7.0 | Positive active instantaneous power (A+) | W |
| 21.7.0 | Positive active instantaneous power (A+) in phase L1 | W |
| 41.7.0 | Positive active instantaneous power (A+) in phase L2 | W |
| 61.7.0 | Positive active instantaneous power (A+) in phase L3 | W |
| 2.7.0 | Negative active instantaneous power (A-) | W |
| 22.7.0 | Negative active instantaneous power (A-) in phase L1 | W |
| 42.7.0 | Negative active instantaneous power (A-) in phase L2 | W |
| 62.7.0 | Negative active instantaneous power (A-) in phase L3 | W |

## Reactive Power

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 3.7.0 | Positive reactive instantaneous power (Q+) | var |
| 23.7.0 | Positive reactive instantaneous power (Q+) in phase L1 | var |
| 43.7.0 | Positive reactive instantaneous power (Q+) in phase L2 | var |
| 63.7.0 | Positive reactive instantaneous power (Q+) in phase L3 | var |
| 4.7.0 | Negative reactive instantaneous power (Q-) | var |
| 24.7.0 | Negative reactive instantaneous power (Q-) in phase L1 | var |
| 44.7.0 | Negative reactive instantaneous power (Q-) in phase L2 | var |
| 64.7.0 | Negative reactive instantaneous power (Q-) in phase L3 | var |

## Voltage and Current

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 9.7.0 | Apparent instantaneous power (S+) | VA |
| 32.7.0 | Instantaneous voltage (U) in phase L1 | V |
| 52.7.0 | Instantaneous voltage (U) in phase L2 | V |
| 72.7.0 | Instantaneous voltage (U) in phase L3 | V |
| 31.7.0 | Instantaneous current (I) in phase L1 | A |
| 51.7.0 | Instantaneous current (I) in phase L2 | A |
| 71.7.0 | Instantaneous current (I) in phase L3 | A |

## Meter Information

| **OBIS Code** | **Description** | **Unit** |
|---------------|-----------------|----------|
| 96.1.0 | Meter identifier | |
| 96.1.1 | Meter model | |
| 42.0.0 | Meter identifier (alternative) | |
| 96.14.0 | Current tariff | |
| 13.7.0 | Instantaneous power factor | |

!!! note "OBIS Standard"
    OBIS (Object Identification System) codes are part of the DLMS/COSEM standard for smart meter communication. These codes provide a standardized way to identify and access various energy measurements and meter parameters.
