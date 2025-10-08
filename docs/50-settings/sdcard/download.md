---
title: Download — retrieve files
category: concepts
tags:
- sdcard
- download
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Download — retrieve files

## Document Context

- **Purpose**: SD card file download API for retrieving CSV reports and other files with appropriate MIME type handling
- **When to use**: Downloading meter data CSV files, retrieving stored reports, backing up configuration files
- **Prerequisites**: SD card with files available, knowledge of target filenames, HTTP download mechanisms
- **Related to**: File listing (listing.md), CSV format specification (csv-format.md), data logging configuration
- **Validates against**: File existence on SD card, MIME type detection by extension, HTTP content delivery standards

## Key Facts

- **Endpoint**: GET `/sdcard/filename.ext` - Download specific file by exact filename
- **MIME types**: text/csv for CSV reports, appropriate types based on file extension
- **Download methods**: Direct browser access, cURL with -O flag for filename preservation
- **Content**: Raw file data with proper Content-Type headers for client handling
- **CSV format**: Structured meter data with timestamps, measurements, and status information

Download files directly via HTTP. For CSV reports the device serves `text/csv`; for other files the MIME type depends on extension.

## Request

```http
GET /sdcard/<filename.ext>
```

### Examples

View content:

```bash
curl -s http://192.168.1.100/sdcard/20241010.CSV
```

Save to disk:

```bash
curl -O http://192.168.1.100/sdcard/20241010.CSV
```

!!! tip "Download with curl"
    Use `-O` to keep the original filename. You can also download from the browser at `http://<device_ip>/sd.html`.

### Sample CSV

```csv
RID,TIME,MID,MSTAT,TARIFF,PF,EAP_T,EAP_T1,EAP_T2,EAN_T,EAN_T1,EAN_T2,...
1,"2024-10-10T05:01:36Z","220000399","OK",2,0.169,29.424,20.841,8.583,...
4,"2024-10-10T05:01:55Z","220000399","OK",2,0.23,29.424,20.841,8.583,...
```
