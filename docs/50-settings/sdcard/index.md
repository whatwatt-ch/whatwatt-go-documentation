---
title: SD card — overview
category: concepts
tags:
- sdcard
- index
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# SD card — overview

## Document Context

- **Purpose**: SD card HTTP interface overview for file management operations including listing, downloading, and deleting files
- **When to use**: Managing local data storage, accessing CSV reports, cleaning up files, setting up data archival workflows
- **Prerequisites**: SD card inserted and mounted, understanding of HTTP file operations, basic file system concepts
- **Related to**: SD card configuration (configuration.md), CSV format specification, data logging services
- **Validates against**: SD card mount status (503 if unmounted), file system operations, HTTP MIME type handling

## Key Facts

- **Base path**: `/sdcard/` - Root endpoint for all SD card file operations
- **Methods**: GET (list/download), DELETE (remove) - Standard HTTP file management
- **Mount dependency**: Returns 503 Service Unavailable if SD card not mounted
- **Content types**: JSON for directory listings, appropriate MIME types for file downloads
- **Operations**: Browse directories, download CSV reports, delete files/folders, configure logging service

--8<-- "../../_partials/auth-note.md"

## Endpoint summary

The SD card HTTP interface lets you list directories, download files (CSV or others), and delete files or folders. If the card isn’t mounted, the device returns HTTP 503.

| Parameter | Value |
|-----------|-------|
| Base path | `/sdcard/` |
| Methods   | `GET`, `DELETE` |
| Content   | JSON for listings, file MIME type for downloads |

## What’s on this page

- Browse and list files: see how to request directory listings and parse responses
- Download files: retrieve CSV reports or any file
- Delete files and folders: endpoints and caveats
- CSV format: naming and column notes
- Configuration: enabling SD writes and frequency
- Troubleshooting: common errors and fixes
- Usage examples: ready-to-run scripts

Use the sidebar to jump to a topic or start here:

- Browse & list → [Listing](listing.md)
- Download files → [Download](download.md)
- Delete files/dirs → [Delete](delete.md)
- CSV format → [CSV format](csv-format.md)
- Configure SD service → [Configuration](configuration.md)
- Errors and fixes → [Troubleshooting](troubleshooting.md)
- Scripts → [Usage examples](usage-examples.md)
