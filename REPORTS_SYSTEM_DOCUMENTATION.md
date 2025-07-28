# BCSB Reports System

> **Enterprise Business Intelligence & Analytics Platform**  
> Bristol County Savings Bank  
> Version: 2.0 (Standardized Architecture)

## Overview

The BCSB Reports System is a comprehensive business intelligence platform that automates critical banking operations reports across multiple business lines. The system processes data from core banking systems, generates formatted Excel reports, and distributes them to stakeholders via automated email delivery.

## 🏗️ System Architecture

### Repository Structure
```
Reports/
├── [Business_Line]/
│   └── [Report_Name]/
│       ├── src/                    # Source code
│       │   ├── config.py          # Standardized configuration
│       │   ├── main.py            # Report logic & business rules
│       │   └── [modules...]       # Supporting modules
│       ├── input/                 # Input files (dev environment)
│       ├── output/                # Generated reports (dev environment)
│       ├── assets/                # Template files & static resources
│       ├── test/                  # Test configuration
│       │   └── test_config.json   # Testing parameters
│       └── Documentation/         # Technical & business documentation
├── cdutils/                       # Shared utilities library
│   ├── cdutils/
│   │   ├── distribution.py        # Email distribution system
│   │   └── database/              # Database connection utilities
│   └── tests/                     # Utility tests
├── test_framework/                # Testing infrastructure
│   ├── simple_tester.py          # Main test runner
│   ├── sync_prod_files.py        # Production file sync utility
│   └── README.md                 # Testing documentation
└── run_tests.py                  # Master test execution script
```

### Business Lines Coverage
- **Commercial Lending**: Portfolio analysis, deposit tracking, concentration reports
- **Operations**: Rate scraping, trial balance, regulatory compliance
- **Retail Banking**: Consumer products, business checking, loan reporting
- **Government Banking**: Municipal services, payroll & vendor processing
- **Indirect Lending**: Dealer networks, contract processing, reserve management
- **Resolution Committee**: Risk management, delinquency tracking, regulatory oversight

## 📋 Standardized Configuration System

### Configuration Template
Every report follows a standardized `config.py` structure:

```python
"""
[Report Name] - [Brief description of business purpose]

Input Files: [List of required input files or "None"]
Output Files: [Description of generated files]
Tables: [Database tables accessed or "None"]
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "[Display Name]"
BUSINESS_LINE = "[Department/Division]"
SCHEDULE = "[Daily/Weekly/Monthly/Manual/As Needed]"
OWNER = "[Responsible Team]"

# Status
PROD_READY = True  # False if report is under development

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\NETWORK\PATH") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients
EMAIL_TO = ["recipient@bcsbmail.com"] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories
OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
```

### Key Configuration Features

#### Environment Management
- **Development Mode**: `REPORT_ENV=dev` (default)
  - Uses local directories relative to report folder
  - No emails sent (empty recipient lists)
  - Safe for testing and development

- **Production Mode**: `REPORT_ENV=prod`
  - Uses network paths for file operations
  - Full email distribution to business users
  - Automated scheduling compatibility

#### Path Management
- **Automatic Directory Creation**: Ensures `input/` and `output/` directories exist
- **Environment-Aware Paths**: Switches between local and network paths based on environment
- **Standardized Structure**: Consistent file organization across all reports

#### Email Configuration
- **Recipient Management**: Separate TO and CC lists with environment-based control
- **Business Intelligence CC**: Automatic CC to BI team in production
- **Development Safety**: Empty recipient lists prevent accidental emails during testing

## 🔧 Development Standards

### Business Logic Documentation
Each `main.py` includes comprehensive business logic extraction:

```python
"""
[Report Name] - Main Entry Point

BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- [Description of data sources, APIs, databases]
- [Relationships between data entities]

Business Rules:
- [Key business rules and calculations]
- [Filtering criteria and business logic]
- [Regulatory or compliance requirements]

Data Processing Flow:
1. [Step-by-step process description]
2. [Data transformations and calculations]
3. [Output generation and formatting]

Key Calculations:
- [Important formulas and business calculations]
- [Data aggregations and summaries]

Business Intelligence Value:
- [How this report supports business decisions]
- [Key insights and metrics provided]
"""
```

### Deprecated Pattern Removal
The standardization process eliminated legacy patterns:
- ❌ `production_flag` parameters (replaced with environment variables)
- ❌ `__version__` imports (replaced with environment-based logic)
- ❌ Hardcoded paths (replaced with environment-aware path management)
- ❌ Mixed email patterns (standardized on EMAIL_TO/EMAIL_CC)

## 📧 Email Distribution System

### Modern Outlook Integration
The `cdutils.distribution` module provides cross-platform email functionality:

```python
import cdutils.distribution

cdutils.distribution.email_out(
    recipients=["primary@bcsbmail.com"],
    cc_recipients=["manager@bcsbmail.com"],
    subject="Daily Report",
    body="Report attached for review.",
    attachment_paths=[Path("output/report.xlsx")]
)
```

### Key Features
- **Cross-Platform**: Works on Windows (PowerShell) and macOS (AppleScript)
- **No Dependencies**: Uses native system tools, no win32com required
- **Outlook Integration**: Creates emails in Outlook for review before sending
- **Attachment Support**: Handles multiple file attachments with path validation
- **Error Handling**: Comprehensive error reporting and fallback mechanisms

### Standard Distribution Pattern
```python
if EMAIL_TO:  # Only send if recipients configured
    cdutils.distribution.email_out(
        recipients=EMAIL_TO,
        cc_recipients=EMAIL_CC,
        subject=f"Report Name - {datetime.now().strftime('%Y-%m-%d')}",
        body="Standard business message...",
        attachment_paths=[output_file]
    )
    print(f"Email sent to {len(EMAIL_TO)} recipients")
else:
    print("Development mode - email not sent")
```

## 🧪 Testing Framework

### Lightweight Testing Approach
The testing system focuses on practical validation:
- **Execution Testing**: Verifies reports run without errors
- **Output Validation**: Confirms expected files are generated
- **Environment Safety**: Tests run in development mode only

### Test Configuration
Each report can include `test/test_config.json`:

```json
{
  "description": "Human-readable test description",
  "skip": false,
  "expected_outputs": [
    "exact_filename.xlsx",
    "pattern_*.csv"
  ],
  "notes": "Additional context about test requirements"
}
```

### Running Tests

#### Test All Reports
```bash
python run_tests.py
```

#### Test Specific Report
```bash
python run_tests.py "Report Name"
```

#### Sync Production Files and Test
```bash
python run_tests.py --sync
```

### Test Results
```
🏃 Testing Rate Scraping...
✅ Rate Scraping: All outputs generated

🏃 Testing Business_Concentration_of_Deposits...
✅ Business_Concentration_of_Deposits: All outputs generated

==================================================
Total: 22 | ✅ Passed: 18 | ❌ Failed: 2 | ⏭️ Skipped: 2
```

## 🚀 Usage Guidelines

### For Report Developers

#### Creating a New Report
1. **Create Directory Structure**:
   ```bash
   mkdir -p "Reports/Business_Line/Report_Name/{src,input,output,assets,test}"
   ```

2. **Implement Configuration**:
   - Copy standard `config.py` template
   - Customize for your report's needs
   - Set appropriate email recipients

3. **Develop Business Logic**:
   - Implement `main.py` with business logic documentation
   - Use `src.config` for all configuration values
   - Follow environment-aware development practices

4. **Add Testing**:
   - Create `test/test_config.json`
   - Specify expected output files
   - Test in development environment

#### Modifying Existing Reports
1. **Review Current Configuration**: Understand existing patterns
2. **Apply Standards Gradually**: Migrate to standardized config
3. **Preserve Business Logic**: Maintain existing functionality
4. **Test Thoroughly**: Validate changes don't break production

### For Business Users

#### Report Scheduling
- Reports check `REPORT_ENV` environment variable
- Production scheduling systems should set `REPORT_ENV=prod`
- Development and testing should use default (dev) environment

#### File Locations
- **Production**: Reports use configured network paths
- **Development**: Reports use local project directories
- **Input Files**: Place in report's `input/` directory
- **Output Files**: Generated in report's `output/` directory

#### Email Distribution
- Production automatically emails configured recipients
- Business Intelligence team is CC'd on all production emails
- Development mode doesn't send emails (for safety)

### For System Administrators

#### Environment Setup
```bash
# Production environment
export REPORT_ENV=prod

# Development environment (default)
export REPORT_ENV=dev
```

#### Network Path Configuration
- Ensure network paths in `config.py` are accessible
- Validate service account permissions for automated execution
- Test file read/write permissions in production environments

#### Database Connectivity
- Reports using `cdutils.database.connect` require database access
- Verify connection strings and credentials
- Monitor database query performance for large reports

## 🔍 Monitoring & Maintenance

### Health Checks
1. **Execution Monitoring**: Track report success/failure rates
2. **File Generation**: Verify expected outputs are created
3. **Email Delivery**: Confirm distribution reaches recipients
4. **Database Performance**: Monitor query execution times

### Troubleshooting Common Issues

#### Report Fails to Execute
1. Check environment variable (`REPORT_ENV`)
2. Verify input file availability
3. Confirm database connectivity (if required)
4. Review file permissions for output directory

#### Email Distribution Problems
1. Verify Outlook installation and configuration
2. Check recipient email addresses in config
3. Ensure attachment files exist and are accessible
4. Review PowerShell/AppleScript execution permissions

#### File Path Issues
1. Confirm network path accessibility in production
2. Verify directory creation permissions
3. Check path format (use raw strings for Windows paths)
4. Validate environment-specific path switching

### Performance Optimization
- **Database Queries**: Optimize query performance for large datasets
- **File Processing**: Use efficient data processing libraries
- **Memory Management**: Monitor memory usage for large reports
- **Concurrent Execution**: Avoid resource conflicts when multiple reports run simultaneously

## 📞 Support & Contact

### Business Intelligence Team
- **Email**: businessintelligence@bcsbmail.com
- **Responsibilities**: 
  - Report development and maintenance
  - System architecture and standards
  - Technical support and troubleshooting
  - Performance optimization and monitoring

### Getting Help
1. **Technical Issues**: Contact BI team with error details
2. **Business Requirements**: Work with BI team to define report specifications
3. **New Report Requests**: Submit requirements through standard channels
4. **System Enhancements**: Propose improvements via BI team

---

**Document Version**: 2.0  
**Last Updated**: January 2025  
**Maintained By**: BCSB Business Intelligence Team