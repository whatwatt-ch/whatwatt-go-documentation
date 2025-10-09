---
title: HTTP Digest Authentication Cheatsheet
category: troubleshooting
tags:
- authentication
- http-digest
- security
- troubleshooting
- curl
difficulty: intermediate
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints:
- all_authenticated_endpoints
protocols:
- HTTP
- Digest
related_concepts:
- web ui password
- device protection
- curl authentication
- http security
use_cases:
- authentication setup
- curl command construction
- troubleshooting 401 errors
- secure api access
real_device_tested: true
---

# HTTP Digest cheatsheet

## Document Context

- **Purpose**: HTTP Digest authentication reference for whatwatt Go device API access including field definitions and practical examples
- **When to use**: Implementing device authentication, troubleshooting auth issues, understanding Digest auth mechanics, scripting API calls
- **Prerequisites**: HTTP authentication knowledge, command-line tools, understanding of nonce-based security, password-protected devices
- **Related to**: REST conventions (rest-conventions.md), cURL usage (curl-options.md), HTTP basics (http-basics.md)
- **Validates against**: RFC 2617 Digest authentication, MD5-sess algorithm, whatwatt Go device auth implementation

## Key Facts

- **Authentication method evolution**:
  - **Firmware 1.10.X and later**: HTTP Digest authentication (this guide)
  - **Firmware before 1.10.X**: HTTP Basic authentication
  - **Recommendation**: Use `curl --anyauth` for automatic method detection
- **Algorithm**: MD5-sess with auth/auth-int quality of protection (qop)
- **Credentials**: Empty username, WebUI password, device hostname as realm
- **Nonce handling**: Server-issued tokens with stale=true refresh mechanism
- **Client requirements**: cnonce generation, nc counter (starts 00000001), automatic retries
- **Implementation**: Built-in support in cURL, Python requests, most HTTP libraries

Short reference for device Digest auth (MD5-sess).

## Core fields

- realm: device hostname (e.g., `whatwatt-ABCDEF.local`)
- algorithm: `MD5-sess`
- qop: `auth` (optionally `auth-int` to include body integrity)
- nonce: server-issued token (changes periodically)
- opaque: server-issued token (echo back if provided)
- username: empty string for device API (user is not used), password is the Web UI password
- cnonce: client random nonce (hex/ASCII)
- nc: request counter per (nonce, cnonce) in 8-hex, starts at `00000001`, increments per request

## Stale nonce handling

When the server returns `401` with `WWW-Authenticate: ... stale=true`, the previous nonce expired.

- Re-run the same request using the new challenge values
- Generate a new `cnonce`, reset `nc` to `00000001`
- Keep the same method, URI, and body

## auth-int vs auth

- qop=auth: integrity covers method/URI
- qop=auth-int: also covers entity body hash ("entity-body" MD5). Use when sending JSON bodies you want integrity-checked.

Most clients (curl, requests, Postman) compute these automatically.

## Quick examples

### curl (Linux/macOS)

```bash
curl --digest -u ":<password>" http://whatwatt-ABCDEF.local/api/v1/system
```

### curl (PowerShell on Windows)

> PowerShell parses quotes differently. Prefer double quotes outside and escape inner quotes, or use backticks.

```powershell
# Basic GET
curl --digest -u ":$env:WHATWATT_PASSWORD" "http://whatwatt-ABCDEF.local/api/v1/system"

# PUT JSON with auth-int (curl auto-negotiates if offered)
$body = '{"system": {"host_name": "whatwatt_ABCDEF"}}'
curl --digest -u ":$env:WHATWATT_PASSWORD" `
  -H "Content-Type: application/json" `
  -X PUT --data "$body" `
  "http://whatwatt-ABCDEF.local/api/v1/settings"
```

### Python requests

```python
import requests
from requests.auth import HTTPDigestAuth

url = "http://whatwatt-ABCDEF.local/api/v1/system"
resp = requests.get(url, auth=HTTPDigestAuth("", "<password>"))
resp.raise_for_status()
print(resp.json())
```
