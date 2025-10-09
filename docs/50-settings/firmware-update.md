---
title: Firmware Update
category: concepts
tags:
- firmware_update
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Firmware Update

## Document Context

- **Purpose**: Guides through remote firmware update procedures for whatwatt Go device via HTTP upload interface
- **When to use**: When planning or executing firmware upgrades without physical device access
- **Prerequisites**: Administrative access rights, firmware binary file from whatwatt support
- **Related to**: Factory reset procedures, system information endpoints, device restart methods
- **Validates against**: Real firmware upgrade sequences with update verification steps

## Key Facts

- **Endpoint**: `/update` (HTTP POST for firmware upload)
- **Methods**: POST (multipart/form-data), GET (update status)
- **Authentication**: Admin credentials required for firmware modifications
- **Response format**: JSON status with progress indicators and error messages
- **Error codes**: File validation errors, insufficient storage, update failure states

--8<-- "../_partials/auth-note.md"

!!! note "Alternative Method"
    Firmware updates can also be performed from the WebUI of the device for easier manual updates.

## Endpoint Details

This endpoint allows you to update the device firmware. The firmware file should be sent in `multipart/form-data` format.

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `/load` |
| **Method** | `POST` |
| **Content Type** | `multipart/form-data` |
| **Response Content Type** | `text/plain` |

## Update Process

### Request Format

The firmware file must be uploaded using the `multipart/form-data` format with the field name `file`.

### Example

```bash
curl -i -F file=@upgrade_file.bin http://192.168.1.100/load
```

### Parameters

- `-F file=@upgrade_file.bin`: Uploads the file `upgrade_file.bin` from the current directory
- `-i`: Include response headers in output
- Replace `192.168.1.100` with your device's IP address
- Replace `upgrade_file.bin` with the actual firmware file name

### Response

The server will respond with status information about the upload and update process.

!!! note "Reboot after successful update"
    After the firmware is uploaded and verified, the device automatically reboots to apply the new version. This is the only routine scenario that requires a reboot. See [Device Restart](restart.md) for reboot behavior and expected downtime.

## Important Considerations

!!! warning "Firmware Update Safety"
    - Ensure the firmware file is specifically designed for your device model
    - Do not interrupt the update process once started
    - The device will reboot automatically after a successful update (routine and expected)
    - Keep the device powered during the entire update process

!!! info "File Format Requirements"
    - Firmware files typically have `.bin` extension
    - Only use firmware files provided by the device manufacturer
    - Verify file integrity before upload if checksums are provided

## Multipart/Form-Data Background

`multipart/form-data` is a media type used to encode files and other form data when uploading via HTTP POST requests. This format:

- Splits form data into multiple parts separated by boundaries
- Encodes each part with its own content type and disposition metadata
- Enables robust handling of binary data and complex file uploads
- Was standardized in RFC 2388 (1998) to overcome limitations of `application/x-www-form-urlencoded`

This format allows each part of the form to be processed independently, making it ideal for file uploads like firmware updates.

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| File not found | Check the file path and ensure the firmware file exists |
| Permission denied | Verify you have read access to the firmware file |
| Connection timeout | Check network connectivity to the device |
| Invalid firmware | Ensure the firmware is compatible with your device model |

### Example Error Responses

```bash
# File too large
HTTP/1.1 413 Payload Too Large

# Invalid file format
HTTP/1.1 400 Bad Request

# Device busy
HTTP/1.1 503 Service Unavailable
```

## Best Practices

1. **Backup Settings**: Save current device configuration before updating
2. **Stable Power**: Ensure reliable power supply during update
3. **Network Stability**: Use wired connection if possible
4. **Verify Version**: Check current firmware version before and after update
5. **Test Functionality**: Verify device operation after successful update
