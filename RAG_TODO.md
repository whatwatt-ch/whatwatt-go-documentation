# RAG Optimization TODO - WhatWatt Go Documentation

## Overview

Transform current MkDocs documentation into RAG-optimized format for better LLM consumption and retrieval.

## Current State Analysis

- ✅ Well-structured technical documentation
- ✅ Comprehensive API coverage
- ✅ Real device examples
- ❌ Not optimized for semantic chunking
- ❌ Missing metadata for retrieval
- ❌ No cross-reference semantic links
- ❌ Limited troubleshooting patterns

## Phase 1: Document Structure Enhancement

### 1.1 Add YAML Frontmatter to All Pages

**Goal**: Enable semantic categorization and metadata-driven retrieval

**Template**:

```yaml
---
title: "Descriptive Title"
category: "api-endpoints|data-formats|configuration|troubleshooting|concepts"
tags: ["tag1", "tag2", "tag3"]
api_endpoints: ["/api/path1", "/api/path2"]
protocols: ["REST", "MQTT", "HTTP"]
difficulty: "beginner|intermediate|advanced"
device_compatibility: ["WW_Go_1.2", "all"]
related_concepts: ["concept1", "concept2"]
use_cases: ["monitoring", "configuration", "troubleshooting"]
last_verified: "2025-10-07"
real_device_tested: true|false
---
```

**Files to update**:

- [x] `docs/00-intro/overview.md` ✅
- [x] `docs/00-intro/rest-vs-mqtt.md` ✅
- [x] `docs/10-general/system-info.md` ✅
- [x] `docs/20-rest/streaming.md` ✅
- [x] `docs/20-rest/polling.md` ✅
- [x] `docs/30-mqtt/index.md` ✅
- [x] `docs/30-mqtt/local-reading.md` ✅
- [x] `docs/50-settings/settings.md` ✅
- [x] `docs/50-settings/sdcard/csv-format.md` ✅ (+ Document Context + Key Facts)
- [x] `docs/50-settings/wifi-setup.md` ✅
- [x] `docs/50-settings/meter-comm.md` ✅
- [x] `docs/90-appendix/digest-cheatsheet.md` ✅
- [x] `docs/90-appendix/curl-options.md` ✅

**Phase 1.1 Status**: ✅ **COMPLETED** - All major files now have YAML frontmatter

### 1.2 Add Semantic Context Blocks

**Goal**: Provide immediate context for LLM understanding

**Progress**:

- [x] `docs/50-settings/sdcard/csv-format.md` ✅ (Document Context + Key Facts)
- [x] `docs/20-rest/polling.md` ✅ (Document Context + Key Facts)
- [x] `docs/10-general/system-info.md` ✅ (Document Context + Key Facts)
- [x] `docs/30-mqtt/local-reading.md` ✅ (Document Context + Key Facts)
- [x] `docs/20-rest/streaming.md` ✅ (Document Context + Key Facts)
- [x] `docs/50-settings/settings.md` ✅ (Document Context + Key Facts)
- [x] `docs/50-settings/wifi-setup.md` ✅ (Document Context + Key Facts)
- [x] `docs/50-settings/meter-comm.md` ✅ (Document Context + Key Facts)

**Status**: ✅ **COMPLETED** - All 8 major files enhanced with semantic context

**Template**:

```markdown
## Document Context

- **Purpose**: What this document explains
- **When to use**: Specific scenarios when this info is needed
- **Prerequisites**: What user should know before reading
- **Related to**: Links to related concepts
- **Validates against**: Real device data (if applicable)
```

### 1.3 Create Fact Boxes

**Goal**: Enable quick fact extraction for RAG

**Template**:

```markdown
## Key Facts

- **Endpoint**: `/api/v1/example`
- **Methods**: GET, POST, PUT
- **Authentication**: Required when password set
- **Rate limits**: None
- **Response format**: JSON
- **Typical response time**: <100ms
- **Error codes**: 400, 401, 404, 500
```

## Phase 2: Content Restructuring

### 2.1 Create Semantic Field Mappings

**Goal**: Help LLM understand data relationships

**Example for CSV format**:

```markdown
## Semantic Field Map

### Energy Counters Group
- `EAP_T` (OBIS: 1.8.0) → **semantic_name**: "total_imported_energy" → **meaning**: "Cumulative energy consumed from grid" → **unit**: "kWh" → **type**: "cumulative_counter"
- `EAN_T` (OBIS: 2.8.0) → **semantic_name**: "total_exported_energy" → **meaning**: "Cumulative energy fed back to grid" → **unit**: "kWh" → **type**: "cumulative_counter"

### Power Measurements Group
- `IPAP_T` (OBIS: 1.7.0) → **semantic_name**: "instantaneous_import_power" → **meaning**: "Current power consumption" → **unit**: "kW" → **type**: "instantaneous_value"
```

**Files needing semantic mapping**:

- [x] `docs/50-settings/sdcard/csv-format.md` ✅ (Semantic Field Map added)
- [x] `docs/20-rest/polling.md` ✅ (Semantic Field Map added)
- [x] `docs/20-rest/streaming.md` ✅ (Semantic Field Map added)
- [ ] `docs/10-general/system-info.md`

**Status**: ✅ **MOSTLY COMPLETED** - 3/4 major API files enhanced with semantic mappings

### 2.2 Add Troubleshooting Knowledge Base

**Goal**: Create pattern-based problem resolution

**Files enhanced with troubleshooting**:

- [x] `docs/20-rest/polling.md` ✅ (Common Issues & Solutions added)
- [x] `docs/20-rest/streaming.md` ✅ (Common Issues & Solutions added)
- [x] `docs/50-settings/sdcard/csv-format.md` ✅ (Common Issues & Solutions added)

**Status**: ✅ **COMPLETED** - Major API endpoints have comprehensive troubleshooting guides

**Template**:

```markdown
## Common Issues & Solutions

### Issue: Empty CSV fields
- **Symptoms**: Many columns contain empty values or zeros
- **Root cause**: Meter doesn't provide all OBIS objects
- **Diagnosis**: Check `MSTAT` field - should be "OK"
- **Solution**: Filter empty fields, focus on populated values
- **Code pattern**: `if field_value and field_value != "0":`
- **Related**: Single-phase vs three-phase meter differences

### Issue: Authentication failures
- **Symptoms**: HTTP 401 responses
- **Root cause**: Device has Web UI password set
- **Diagnosis**: Check if `protection: true` in settings
- **Solution**: Use HTTP Digest authentication
- **Code pattern**: `curl --anyauth -u ":PASSWORD"`
- **Related**: [Digest cheatsheet](link)
```

### 2.3 Create Usage Pattern Library

**Goal**: Provide actionable code patterns

**Files enhanced with usage patterns**:

- [x] `docs/20-rest/polling.md` ✅ (Usage Patterns added - real-time monitoring, energy analysis, solar monitoring, phase balancing)
- [x] `docs/20-rest/streaming.md` ✅ (Usage Patterns added - SSE dashboard, data logging, alerting system)

**Status**: ✅ **COMPLETED** - Major API endpoints have practical code examples

**Example patterns implemented**:

- Real-time energy monitoring dashboard
- Energy usage analysis and reporting
- Solar system monitoring and analysis
- Three-phase load balancing analysis
- SSE-based live dashboards
- Real-time data logging to database
- Real-time alerting system with thresholds

**Error handling**: Check for 401 (auth required), 404 (endpoint disabled)

## Phase 3: Cross-Reference Enhancement

### 3.1 Create Concept Relationship Map

**Goal**: Help RAG understand document relationships

**File**: `docs/_data/concept_map.yaml`

```yaml
concepts:
  energy_monitoring:
    related_endpoints: ["/api/v1/report", "/api/v1/live", "/sdcard/"]
    related_docs: ["polling.md", "streaming.md", "csv-format.md"]
    protocols: ["REST", "MQTT"]

  authentication:
    related_endpoints: ["all_api_endpoints"]
    related_docs: ["digest-cheatsheet.md", "rest-conventions.md"]
    required_when: "device.protection == true"

  device_configuration:
    related_endpoints: ["/api/v1/settings", "/api/v1/wifi/sta/settings"]
    related_docs: ["settings.md", "wifi-setup.md"]
    requires_auth: "usually"
```

### 3.2 Add Smart Cross-References

**Goal**: Context-aware linking

**Template**:

```markdown
## Related Information

**If you're trying to**: Get real-time data
**Then see**: [REST Polling](../20-rest/polling.md) or [SSE Streaming](../20-rest/streaming.md)

**If you're trying to**: Download historical data
**Then see**: [SD Card CSV Format](csv-format.md)

**If you get**: HTTP 401 errors
**Then see**: [Digest Authentication](../../90-appendix/digest-cheatsheet.md)

**If device shows**: `MSTAT: "ENCRYPTION KEY"`
**Then see**: [Meter Communication Settings](../meter-comm.md#encryption)
```

## Phase 4: Real Device Validation

### 4.1 Add Device-Tested Badges

**Goal**: Mark content validated against real hardware

**Template**:

```markdown
> **✅ Device Tested**: This documentation was verified against real WhatWatt Go device (192.168.99.114) on 2025-10-07
>
> **Device Info**: Landis+Gyr LGZ1030784855204, MBUS interface, DLMS protocol, Firmware 1.10.0
```

### 4.2 Include Real Response Examples

**Goal**: Provide actual device responses, not synthetic examples

**Update all API docs with**:

- Real HTTP responses from 192.168.99.114
- Actual error conditions
- Real timing measurements
- Actual field values

### 4.3 Create Device Capability Matrix

**Goal**: Help LLM understand device variations

**File**: `docs/_data/device_capabilities.yaml`

```yaml
meter_types:
  landis_gyr_lgz:
    model_pattern: "LGZ*"
    interface: "MBUS"
    protocol: "DLMS"
    populated_fields:
      - "EAP_T"  # Always available
      - "EAN_T"  # Always available
      - "V_L1"   # Single phase only
    empty_fields:
      - "V_L2"   # Not applicable for single-phase
      - "V_L3"   # Not applicable for single-phase
      - "PF"     # Not provided by this model
```

## Phase 5: RAG-Specific Formatting

### 5.1 Create Chunk-Friendly Structure

**Goal**: Ensure each section is self-contained

**Guidelines**:

- Each H2 section should be understandable independently
- Include context/definitions in each major section
- Avoid pronoun references across sections
- Include key facts in each chunk

### 5.2 Add Semantic Markup

**Goal**: Help RAG identify content types

**Template**:

```html
<!-- FACT_BLOCK -->
The WhatWatt Go device uses HTTP Digest authentication when a Web UI password is configured.
<!-- /FACT_BLOCK -->

<!-- CODE_EXAMPLE -->
curl --anyauth -u ":PASSWORD" http://device-ip/api/v1/system
<!-- /CODE_EXAMPLE -->

<!-- TROUBLESHOOTING -->
If you receive HTTP 401: Check if device.protection is true, then use Digest auth
<!-- /TROUBLESHOOTING -->

<!-- REAL_DATA -->
Verified on device 192.168.99.114 on 2025-10-07: response time 45ms, firmware 1.10.0
<!-- /REAL_DATA -->
```

### 5.3 Create Summary Extraction Points

**Goal**: Enable quick LLM summarization

**Template**:

```markdown
## Summary for RAG

**What this document covers**: CSV file format for SD card data logging
**Key endpoints**: `/sdcard/` (list files), `/sdcard/YYYYMMDD.CSV` (download)
**Authentication**: Usually not required for SD card access
**File format**: CSV with OBIS-based column names, UTC timestamps
**Typical use**: Historical data analysis, offline processing
**Alternatives**: REST API `/api/v1/report` for real-time data
**Gotchas**: Many fields empty depending on meter type, time zone is UTC not local
```

## Phase 6: Validation & Testing

### 6.1 RAG Retrieval Testing

- [ ] Test semantic search for common questions
- [ ] Validate cross-reference resolution
- [ ] Check chunk completeness
- [ ] Verify fact extraction accuracy

### 6.2 LLM Response Quality Testing

- [ ] Test Q&A accuracy with modified docs
- [ ] Validate code generation from patterns
- [ ] Check troubleshooting guidance effectiveness
- [ ] Measure response relevance improvement

## Implementation Priority

1. **High Priority (Week 1)**:
   - Add YAML frontmatter to all files
   - Add semantic context blocks
   - Update examples with real device data

2. **Medium Priority (Week 2)**:
   - Create troubleshooting knowledge base
   - Add usage pattern library
   - Implement smart cross-references

3. **Low Priority (Week 3)**:
   - Create device capability matrix
   - Add semantic markup
   - Comprehensive validation testing

## Success Metrics

- **Retrieval accuracy**: RAG finds relevant info for 95% of technical queries
- **Response completeness**: Generated answers include context, examples, and troubleshooting
- **Code quality**: Generated code examples work without modification
- **Cross-reference utility**: Related information suggestions are accurate and helpful

## Tools Needed

- **YAML linter**: Validate frontmatter syntax
- **Link checker**: Ensure cross-references work
- **RAG testing framework**: Validate retrieval quality
- **Device access**: Continue testing against 192.168.99.114

---
**Created**: 2025-10-07
**Last Updated**: 2025-10-07
**Status**: Planning phase
**Estimated effort**: 3 weeks for complete implementation
