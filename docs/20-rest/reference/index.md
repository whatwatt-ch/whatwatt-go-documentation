---
title: REST Reference (OpenAPI)
category: concepts
tags:
- index
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
---

# REST Reference (OpenAPI)

## Document Context

- **Purpose**: Provides comprehensive OpenAPI/Swagger specification for all WhatWatt Go REST API endpoints with interactive documentation
- **When to use**: API development, integration planning, endpoint discovery, parameter validation, response schema reference
- **Prerequisites**: Understanding of REST APIs, HTTP methods, JSON schema, OpenAPI/Swagger specification format
- **Related to**: All REST endpoints, HTTP authentication, API polling, streaming, device configuration
- **Validates against**: Complete API specification generated from actual device firmware endpoints

## Key Facts

- **Documentation format**: OpenAPI 3.0 specification with ReDoc renderer
- **Coverage**: All available REST API endpoints and methods
- **Interactive features**: Request/response examples, parameter details, schema validation
- **Authentication**: HTTP authentication requirements documented
- **Response schemas**: Complete JSON response structures and data types
- **Error codes**: HTTP status codes and error response formats
- **Fallback access**: Raw YAML specification available for download
- **Live testing**: Interactive API explorer with device endpoint testing

Below is the full OpenAPI reference for the device REST API. It is rendered with ReDoc from the OpenAPI source.

<div class="redoc-container">
  <redoc spec-url="openapi.yaml"></redoc>
</div>

<script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>

If the viewer doesn’t load, you can download the raw spec:

- [openapi.yaml](openapi.yaml)
