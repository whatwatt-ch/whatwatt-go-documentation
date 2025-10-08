---
title: Delete — files and directories
category: concepts
tags:
- delete
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Delete — files and directories

## Document Context

- **Purpose**: SD card file and directory deletion API with recursive directory removal capabilities
- **When to use**: Cleaning up log files, removing old data, managing SD card storage space, maintenance operations
- **Prerequisites**: SD card mounted and accessible, understanding of recursive deletion risks, proper file path knowledge
- **Related to**: SD card listing (listing.md), file download (download.md), SD card configuration (configuration.md)
- **Validates against**: SD card filesystem structure, path validation, directory traversal safety

## Key Facts

- **Endpoint**: DELETE `/sdcard/[path/]filename.ext` - Remove specific files or directories
- **Method**: DELETE only - Returns 204 No Content on successful deletion
- **Recursion**: Directory deletion removes all contained files and subdirectories
- **Path format**: File paths relative to SD card root, trailing slash for directories
- **Safety**: Irreversible operation requiring careful path validation

Delete files or directories recursively.

## Requests

```http
DELETE /sdcard/[path/]<filename.ext>
DELETE /sdcard/path/[path/]
```

!!! warning "Recursive delete"
    Deleting a directory removes all files and subdirectories it contains.

### Examples

Delete file:

```bash
curl -i -X DELETE http://192.168.1.100/sdcard/20250127.csv
```

Delete directory:

```bash
curl -i -X DELETE http://192.168.1.100/sdcard/some_directory/
```

Successful operations return `204 No Content`.
