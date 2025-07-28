# Configuration Guide

## Standardized Report Configuration

This guide explains the standardized configuration system implemented across all BCSB reports.

## 🎯 Configuration Philosophy

The standardized configuration system follows these principles:

1. **Simplicity**: Keep configuration files simple and readable
2. **Consistency**: Use the same patterns across all reports
3. **Environment Safety**: Prevent production issues during development
4. **AI-Ready**: Include business logic documentation for AI systems
5. **Maintainability**: Make it easy to update and modify reports

## 📁 File Structure

Each report follows this structure:
```
Reports/[Business_Line]/[Report_Name]/
├── src/
│   ├── config.py          # ← STANDARDIZED CONFIGURATION
│   ├── main.py            # ← Business logic with documentation
│   └── [other modules]
├── input/                 # Development input files
├── output/                # Development output files
├── assets/                # Templates and static files
└── test/
    └── test_config.json   # Testing configuration
```

## 📋 Standard config.py Template

### Complete Template
```python
"""
[Report Name] - [Brief description of business purpose and functionality]

Input Files: [List required input files, or "None" if no files needed]
Output Files: [Describe generated files with naming patterns]
Tables: [List database tables accessed, or "None" if no database access]
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "[Human-readable report name]"
BUSINESS_LINE = "[Commercial Lending/Operations/Retail/Government Banking/etc]"
SCHEDULE = "[Daily/Weekly/Monthly/Manual/As Needed]"
OWNER = "[Team or Person Responsible]"

# Status
PROD_READY = True  # Set to False if report is under development

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\[PRODUCTION_NETWORK_PATH]") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = ["primary@bcsbmail.com", "secondary@bcsbmail.com"] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories
OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
```

## 🔧 Configuration Sections Explained

### 1. Documentation Header
```python
"""
Rate Scraping Report - Automated daily collection of interest rates from multiple external 
sources (FRED, CME, FHLB) for treasury management and loan pricing decisions.

Input Files: None (external API/web scraping)
Output Files: Rate_Report_MMM_DD_YY_HHMM.xlsx and .pdf
Tables: None
"""
```

**Purpose**: AI-ready documentation that explains:
- What the report does
- What files it needs (input)
- What files it creates (output)  
- What database tables it uses

**Best Practices**:
- Keep description concise but complete
- Be specific about file patterns
- List all database dependencies

### 2. Report Metadata
```python
# Report Info
REPORT_NAME = "Rate Scraping Report"
BUSINESS_LINE = "Operations"
SCHEDULE = "Daily"
OWNER = "Operations Team"
```

**Purpose**: Standardized metadata for:
- Report catalogs and inventories
- Scheduling systems
- Ownership tracking
- Business line organization

**Valid Values**:
- `BUSINESS_LINE`: Commercial Lending, Operations, Retail, Government Banking, Indirect Lending, Resolution Committee
- `SCHEDULE`: Daily, Weekly, Monthly, Manual, As Needed
- `OWNER`: Specific team or person name

### 3. Development Status
```python
# Status
PROD_READY = True  # False if report is under development
```

**Purpose**: Indicates if report is ready for production use
- `True`: Report is stable and can be scheduled
- `False`: Report is under development, should not be automated

### 4. Environment Management
```python
# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\network\path") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"
```

**How It Works**:
- **Development** (`REPORT_ENV=dev` or unset): Uses local directories
- **Production** (`REPORT_ENV=prod`): Uses network paths

**Path Examples**:
```python
# Commercial Lending
BASE_PATH = Path(r"\\00-DA1\Home\Share\Line of Business_Shared Services\Commercial Lending\Production")

# Operations  
BASE_PATH = Path(r"\\00-berlin\Operations\Reports\Production")

# Development (all reports)
BASE_PATH = Path(__file__).parent.parent  # Points to report root directory
```

### 5. Email Configuration
```python
# Email Recipients
EMAIL_TO = ["user1@bcsbmail.com", "user2@bcsbmail.com"] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []
```

**Safety Features**:
- Empty lists in development prevent accidental emails
- Business Intelligence team automatically CC'd in production
- Supports both TO and CC recipients

**Usage in main.py**:
```python
if EMAIL_TO:  # Only send if recipients configured
    cdutils.distribution.email_out(
        recipients=EMAIL_TO,
        cc_recipients=EMAIL_CC,
        subject="Report Subject",
        body="Report message",
        attachment_paths=[output_file]
    )
else:
    print("Development mode - email not sent")
```

### 6. Directory Creation
```python
# Creates directories
OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
```

**Purpose**: Ensures required directories exist when config is imported
- Safe to run multiple times (`exist_ok=True`)
- Works in both development and production environments

## 🚫 What NOT to Include in Config

### Deprecated Patterns (Removed)
```python
# ❌ DON'T USE THESE ANYMORE
production_flag = True              # Use ENV instead
__version__ = "1.0.0"              # Not needed
EMAIL_BCC = [...]                  # Use EMAIL_CC instead
BASE_DIR = Path("hardcoded/path")  # Use environment-aware paths
```

### Complex Logic (Move to main.py)
```python
# ❌ DON'T PUT COMPLEX LOGIC IN CONFIG
def calculate_dates():             # Move to main.py
    ...

COMPLEX_QUERY = """                # Move to main.py
    SELECT complex query...
"""

LARGE_DATA_STRUCTURES = [...]      # Move to main.py
```

**Rule**: Config should only contain simple configuration values

## 🔄 Migration from Legacy Configs

### Step-by-Step Migration

1. **Backup Original**: Save copy of existing config.py
2. **Apply Template**: Replace with standardized template
3. **Migrate Values**: Copy relevant configuration values
4. **Move Complex Items**: Move functions/queries to main.py
5. **Update Imports**: Ensure main.py imports from config correctly
6. **Test**: Verify report works in development mode

### Common Migration Issues

#### Hard-coded Paths
```python
# Before (❌)
OUTPUT_PATH = Path("C:\\Reports\\Output")

# After (✅)
OUTPUT_DIR = BASE_PATH / "output"
```

#### Mixed Email Patterns
```python
# Before (❌)
EMAIL_BCC = ["user@bcsbmail.com"]
EMAIL_RECIPIENTS = ["other@bcsbmail.com"]

# After (✅)
EMAIL_TO = ["user@bcsbmail.com", "other@bcsbmail.com"] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []
```

#### Production Flags
```python
# Before (❌)
def main(production_flag=False):
    if production_flag:
        # production logic

# After (✅)
# In main.py, use src.config.ENV
if src.config.ENV == 'prod':
    # production logic
```

## 🧪 Testing Configuration

### Basic Validation
```python
# Test in Python console
import sys
sys.path.append('Reports/Business_Line/Report_Name/src')
import config

print(f"Environment: {config.ENV}")
print(f"Output dir: {config.OUTPUT_DIR}")
print(f"Email recipients: {len(config.EMAIL_TO)}")
```

### Environment Testing
```bash
# Test development mode (default)
python -c "import src.config; print(src.config.ENV, src.config.OUTPUT_DIR)"

# Test production mode  
REPORT_ENV=prod python -c "import src.config; print(src.config.ENV, src.config.OUTPUT_DIR)"
```

## 📝 Configuration Checklist

When creating or updating a config.py:

- [ ] Documentation header with business purpose
- [ ] All required metadata fields filled
- [ ] PROD_READY status set appropriately  
- [ ] Environment-aware path configuration
- [ ] Production network path is correct
- [ ] Email recipients configured for production
- [ ] Business Intelligence CC included
- [ ] Directory creation included
- [ ] No deprecated patterns used
- [ ] No complex logic in config
- [ ] Tested in both dev and prod modes

## 🔗 Related Documentation

- [REPORTS_SYSTEM_DOCUMENTATION.md](REPORTS_SYSTEM_DOCUMENTATION.md) - Full system overview
- [test_framework/README.md](test_framework/README.md) - Testing system
- [cdutils/cdutils/README_distribution.md](cdutils/cdutils/README_distribution.md) - Email system

---

**Maintained By**: BCSB Business Intelligence Team