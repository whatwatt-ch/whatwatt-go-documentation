---
title: SD Recorder Mode
category: concepts
tags:
- sdcard
- recorder_mode
- offline
- standalone
difficulty: intermediate
device_compatibility:
- WW_Go_2.0.1+
- all
last_verified: '2025-11-17'
---

# SD Recorder Mode

## Document Context

- **Purpose**: Standalone operation mode for logging meter reports to SD card without network connectivity or USB-C power
- **When to use**: Off-grid installations, temporary deployments, backup logging without network infrastructure
- **Prerequisites**: FAT32-formatted SD card, initial device configuration via network, understanding of LED indicator patterns
- **Related to**: [SD card configuration](configuration.md), [Device settings](../settings.md), [Power management](../../10-general/power-and-wifi.md)
- **Validates against**: Firmware 2.0.1+ requirements, SD card mount behavior, LED status indicators

## Key Facts

- **Availability**: Firmware 2.0.1 and newer
- **Power source**: Meter interface only (no USB-C in recorder mode)
- **Configuration**: `services.sd.recorder_mode: true` via REST API before deployment
- **LED indicators**: Green (OK), Red (meter comm error), Blinking (SD card issue)
- **Unmount time**: 200 seconds window after 3-6s button press
- **Data format**: Standard CSV reports with configurable frequency (1-1440 seconds)

## Overview

SD Recorder Mode enables the whatwatt Go device to operate standalone, powered solely by the meter interface and logging reports to SD card without network connectivity or USB-C power. This mode is ideal for:

- Off-grid installations without network infrastructure
- Temporary deployments requiring local data collection
- Backup logging independent of network availability
- Field testing and data collection scenarios

!!! warning "Firmware Requirement"
    SD Recorder Mode requires firmware version 2.0.1 or newer.

!!! important "Pre-Configuration Required"
    The device must be configured via network (Wi-Fi or Ethernet) before deploying in recorder mode. Once activated, the device operates offline without network access.

## Setup Procedure

### 1. Prepare SD Card

Insert a FAT32-formatted SD card into the device. Most new SD cards come pre-formatted in FAT32.

!!! tip "SD Card Format"
    If your card needs formatting, use FAT32 file system. Most cards up to 32GB are formatted as FAT32 by default.

### 2. Initial Network Connection

Connect the device to your network using either:

- **Wi-Fi**: Configure via [Wi-Fi setup](../wifi-setup.md)
- **Ethernet**: Connect via LAN cable

Power the device via USB-C during configuration.

### 3. Configure Device Settings

Set up all required device parameters while connected to the network:

- Meter communication parameters
- Time synchronization
- Any other application-specific settings

### 4. Enable SD Recorder Mode

Activate recorder mode via the settings API:

```bash
curl -i -X PUT \
  -H "Content-Type: application/json" \
  -d '{"services":{"sd":{"recorder_mode":true,"frequency":15,"enable":true}}}' \
  http://192.168.99.114/api/v1/settings
```

**Configuration parameters:**

| Parameter | Value | Description |
|-----------|-------|-------------|
| `recorder_mode` | `true` | Enable standalone SD recorder mode |
| `frequency` | `15` | Report logging interval in seconds (1-1440) |
| `enable` | `true` | Enable SD card logging service |

!!! tip "Test First"
    Start with a shorter frequency (e.g., 15 seconds) to verify proper operation before deploying for longer periods.

### 5. Remove Wi-Fi Settings (Optional)

If the device was connected via Wi-Fi, clear the Wi-Fi configuration to ensure it doesn't attempt reconnection:

**Via WebUI:**
- Navigate to **Reset WiFi Settings**

**Via REST API:**
```bash
curl -i -X DELETE http://192.168.99.114/api/v1/wifi/sta/settings
```

### 6. Deploy in Recorder Mode

1. **Disconnect** the meter interface from the device
2. **Disconnect** USB-C power cable
3. Wait for the LED to turn off completely
4. **Connect** the device to the meter interface (do not connect USB-C)
5. Wait for the LED to illuminate

## LED Status Indicators

The device uses LED patterns to indicate operational status in recorder mode:

| LED Pattern | Meaning | Action Required |
|-------------|---------|-----------------|
| **Solid Green** | Normal operation - meter communication OK, SD card mounted | None - device is logging properly |
| **Solid Red** | Meter communication error | Check meter interface connection and configuration |
| **Blinking** | SD card mounting issue | Check SD card insertion, format, or try different card |

!!! warning "Green LED ≠ Guaranteed Logging"
    A green LED indicates successful meter communication and SD card mounting, but doesn't guarantee that reports are being written correctly. Always verify data logging with a short test run before long-term deployment.

## Verification Procedure

Before deploying for extended periods:

1. Run the device in recorder mode for a short test period (e.g., 5-10 minutes)
2. Safely unmount the SD card (see below)
3. Check that CSV files are being created with expected data
4. Verify file timestamps and content match your configuration
5. Ensure sufficient SD card space for your deployment duration

!!! tip "Storage Planning"
    Calculate required storage: With 15-second intervals, expect approximately 5,760 reports per day. Each report is typically 100-200 bytes, requiring ~1MB per day.

## SD Card Management

### Safe Unmount Procedure

To remove the SD card without waiting for device shutdown:

1. **Press and hold** the device button for **3-6 seconds**
2. LED will start **blinking** to indicate unmount mode
3. You have **200 seconds** to safely remove the SD card
4. Remove the card during this window

!!! warning "Unmount Timeout"
    After 200 seconds, the device will attempt to remount the card automatically. Remove the card promptly after initiating unmount.

### Remounting SD Card

After removing the card, to remount it:

**Option 1: Automatic remount**
1. Insert the SD card back into the slot
2. Wait for automatic detection and mounting

**Option 2: Manual remount trigger**
1. Insert the SD card
2. Press and hold the button for 3-6 seconds
3. Device will attempt to mount the card immediately

### Data Retrieval

Periodically transfer data from the SD card:

1. Safely unmount as described above
2. Remove card and read using a card reader
3. Copy CSV files to backup storage
4. Optionally delete old files to free space
5. Reinsert card and remount

!!! tip "Regular Backups"
    Establish a regular schedule for data retrieval to prevent SD card capacity issues and ensure data is backed up.

## Button Behavior

Button functionality differs between normal and recorder modes:

| Mode | Button Behavior |
|------|-----------------|
| **Normal Mode** | Standard functions (factory reset, Wi-Fi config, etc.) |
| **Recorder Mode** | SD card unmount/mount trigger only (3-6s press) |

!!! note "Limited Button Functions"
    In recorder mode, normal button functions (like factory reset or WPS) are disabled. Only SD card unmount/mount is available via button press.

## Return to Normal Operation

To exit recorder mode and return to normal network-connected operation:

1. Remove the meter interface connection
2. Connect USB-C power cable
3. The device will boot in normal mode
4. Reconfigure network settings as needed
5. Optionally disable recorder mode via API:

```bash
curl -i -X PUT \
  -H "Content-Type: application/json" \
  -d '{"services":{"sd":{"recorder_mode":false}}}' \
  http://192.168.99.114/api/v1/settings
```

## Troubleshooting

### LED Stays Red

**Problem**: Solid red LED after connecting to meter

**Possible causes:**
- Meter interface not properly connected
- Incorrect meter communication settings
- Incompatible meter type
- Damaged meter interface cable

**Solutions:**
1. Verify physical connections
2. Test with USB-C power and network to check meter settings
3. Review meter communication configuration
4. Try different meter interface cable

### LED Blinking

**Problem**: Blinking LED pattern

**Possible causes:**
- SD card not properly inserted
- SD card not formatted as FAT32
- Corrupted or defective SD card
- SD card capacity issues

**Solutions:**
1. Reinsert SD card ensuring proper seating
2. Format card as FAT32 (backup data first)
3. Try a different SD card
4. Verify card has sufficient free space

### No Data on SD Card

**Problem**: LED shows green but CSV files are missing or empty

**Possible causes:**
- SD card write errors
- Insufficient free space
- Incorrect frequency configuration
- Meter not providing valid data

**Solutions:**
1. Check SD card free space
2. Verify `frequency` setting is reasonable (15-60 seconds recommended)
3. Test device in normal mode to verify meter communication
4. Format SD card and retry with shorter test duration

### Button Doesn't Respond

**Problem**: Pressing button for 3-6 seconds doesn't trigger unmount

**Possible causes:**
- Button held for incorrect duration (too short or too long)
- Device in error state
- Hardware button issue

**Solutions:**
1. Ensure 3-6 second press duration (count slowly: "one thousand one, one thousand two...")
2. Verify LED responds to button press with blinking pattern
3. If no response, disconnect power completely and reconnect

## Best Practices

1. **Always test first**: Run a short verification period before long-term deployment
2. **Monitor storage**: Calculate expected data volume and ensure adequate SD card capacity
3. **Regular backups**: Establish schedule for periodic data retrieval
4. **Green LED verification**: Don't trust green LED alone - verify actual data logging
5. **Clean shutdown**: Always use safe unmount procedure before removing SD card
6. **Spare cards**: Keep formatted spare SD cards for quick field replacement
7. **Documentation**: Record configuration settings and deployment dates
8. **Capacity planning**: Leave 20% free space buffer on SD card for write operations

## Related Configuration

See also:

- [SD Card Configuration](configuration.md) - Basic SD logging setup
- [CSV Format](csv-format.md) - Report file structure
- [Device Settings](../settings.md) - Complete settings reference
- [File Listing](listing.md) - Browsing SD card contents
- [Download Files](download.md) - Retrieving CSV reports
