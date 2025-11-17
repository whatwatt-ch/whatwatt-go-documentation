---
title: REST API Conventions
category: concepts
tags:
- rest_conventions
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# REST API Conventions

## Document Context

- **Purpose**: REST API conventions and best practices for whatwatt Go device configuration including HTTP methods, status codes, and security
- **When to use**: Before implementing REST API integrations, troubleshooting API calls, understanding authentication requirements
- **Prerequisites**: HTTP/REST API knowledge, JSON format understanding, basic web development concepts
- **Related to**: [Authentication](../90-appendix/digest-cheatsheet.md), [HTTP basics](../90-appendix/http-basics.md), device settings endpoints
- **Validates against**: HTTP standards, JSON specifications, Digest authentication RFC, CORS policy implementation

## Key Facts

- **HTTP methods**: GET (read), POST (overwrite), PUT (update), DELETE (remove configuration)
- **Authentication**: HTTP Authentication required when WebUI password set
- **Response format**: JSON with UTF-8 encoding, security headers included
- **Status codes**: 200/204 success, 400 bad request, 401 unauthorized, 404 not found
- **Limits**: 8kB typical request size, CORS origin validation required for browser requests

--8<-- "../../_partials/auth-note.md"

General conventions for using the local REST API to configure whatwatt Go device settings.

## HTTP Methods

The local REST API allows you to read, overwrite, update, or delete values. The body is typically returned and processed in JSON format.

| Method   | Purpose                                                    | Usage                                    |
|----------|------------------------------------------------------------|-----------------------------------------|
| **GET**  | Read current values                                        | Retrieve configuration                  |
| **POST** | Overwrite all values                                       | Replace entire configuration (full object expected) |
| **PUT**  | Update selected fields                                     | Modify specific settings                |
| **DELETE** | Delete configuration (selected endpoints only)           | Remove configuration entirely           |

### Method Details

#### GET Method

- Returns current configuration values
- No request body required
- Response in JSON format

#### POST Method

- Overwrites the configuration
- Expects a complete JSON object following the endpoint schema
- Missing required fields or invalid values result in HTTP 400
- Use when replacing the entire configuration

#### PUT Method

- Updates only the fields specified in the JSON body
- Existing fields not mentioned remain unchanged
- Preferred for modifying specific settings

#### DELETE Method

- Removes all configuration for the endpoint
- Only available for selected endpoints
- Use with caution as this cannot be undone

## HTTP Status Codes

Each API method returns an HTTP status code indicating the result:

| Code | Status                | Description                                          |
|------|-----------------------|----------------------------------------------------|
| 200  | Success               | Request successful with response (usually JSON)    |
| 204  | No Content            | Request successful without response body           |
| 202  | Accepted              | Request accepted for asynchronous processing (e.g., actions) |
| 400  | Bad Request           | Invalid parameters or ranges in JSON object       |
| 401  | Unauthorized          | Authentication required        |
| 404  | Not Found             | Endpoint not found or blocked by CORS policy      |
| 500  | Internal Server Error | Internal device problem                            |
| 503  | Service Unavailable   | Service temporarily unavailable                    |

## General Guidelines

### JSON Format

- All request and response bodies use JSON format
- Ensure proper JSON syntax and encoding
- Maximum request size varies by endpoint (typically 8 kB)

### Authentication

- When a Web UI password is set, endpoints require HTTP authentication
- **Firmware 1.10.X and later**: Uses HTTP Digest authentication (more secure)
- **Firmware before 1.10.X**: Uses HTTP Basic authentication
- **Recommendation**: Use `curl --anyauth` to automatically detect the appropriate method
- Include credentials in all requests when authentication is enabled

See the authentication note above for detailed technical specifications and curl examples.

!!! tip "Digest quick reference"
    For field meanings (cnonce, nc, realm), stale=true handling, and PowerShell-friendly examples, see the [Digest cheatsheet](../90-appendix/digest-cheatsheet.md).

### CORS and Security Headers

- Requests from browsers must include an Origin matching the device’s allowed list (device hostname and its .local). Disallowed origins receive HTTP 404 without CORS headers.
- Responses include security headers such as `X-Content-Type-Options: nosniff` and `Cache-Control: no-store`.
- JSON responses use `Content-Type: application/json; charset=utf-8`.

### Error Handling

- Always check HTTP status codes
- Parse error responses for details when available
- Implement retry logic/backoff for transient errors (e.g., 503)

### Best Practices

- Use PUT for partial updates rather than POST when possible
- Validate configuration locally before sending to device
- Keep backups of working configurations
- Test changes in development environment first

!!! tip "POST vs PUT"
    Use PUT for partial updates. Use POST only when replacing the entire object with a full, valid configuration.
