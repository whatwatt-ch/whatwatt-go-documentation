# OpenAPI Documentation Structure

This directory contains the OpenAPI 3.0 specification for the whatwatt Go device REST API.

## Files Overview

| File | Purpose | Status |
|------|---------|--------|
| `api-split.yaml` | **Source file** - modular structure with external references | ✅ Primary |
| `api.yaml` | **Generated file** - bundled from api-split.yaml for documentation | 🔄 Auto-generated |
| `components/` | Schema definitions and reusable components | ✅ Edit these |
| `paths/` | API endpoint definitions grouped by functionality | ✅ Edit these |

## File Structure

```txt
openapi/
├── api-split.yaml        # Main source file (edit this)
├── api.yaml             # Generated bundle (auto-created)
├── components/
│   ├── responses/       # HTTP response definitions
│   └── schemas/         # Data model schemas
└── paths/              # API endpoints grouped by feature
    ├── general.yaml    # System information endpoints
    ├── measurements.yaml # Data reading endpoints
    ├── streaming.yaml  # Real-time data endpoints
    ├── settings.yaml   # Device configuration
    ├── maintenance.yaml # System maintenance
    ├── wi-fi.yaml      # Wi-Fi configuration
    ├── ethernet.yaml   # Ethernet configuration
    ├── actions.yaml    # Device actions
    └── sd-card.yaml    # SD card operations
```

## Workflow

### 1. Editing

**✅ DO edit these files:**

- `api-split.yaml` - Main specification and metadata
- `components/schemas/*.yaml` - Data models
- `components/responses/*.yaml` - Response definitions
- `paths/*.yaml` - API endpoints

**❌ DON'T edit:**

- `api.yaml` - This file is auto-generated

### 2. Building

After editing the modular files, regenerate the bundled version:

```bash
# Regenerate api.yaml from api-split.yaml
npx @redocly/cli bundle openapi/api-split.yaml --output openapi/api.yaml
```

### 3. Validation

The OpenAPI specification is automatically validated as part of the documentation pipeline:

```bash
# Full validation (includes OpenAPI check)
python validate_docs.py

# OpenAPI-only validation
python -c "from prance import ResolvingParser; ResolvingParser('openapi/api.yaml')"
```

## Authentication Documentation

The API specification includes firmware version-specific authentication information:

- **Firmware 1.10.x and later**: HTTP Digest authentication
- **Firmware 1.9.x and earlier**: HTTP Basic authentication
- **Generic curl examples**: Use `--anyauth` for automatic method detection

## Integration

### MkDocs Integration

The OpenAPI specification is integrated into the documentation via the macros plugin:

```yaml
# In mkdocs.yml
plugins:
  - macros
```

The specification is automatically copied to the site during build and referenced in documentation pages.

### Validation Pipeline

OpenAPI validation is integrated into the comprehensive documentation validation pipeline:

- ✅ Syntax validation with Prance
- ✅ Reference resolution checking
- ✅ Schema validation
- ✅ Automated testing as part of CI/CD

## Best Practices

1. **Always edit source files** (`api-split.yaml` and `components/`, `paths/`)
2. **Regenerate bundle** after changes with Redocly CLI
3. **Validate changes** using the validation pipeline
4. **Commit both source and generated files** for consistency
5. **Use semantic commit messages** describing API changes

## Troubleshooting

### Bundle Generation Issues

If bundling fails, check for:

- Invalid YAML syntax in source files
- Broken `$ref` references
- Missing referenced files

### Validation Errors

Common issues and solutions:

- **Missing schemas**: Add missing schema definitions to `components/schemas/`
- **Invalid references**: Check file paths in `$ref` statements
- **Authentication inconsistencies**: Update both specification and documentation

## Tools Required

- **Node.js** and **npm** (for Redocly CLI)
- **Python 3.11+** with **Prance** (for validation)
- **Redocly CLI**: `npm install -g @redocly/cli`

This structure ensures maintainable, validated, and automatically synchronized OpenAPI documentation.
