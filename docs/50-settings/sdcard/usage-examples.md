---
title: Usage Examples
category: concepts
tags:
- sdcard
- usage_examples
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Usage examples

This section provides practical examples of working with the SD card endpoint.

## Document Context

- **Purpose**: Practical SD card HTTP interface examples with ready-to-run scripts for common file management operations
- **When to use**: Learning SD card API usage, implementing file management automation, building data retrieval workflows
- **Prerequisites**: Basic cURL knowledge, understanding of HTTP responses, SD card with sample data available
- **Related to**: API documentation (listing.md, download.md, delete.md), automation scripting, data processing workflows
- **Validates against**: Real SD card operations, HTTP response patterns, practical integration scenarios

## Key Facts

- **Operations covered**: Directory listing, file download, file deletion - Complete SD card management workflow
- **Response formats**: JSON for listings, raw file content for downloads, status codes for confirmations
- **File patterns**: CSV reports with YYYYMMDD.CSV naming, directory structure navigation examples
- **Automation ready**: Copy-paste cURL commands, real device responses, error handling examples
- **Integration**: Suitable for scripts, monitoring systems, automated data collection workflows

## Basic Operations

### List SD Card Contents

```bash
curl -s http://192.168.1.100/sdcard/
```

**Response:**

```json
{
  "path": "/sdcard/",
  "files": [
    {"name":"NIHAO.TXT","size":13,"type":"file"},
    {"name":"SYSTEM~1","size":0,"type":"dir"},
    {"name":"20240924.CSV","size":493074,"type":"file"}
  ]
}
```

### Download a CSV File

View content:

```bash
curl -s http://192.168.1.100/sdcard/20241010.CSV
```

Save to disk:

```bash
curl -O http://192.168.1.100/sdcard/20241010.CSV
```

**Sample CSV content:**

```csv
RID,TIME,MID,MSTAT,TARIFF,PF,EAP_T,EAP_T1,EAP_T2,EAN_T,EAN_T1,EAN_T2,...
1,"2024-10-10T05:01:36Z","220000399","OK",2,0.169,29.424,20.841,8.583,...
```

### Delete Files

Delete a specific file:

```bash
curl -i -X DELETE http://192.168.1.100/sdcard/20241010.CSV
```

Returns `204` status code on success.

## Advanced Script: Download CSV Files from Date Range

CSV files with reports are saved in the `YYYYMMDD.CSV` format. This script downloads all CSV files within a specified date range.

### Script Arguments

- **Argument 1**: Device IP address
- **Argument 2**: Start date (YYYY-MM-DD)
- **Argument 3**: End date (YYYY-MM-DD)

### Script Source Code

```bash title="download_csv.sh"
#!/usr/bin/env bash

if [ $# -ne 3 ]; then
    echo "Usage: $0 <device_ip> <start_date> <end_date>"
    exit 1
fi

DEVICE_IP="$1"
START_DATE="$2"
END_DATE="$3"

# Validate dates

if ! date -d "$START_DATE" &>/dev/null; then
    echo "Invalid start date: $START_DATE"
    exit 1
fi

if ! date -d "$END_DATE" &>/dev/null; then
    echo "Invalid end date: $END_DATE"
    exit 1
fi

# Convert dates to integers for comparison
START_DATE_INT=$(date -d "$START_DATE" +%Y%m%d)
END_DATE_INT=$(date -d "$END_DATE" +%Y%m%d)

if [ $START_DATE_INT -gt $END_DATE_INT ]; then
    echo "Error: start date is later than end date."
    exit 1
fi

# Get file list from device
FILE_LIST_JSON=$(curl -s "http://$DEVICE_IP/sdcard/")

if [ -z "$FILE_LIST_JSON" ]; then
    echo "No response or SD card unavailable."
    exit 1
fi

# Extract CSV files in YYYYMMDD.CSV format
CSV_FILES=$(echo "$FILE_LIST_JSON" | jq -r '.files[] | select(.type=="file") | .name' | grep -E '^[0-9]{8}\.CSV$')

if [ -z "$CSV_FILES" ]; then
    echo "No CSV files found in YYYYMMDD.CSV format."
    exit 0
fi

# Download files within date range
for file in $CSV_FILES; do
    DATE_PART="${file%.*}"
    YEAR=${DATE_PART:0:4}
    MONTH=${DATE_PART:4:2}
    DAY=${DATE_PART:6:2}
    FILE_DATE_INT=$(( 10#$YEAR * 10000 + 10#$MONTH * 100 + 10#$DAY ))

    if [ $FILE_DATE_INT -ge $START_DATE_INT ] && [ $FILE_DATE_INT -le $END_DATE_INT ]; then
        echo "Downloading: $file"
        curl -s -O "http://$DEVICE_IP/sdcard/$file" || echo "Error downloading $file"
    fi
done

echo "Done."
```

### Make Script Executable

```bash
chmod +x download_csv.sh
```

### Usage Examples

```bash
# Download files from September 2024
./download_csv.sh 192.168.1.100 2024-09-01 2024-09-30

# Download files from a single day
./download_csv.sh 192.168.1.100 2024-10-07 2024-10-07
```

**Expected output:**

```txt
Downloading: 20240924.CSV
Downloading: 20240925.CSV
Downloading: 20240928.CSV
Downloading: 20240929.CSV
Downloading: 20240930.CSV
Done.
```

## Error Handling Examples

### SD Card Not Available

```bash
curl -s http://192.168.1.100/sdcard/
# Returns 503 Service Unavailable if SD card is not mounted
```

### File Not Found

```bash
curl -i http://192.168.1.100/sdcard/nonexistent.csv
# Returns 404 Not Found
```

### Invalid Delete Operation

```bash
curl -i -X DELETE http://192.168.1.100/sdcard/
# Returns 400 Bad Request (cannot delete root directory)
```
