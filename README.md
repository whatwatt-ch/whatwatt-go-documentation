# whatwatt Go Documentation

Modern, comprehensive documentation for whatwatt Go devices built with **MkDocs Material**.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (for markdownlint and broken-link-checker)
- Git

### Installation

```bash
# Clone and setup
git clone <repository-url>
cd whatwatt_doc

# Python environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
npm install
```

`requirements.txt` installs the Python-side validation dependencies,
including `Prance` and the OpenAPI validation backend used by the validation
script.
Install `Vale` separately as a system CLI tool.

### Development

```bash
# Start local development server
mkdocs serve -a 127.0.0.1:8000
# Or using npm
npm run serve

# Open http://127.0.0.1:8000 in your browser
```

## 🔧 Building & Deployment

### Local Build

```bash
# Development build
mkdocs build --clean
# Or using npm
npm run build

# Production build (with validation)
npm run build:prod
```

### Deployment

```bash
# Build for production deployment
npm run build:prod

# Deploy directory: ./dist/
# Copy ./dist/ contents to your web server
```

Recommended direct invocation from the project virtual environment:

```bash
cd /home/sj/esp32-workspace/whatwatt/whatwatt-go-documentation
source .venv/bin/activate
python build_production.py
```

The production build includes:

- Strict validation
- Optimized assets
- Ready-to-deploy static files in `./dist/`

## ✅ Validation & Quality

### Quick Validation

```bash
# Fast validation (recommended for development)
python validate_docs.py --fast

# Full validation (all checks)
python validate_docs.py
```

### Available Commands

```bash
# Individual validators
npm run validate:markdown    # Markdown syntax
npm run validate:mkdocs      # MkDocs build
npm run validate:links       # Link checking
npm run validate:openapi     # OpenAPI specs

# Fixes
npm run lint:fix            # Auto-fix markdown issues
```

### Validation Pipeline

Our documentation maintains **100% validation success** with:

- ✅ **Markdown syntax** (markdownlint-cli2)
- ✅ **MkDocs strict build** (catches broken references)
- ✅ **OpenAPI validation** (Prance)
- ✅ **Link checking** (7900+ links tested)
- ✅ **Style validation** (Vale with technical vocabulary)

## 📁 Project Structure

```text
docs/                   # Documentation content
├── index.md           # Homepage
├── 00-intro/          # Getting started
├── 10-general/        # General information
├── 20-rest/           # REST API docs
├── 30-mqtt/           # MQTT docs
├── 40-secure-mqtt/    # Secure MQTT setup
├── 50-settings/       # Device settings
└── 90-appendix/       # Additional resources

openapi/               # OpenAPI specifications
├── api.yaml          # Main API spec
└── components/       # Reusable components

dist/                  # Production build output (git-ignored)
site/                  # Development build output (git-ignored)
```

## 🛠️ Development Tools

### Optional: Advanced Validation

For full validation pipeline, install additional tools:

```bash
# Vale (style guide)
# Windows (Chocolatey)
choco install vale

# macOS (Homebrew)
brew install vale

# Then sync styles
npm run vale:sync
```

### Pre-commit Hooks

The project uses pre-commit hooks for code quality:

```bash
# Install pre-commit (optional)
pip install pre-commit
pre-commit install

# Manual run
pre-commit run --all-files
```

## 📊 Performance

- **Build time**: ~20s (production)
- **Validation**: ~10s (fast mode)
- **Link checking**: ~30s (7900+ links)
- **Site size**: ~2MB (optimized)

---

**Built with**: MkDocs Material • OpenAPI • Vale • Modern validation pipeline
