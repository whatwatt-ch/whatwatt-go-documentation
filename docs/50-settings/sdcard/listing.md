---
title: Listing — browse SD card
category: concepts
tags:
- sdcard
- listing
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# Listing — browse SD card

List directories to discover files available on the SD card.

## Document Context

- **Purpose**: SD card directory listing API for discovering files and folders available on mounted storage
- **When to use**: Browsing SD card contents, finding CSV reports, checking file availability before download operations
- **Prerequisites**: SD card mounted and accessible, understanding of directory path structures, JSON response parsing
- **Related to**: [File download](download.md), [File deletion](delete.md), [SD card configuration](configuration.md)
- **Validates against**: SD card filesystem structure, directory traversal patterns, file type identification

## Key Facts

- **Endpoint**: GET `/sdcard/[directory/]` - List contents of specified directory path
- **Path format**: Must end with `/` for directory listing, JSON response with file metadata
- **Response structure**: Path confirmation, files array with name/size/type information
- **File types**: Distinguishes between files and directories, size in bytes (0 for dirs)
- **Navigation**: Supports subdirectory browsing with proper path construction

## Requests

```http
GET /sdcard/
GET /sdcard/<directory_name>/
```

!!! warning "Path format"
    To list a directory, the path must end with `/`. Without a file extension, the server returns a JSON listing for that directory.

### Example

```bash
curl -s http://192.168.1.100/sdcard/
```

### Response

```json
{
  "path": "/sdcard/",
  "files": [
    {"name": "20240929.CSV", "size": 1161385, "type": "file"},
    {"name": "SYSTEM~1",    "size": 0,       "type": "dir"},
    {"name": "NIHAO.TXT",   "size": 13,      "type": "file"}
  ]
}
```

### Response fields

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Path for which contents are listed |
| `files[].name` | string | File or directory name |
| `files[].size` | uint | Size in bytes (0 for directories) |
| `files[].type` | string | `file` or `dir` |
