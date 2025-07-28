# Developer Guide

## BCSB Reports System Development Guide

This guide provides detailed instructions for developers working with the BCSB Reports System.

## 🚀 Quick Start

### Setting Up Development Environment

1. **Clone Repository**:
   ```bash
   git clone [repository-url]
   cd Reports
   ```

2. **Set Development Environment**:
   ```bash
   export REPORT_ENV=dev  # or set in your IDE
   ```

3. **Install Dependencies** (if needed):
   ```bash
   pip install pandas openpyxl sqlalchemy
   # Other dependencies as needed per report
   ```

4. **Test Framework Setup**:
   ```bash
   python run_tests.py  # Run all tests
   ```

## 📁 Creating a New Report

### Step 1: Directory Structure
```bash
mkdir -p "Reports/[Business_Line]/[Report_Name]/{src,input,output,assets,test}"
```

### Step 2: Create config.py
```python
"""
[Report Name] - [Business description]

Input Files: [List or "None"]
Output Files: [Description]
Tables: [List or "None"]
"""

import os
from pathlib import Path

# Report Info
REPORT_NAME = "Your Report Name"
BUSINESS_LINE = "Your Business Line"
SCHEDULE = "Daily"  # or Weekly/Monthly/Manual/As Needed
OWNER = "Your Team"

# Status
PROD_READY = False  # Set to True when ready

# Environment & Paths
ENV = os.getenv('REPORT_ENV', 'dev')
BASE_PATH = Path(r"\\PRODUCTION\PATH") if ENV == 'prod' else Path(__file__).parent.parent
OUTPUT_DIR = BASE_PATH / "output"
INPUT_DIR = BASE_PATH / "input"

# Email Recipients  
EMAIL_TO = ["recipient@bcsbmail.com"] if ENV == 'prod' else []
EMAIL_CC = ["businessintelligence@bcsbmail.com"] if ENV == 'prod' else []

# Creates directories
OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
```

### Step 3: Create main.py with Business Logic Documentation
```python
"""
[Report Name] - Main Entry Point

BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- [Describe your data sources]
- [Explain relationships between data]

Business Rules:
- [Key business rules]
- [Filtering criteria]  
- [Calculations and logic]

Data Processing Flow:
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

Key Calculations:
- [Important formulas]
- [Business calculations]

Business Intelligence Value:
- [How this supports business decisions]
- [Key insights provided]
"""

import pandas as pd
from datetime import datetime
import src.config

def main():
    """Main report execution."""
    print(f"Starting {src.config.REPORT_NAME}")
    
    # Your business logic here
    
    # Generate output
    output_file = src.config.OUTPUT_DIR / "report_output.xlsx"
    
    # Email distribution
    if src.config.EMAIL_TO:
        import cdutils.distribution
        cdutils.distribution.email_out(
            recipients=src.config.EMAIL_TO,
            cc_recipients=src.config.EMAIL_CC,
            subject=f"{src.config.REPORT_NAME} - {datetime.now().strftime('%Y-%m-%d')}",
            body="Please find attached the report.",
            attachment_paths=[output_file]
        )
        print(f"Email sent to {len(src.config.EMAIL_TO)} recipients")
    else:
        print("Development mode - email not sent")

if __name__ == "__main__":
    main()
```

### Step 4: Create Test Configuration
```json
{
  "description": "Test [Report Name]",
  "skip": false,
  "expected_outputs": [
    "report_output.xlsx"
  ],
  "notes": "Any special requirements for testing"
}
```

### Step 5: Test Your Report
```bash
python run_tests.py "Your Report Name"
```

## 🔧 Development Best Practices

### Configuration Management

#### DO ✅
```python
# Use config values
output_path = src.config.OUTPUT_DIR / "report.xlsx"

# Environment-aware logic
if src.config.ENV == 'prod':
    # Production-specific logic
    pass

# Check recipients before emailing
if src.config.EMAIL_TO:
    # Send email
    pass
```

#### DON'T ❌
```python
# Hard-code paths
output_path = Path("C:\\Reports\\output\\report.xlsx")

# Use deprecated patterns
def main(production_flag=False):
    pass

# Put complex logic in config.py
def complex_calculation():
    pass
```

### Business Logic Documentation

#### Required Sections
1. **Data Sources & Relationships**: What data you use and how it connects
2. **Business Rules**: The logic and rules that drive the report
3. **Data Processing Flow**: Step-by-step process description
4. **Key Calculations**: Important formulas and business calculations
5. **Business Intelligence Value**: How this helps business decisions

#### Example Documentation
```python
"""
BUSINESS LOGIC EXTRACTED:

Data Sources & Relationships:
- COCCDM.WH_RTXN table for transaction history
- Filters to account 150523994.00 (vendor) and 150524009.00 (payroll)
- 30-day lookback period for analysis

Business Rules:
- Only include transactions with non-null check numbers
- Convert all amounts to positive values for output
- Format payroll as fixed-width text, vendor as CSV
- Pad check numbers to 10 digits with leading zeros

Data Processing Flow:
1. Query last 30 days of transactions from both accounts
2. Apply filtering criteria for valid transactions
3. Format payroll data as fixed-width text file
4. Format vendor data as CSV with specific column structure
5. Output both files to designated directories

Key Calculations:
- Date range: Current date minus 30 days
- Amount formatting: Remove decimals, pad to 10 digits
- Check number formatting: Pad to 10 digits with leading zeros

Business Intelligence Value:
- Government banking transaction monitoring
- Audit trail for payroll and vendor payments
- Automated formatting for downstream processing systems
"""
```

### Database Integration

#### Using cdutils.database.connect
```python
import cdutils.database.connect
from sqlalchemy import text

def fetch_data():
    query = text("""
        SELECT column1, column2
        FROM table_name
        WHERE condition = :param
    """)
    
    queries = [
        {'key': 'data', 'sql': query, 'engine': 2}
    ]
    
    data = cdutils.database.connect.retrieve_data(queries)
    return data['data']
```

#### Best Practices
- Use parameterized queries to prevent SQL injection
- Specify the correct engine number (1 or 2)
- Handle database connection errors gracefully
- Test queries in development environment first

### File Processing

#### Path Management
```python
# ✅ Use config paths
input_file = src.config.INPUT_DIR / "input.xlsx"
output_file = src.config.OUTPUT_DIR / "output.xlsx"

# ✅ Check file existence
if input_file.exists():
    df = pd.read_excel(input_file)
else:
    print(f"Input file not found: {input_file}")
    return
```

#### Excel Operations
```python
# Reading Excel files
df = pd.read_excel(input_file, sheet_name="Sheet1")

# Writing Excel files with formatting
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='Data', index=False)
    
    # Apply formatting if needed
    workbook = writer.book
    worksheet = writer.sheets['Data']
    # Add formatting code here
```

### Email Distribution

#### Standard Pattern
```python
if src.config.EMAIL_TO:
    import cdutils.distribution
    
    subject = f"{src.config.REPORT_NAME} - {datetime.now().strftime('%Y-%m-%d')}"
    body = """Hi,

Attached is the {report_name}. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com

Thanks!""".format(report_name=src.config.REPORT_NAME)
    
    cdutils.distribution.email_out(
        recipients=src.config.EMAIL_TO,
        cc_recipients=src.config.EMAIL_CC,
        subject=subject,
        body=body,
        attachment_paths=[output_file]
    )
    print(f"Email sent to {len(src.config.EMAIL_TO)} recipients")
else:
    print("Development mode - email not sent")
```

#### Email Best Practices
- Always check if recipients are configured before sending
- Use descriptive subject lines with dates
- Include standard footer with BI contact
- Verify attachment files exist before sending

### Error Handling

#### Comprehensive Error Handling
```python
def main():
    try:
        print(f"Starting {src.config.REPORT_NAME}")
        
        # Your report logic here
        
        print(f"Completed {src.config.REPORT_NAME}")
        
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return False
    except Exception as e:
        print(f"Error in {src.config.REPORT_NAME}: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
```

## 🧪 Testing Your Report

### Local Testing
```bash
# Test single report
python run_tests.py "Your Report Name"

# Test with production file sync
python run_tests.py "Your Report Name" --sync
```

### Manual Testing Checklist
- [ ] Report runs without errors in development mode
- [ ] Expected output files are generated
- [ ] File formats and content are correct
- [ ] No emails sent in development mode
- [ ] Database queries execute successfully (if applicable)
- [ ] Input files are processed correctly (if applicable)

### Production Testing
```bash
# Set production environment
export REPORT_ENV=prod

# Test (carefully!)
python Reports/Business_Line/Report_Name/src/main.py
```

## 🔄 Migrating Existing Reports

### Migration Checklist

1. **Backup Original Code**
2. **Analyze Current Configuration**:
   - Identify hard-coded paths
   - Find email configuration patterns
   - Locate complex configuration logic

3. **Apply Standard Template**:
   - Replace config.py with standard template
   - Fill in report-specific values
   - Set production network path

4. **Move Complex Logic**:
   - Move functions from config.py to main.py
   - Move large data structures to main.py
   - Keep config.py simple

5. **Update main.py**:
   - Add business logic documentation
   - Update imports to use src.config
   - Replace deprecated patterns
   - Standardize email distribution

6. **Test Migration**:
   - Test in development mode
   - Verify output files are identical
   - Test email distribution (carefully)
   - Run automated tests

### Common Migration Issues

#### Path Issues
```python
# Before
OUTPUT_PATH = "C:\\Reports\\Output"

# After  
output_file = src.config.OUTPUT_DIR / "filename.xlsx"
```

#### Email Issues
```python
# Before
EMAIL_BCC = ["user@example.com"]
send_email(bcc=EMAIL_BCC)

# After
if src.config.EMAIL_TO:
    cdutils.distribution.email_out(
        recipients=src.config.EMAIL_TO,
        cc_recipients=src.config.EMAIL_CC,
        # ...
    )
```

#### Environment Issues
```python
# Before
def main(production_flag=False):
    if production_flag:
        # production logic

# After
def main():
    if src.config.ENV == 'prod':
        # production logic
```

## 🐛 Debugging Common Issues

### Import Errors
```python
# If you get import errors, check:
# 1. Python path includes the src directory
# 2. All required dependencies are installed
# 3. File names and module names are correct

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
import config
```

### Path Errors
```python
# Debug path issues
print(f"Current working directory: {os.getcwd()}")
print(f"Config file location: {Path(__file__).parent}")
print(f"Environment: {os.getenv('REPORT_ENV', 'dev')}")
print(f"Base path: {src.config.BASE_PATH}")
print(f"Output dir exists: {src.config.OUTPUT_DIR.exists()}")
```

### Email Issues
```python
# Debug email configuration
print(f"Email TO recipients: {len(src.config.EMAIL_TO)}")
print(f"Email CC recipients: {len(src.config.EMAIL_CC)}")
print(f"Environment: {src.config.ENV}")

# Test email without sending
if src.config.EMAIL_TO:
    print("Would send email to:", src.config.EMAIL_TO)
else:
    print("No email recipients configured")
```

## 📚 Additional Resources

- [CONFIGURATION_GUIDE.md](CONFIGURATION_GUIDE.md) - Detailed configuration reference
- [test_framework/README.md](test_framework/README.md) - Testing system documentation  
- [cdutils/cdutils/README_distribution.md](cdutils/cdutils/README_distribution.md) - Email distribution guide

## 💡 Getting Help

### Before Asking for Help
1. Check this documentation
2. Review similar reports for examples
3. Test in development environment first
4. Check error messages and logs

### How to Ask for Help
1. Describe what you're trying to do
2. Include the exact error message
3. Share relevant code snippets
4. Mention what you've already tried

### Contact
- **Business Intelligence Team**: businessintelligence@bcsbmail.com
- **Include**: Report name, error details, and steps to reproduce

---

**Maintained By**: BCSB Business Intelligence Team