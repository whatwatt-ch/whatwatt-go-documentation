---
title: cURL Options Reference - HTTP Client Configuration
category: troubleshooting
tags:
- curl
- http-client
- cli-tools
- debugging
- command-line
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- all_http_endpoints
protocols:
- HTTP
- HTTPS
related_concepts:
- http clients
- command line tools
- api testing
- debugging techniques
use_cases:
- api testing
- command line automation
- debugging requests
- scripting integration
real_device_tested: true
---

# cURL Options

## Document Context

- **Purpose**: Comprehensive cURL command-line tool reference for HTTP API interactions including common options and practical examples
- **When to use**: Testing API endpoints, scripting automation, troubleshooting HTTP requests, learning command-line API interaction
- **Prerequisites**: Command-line familiarity, basic HTTP knowledge, cURL installation, understanding of HTTP methods
- **Related to**: [HTTP basics](http-basics.md), [REST conventions](../50-settings/rest-conventions.md), authentication methods
- **Validates against**: Real whatwatt Go device API endpoints, cross-platform compatibility (Linux/Windows/PowerShell)

## Key Facts

- **Essential options**: -i (headers), -s (silent), -d (data), -X (method) - Core cURL functionality for API testing
- **Data formats**: JSON payloads, form data, request bodies - Support for various content types
- **HTTP methods**: GET, POST, PUT, DELETE - Complete REST API interaction capability
- **Platform support**: Bash and PowerShell examples - Cross-platform command-line usage
- **Practical examples**: whatwatt Go API calls, authentication, streaming - Real-world usage patterns

The `curl` command-line tool is invaluable for interacting with web APIs. It allows for the execution of HTTP requests directly from the terminal, providing a versatile and powerful means of engaging with endpoints. Here are the most commonly used options:

## Essential Options

### `-i` (Include Headers)

This option is used to include the HTTP response headers in the output. When making a request, it's often crucial to see the headers returned by the server, as they contain important information such as status codes and content types.

```bash
curl -i [URL]
```

### `-s` (Silent Mode)

The `-s` option stands for "silent" mode. It suppresses progress meters and error messages, making the output cleaner and more readable, especially useful when processing the response in scripts.

```bash
curl -s [URL]
```

### `-d` (Send Data)

This option is used to send data in a POST request. You'll typically use this option when you need to submit form data or JSON payloads to the server for processing. It's crucial in scenarios where the request body must be included.

```bash
curl -X POST -d '{"key": "value"}' [URL]
```

### `-X` (Specify Method)

The `-X` option allows you to specify the HTTP method to use for the request, such as GET, POST, PUT, DELETE, etc. This is essential for interacting with APIs that require specific methods to perform different actions.

```bash
curl -X PUT -d '{"setting": "new value"}' [URL]
```

## Combining Options

By combining these options, you can craft precise and powerful HTTP requests tailored to your needs. For example, to send a JSON payload with a POST request and include the response headers, you could use:

```bash
curl -i -X POST -d '{"setting": "new value"}' [URL]
```

## Examples with whatwatt Go

Here are some practical examples for interacting with whatwatt Go API:

```bash
# Get device information with headers
curl -i http://192.168.1.100/api/v1/info

# Get meter report silently (for scripts)
curl -s http://192.168.1.100/api/v1/report

# Update WiFi settings
curl -X PUT -d '{"wifi": {"enable": true, "name": "MyNetwork"}}' \
     http://192.168.1.100/api/v1/settings
```

## Windows PowerShell tips

PowerShell interprets quotes differently from bash. Prefer double quotes for the URL and escape inner quotes. You can also use backticks for line continuation.

```powershell
# HTTP auth with password from environment variable
$env:WHATWATT_PASSWORD = "changeme"
curl --anyauth -u ":$env:WHATWATT_PASSWORD" "http://whatwatt-ABCDEF.local/api/v1/system"

# PUT JSON (ensure JSON is a single line or properly escaped)
$body = '{"system": {"host_name": "whatwatt_ABCDEF"}, "services": {"report_interval": 30}}'
curl --anyauth -u ":$env:WHATWATT_PASSWORD" `
     -H "Content-Type: application/json" `
     -X PUT --data "$body" `
     "http://whatwatt-ABCDEF.local/api/v1/settings"

# Streaming SSE (CTRL+C to stop)
curl "http://whatwatt-ABCDEF.local/api/v1/live"
```

Mastering the `curl` command and its options equips you with the ability to seamlessly communicate with web APIs, ensuring efficient and effective interactions with server resources.
