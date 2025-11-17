---
title: REST vs MQTT
category: concepts
tags:
- rest-api
- mqtt
- integration-methods
- comparison
- architecture-decision
difficulty: beginner
device_compatibility:
- WW_Go_1.2
- all
last_verified: '2025-10-07'
api_endpoints: []
protocols:
- HTTP
- REST
- MQTT
related_concepts:
- api design
- messaging patterns
- integration architecture
- protocol selection
use_cases:
- architecture planning
- integration design
- protocol selection
- technical decision making
real_device_tested: false
---

# REST vs MQTT

## Document Context

- **Purpose**: Comparison guide for choosing between REST API and MQTT integration methods based on use case requirements and architectural needs
- **When to use**: Architecture planning phase, integration design decisions, protocol selection for smart meter projects, technical evaluation
- **Prerequisites**: Basic understanding of HTTP/REST concepts, MQTT publish-subscribe messaging, integration patterns, network protocols
- **Related to**: [First request](first-request.md), [MQTT overview](../30-mqtt/index.md), [REST polling](../20-rest/polling.md), [Streaming](../20-rest/streaming.md)
- **Validates against**: whatwatt Go dual-protocol support, real-world integration patterns, performance characteristics

## Key Facts

- **REST API**: HTTP-based request-response for on-demand reads, configuration, CRUD operations
- **MQTT**: Lightweight publish-subscribe for streaming telemetry, real-time monitoring, event-driven automation
- **Use cases**: REST for polling/configuration, MQTT for continuous data streams and low-latency applications
- **Network efficiency**: MQTT optimized for bandwidth and reliability, REST better for simple integrations
- **Integration complexity**: REST simpler to implement, MQTT requires broker infrastructure

## Local REST API over HTTP

The REST API provides a straightforward method for integrating the whatwatt Go device through standard web protocols. Key advantages include:

- Ease of integration with various systems due to its simplicity and compatibility with many development environments
- Allows for direct implementation of CRUD operations (Create, Read, Update, Delete) on the data provided by the device

## MQTT Client Connection

MQTT (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe messaging protocol. It is particularly beneficial for scenarios where bandwidth usage and network reliability are significant concerns. By connecting as an MQTT client, the whatwatt Go device can:

- Efficiently handle high volumes of data transmission with minimal overhead
- Ensure low latency, making it ideal for real-time monitoring and control applications
- Optimize the use of network resources, providing a reliable method for data communication

## When to Use Which

- Use **REST** for on-demand reads and configuration
- Use **MQTT** for streaming telemetry and event-driven automation
