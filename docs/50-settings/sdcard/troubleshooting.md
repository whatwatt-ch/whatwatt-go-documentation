---
title: Troubleshooting
category: troubleshooting
tags:
- sdcard
- troubleshooting
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---


# Troubleshooting

Common issues and their resolutions.

## Document Context

- **Purpose**: SD card HTTP interface troubleshooting guide for resolving common file operation issues and error conditions
- **When to use**: Debugging SD card access problems, resolving mount issues, fixing file operation errors
- **Prerequisites**: Basic HTTP status code knowledge, SD card hardware concepts, file system troubleshooting experience
- **Related to**: SD card operations ([Listing](listing.md), [Download](download.md), [Delete](delete.md)), system configuration, hardware diagnostics
- **Validates against**: HTTP error response patterns, SD card mount behavior, file system operation requirements

## Key Facts

- **Error types**: 503 (card unmounted), 404 (file missing), 400 (invalid operation)
- **Mount issues**: SD card presence required, mount failures need reboot resolution
- **Path requirements**: Directory paths must end with `/`, exact filename matching required
- **File naming**: CSV files follow YYYYMMDD.CSV pattern for date-based organization
- **Quick access**: Browser interface at `/sd.html` for manual inspection and verification

| HTTP status | Meaning | Likely cause | Fix |
|-------------|---------|--------------|-----|
| 503 Service Unavailable | SD card not mounted | No SD card present or mount failed | Insert/replace card; reboot if needed |
| 404 Not Found | File/directory missing | Wrong path or deleted | List parent directory and verify name |
| 400 Bad Request | Invalid operation | Attempted to delete root or malformed path | Use a specific file/dir path |

## Tips

- Ensure directory listing paths end with `/`
- CSV files follow `YYYYMMDD.CSV` naming
- Use browser at `/sd.html` for quick inspection
