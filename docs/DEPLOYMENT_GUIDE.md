# Deployment Guide

## BCSB Reports System Deployment & Operations

This guide covers deployment, configuration, and operational procedures for the BCSB Reports System in production environments.

## 🎯 Deployment Overview

### Deployment Architecture
```
Production Environment
├── Application Server
│   ├── Reports Repository
│   ├── Python Runtime
│   └── Scheduling System
├── Network File Storage
│   ├── Input Files (\\00-DA1\...)
│   ├── Output Files  
│   └── Archive Storage
├── Database Servers
│   ├── (Engine 1)
│   └── (Engine 2)
└── Email System
    └── Microsoft Outlook/Exchange
```

### Environment Requirements
- **Python**: 3.8+ with required packages
- **Network Access**: Read/write to configured network paths
- **Database Access**: Connections to OSIBANK and COCCDM
- **Email System**: Microsoft Outlook integration
- **Scheduling**: Windows Task Scheduler or equivalent

## 🚀 Production Deployment

### Step 1: Environment Setup

#### Python Environment
```bash
# Install Python 3.11+
# Install required packages
pip install pandas openpyxl sqlalchemy pyodbc

# Verify installation
python --version
python -c "import pandas, openpyxl, sqlalchemy; print('Dependencies OK')"
```

#### Environment Variables
```bash
# Set production environment
set REPORT_ENV=prod

# Verify environment
python -c "import os; print('Environment:', os.getenv('REPORT_ENV', 'dev'))"
```

### Step 2: Network Configuration

#### Validate Network Paths
Test access to all configured network paths:
```python
# Test script: validate_paths.py
from pathlib import Path
import sys

paths_to_test = [
    r"\\00-DA1\Home\Share\Data & Analytics Initiatives\Project Management",
    r"\\00-berlin\Operations\Loan Servicing\Daily Rate Updates",
    # Add other production paths
]

for path in paths_to_test:
    try:
        p = Path(path)
        if p.exists():
            print(f"✅ {path} - Accessible")
            # Test write permissions
            test_file = p / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            print(f"✅ {path} - Writable")
        else:
            print(f"❌ {path} - Not accessible")
    except Exception as e:
        print(f"❌ {path} - Error: {e}")
```

#### Service Account Permissions
Ensure the service account has:
- **Read access** to all input file locations
- **Write access** to all output file locations  
- **Execute permissions** for Python and PowerShell
- **Database connections** to OSIBANK and COCCDM

### Step 3: Database Configuration

#### Connection Testing
```python
# Test database connections
import cdutils.database.connect
from sqlalchemy import text

def test_database_connections():
    try:
        # Test simple query on each engine
        queries = [
            {'key': 'test1', 'sql': text("SELECT 1 as test"), 'engine': 1},
            {'key': 'test2', 'sql': text("SELECT 1 as test"), 'engine': 2}
        ]
        
        results = cdutils.database.connect.retrieve_data(queries)
        print("✅ Database connections successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

test_database_connections()
```

### Step 4: Email System Configuration

#### Outlook Integration Testing
```python
# Test email functionality
import cdutils.distribution

try:
    # Test email preparation (doesn't send)
    cdutils.distribution.email_out(
        recipients=["test@bcsbmail.com"],
        cc_recipients=["businessintelligence@bcsbmail.com"],
        subject="Test Email - System Validation",
        body="This is a test email for system validation."
    )
    print("✅ Email system configured correctly")
except Exception as e:
    print(f"❌ Email system error: {e}")
```

### Step 5: Report Validation

#### Pre-deployment Testing
```bash
# Test all reports in production environment
REPORT_ENV=prod python run_tests.py

# Test specific critical reports
REPORT_ENV=prod python run_tests.py "Rate Scraping"
REPORT_ENV=prod python run_tests.py "Business_Concentration_of_Deposits"
```

#### Note for Windows Powershell, you set environment variable via the below syntax:
```Powershell
$env:REPORT_ENV="prod"
```

#### Validation Checklist
- [ ] All expected output files generated
- [ ] File formats and content correct
- [ ] Email distribution works properly
- [ ] Database queries execute successfully
- [ ] Network file operations complete
- [ ] No errors in execution logs

## ⏰ Scheduling Configuration

### Windows Task Scheduler

#### Create Scheduled Task
```batch
# Example task creation
schtasks /create /tn "BCSB_Rate_Scraping_Daily" ^
    /tr "C:\Python\python.exe C:\Reports\Operations\Rate Scraping\src\main.py" ^
    /sc daily /st 06:00 /ru "DOMAIN\ServiceAccount"
```

#### Task Configuration Template
```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>BCSB Rate Scraping Daily Report</Description>
  </RegistrationInfo>
  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2025-01-01T06:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>C:\Python\python.exe</Command>
      <Arguments>C:\Reports\Operations\Rate Scraping\src\main.py</Arguments>
      <WorkingDirectory>C:\Reports\Operations\Rate Scraping</WorkingDirectory>
    </Exec>
  </Actions>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
  </Settings>
</Task>
```

### Scheduling Best Practices

#### Timing Considerations
- **Rate Scraping**: Early morning (6:00 AM) after markets open
- **Deposit Reports**: After nightly database updates (7:00 AM)
- **Month-end Reports**: First business day of month (8:00 AM)
- **Weekly Reports**: Monday mornings (7:30 AM)

#### Resource Management
- **Stagger execution**: Avoid running multiple reports simultaneously
- **Set timeouts**: Configure maximum execution time
- **Error handling**: Configure retry policies and failure notifications
- **Logging**: Enable comprehensive logging for troubleshooting

## 📊 Monitoring & Alerting

### Execution Monitoring

#### Log Analysis
```python
# Example log monitoring script
import re
from pathlib import Path
from datetime import datetime, timedelta

def check_report_logs(log_dir, hours_back=24):
    """Check for report failures in the last N hours."""
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    failures = []
    
    for log_file in Path(log_dir).glob("*.log"):
        if log_file.stat().st_mtime > cutoff_time.timestamp():
            content = log_file.read_text()
            if re.search(r"ERROR|FAILED|Exception", content, re.IGNORECASE):
                failures.append(log_file.name)
    
    return failures
```

#### Health Check Script
```python
# health_check.py - Run periodically to validate system health
def system_health_check():
    checks = {
        "database": test_database_connections(),
        "network_paths": validate_network_access(),
        "email_system": test_email_configuration(),
        "python_environment": verify_dependencies()
    }
    
    all_healthy = all(checks.values())
    
    if not all_healthy:
        send_alert("System Health Check Failed", checks)
    
    return all_healthy
```

### Alert Configuration

#### Critical Alerts
- **Report Execution Failures**: Immediate notification
- **Database Connection Issues**: High priority
- **Network Path Access Problems**: High priority
- **Email Distribution Failures**: Medium priority

#### Alert Recipients
- **Technical Issues**: Business Intelligence Team
- **Business Issues**: Report owners and stakeholders
- **System Issues**: IT Operations Team

## 🔧 Maintenance Procedures

### Regular Maintenance Tasks

#### Daily
- [ ] Review execution logs for errors
- [ ] Verify report output generation
- [ ] Check email delivery confirmations
- [ ] Monitor system resource usage

#### Weekly  
- [ ] Validate database connections
- [ ] Test network path accessibility
- [ ] Review and archive old output files
- [ ] Update production file sync for development

#### Monthly
- [ ] Review and update report schedules
- [ ] Analyze performance metrics
- [ ] Update documentation
- [ ] Test disaster recovery procedures

#### Quarterly
- [ ] Review and update network paths
- [ ] Validate email distribution lists
- [ ] Performance optimization review
- [ ] Security assessment and updates

### Update Procedures

#### Code Updates
1. **Test in Development**: Validate all changes thoroughly
2. **Backup Production**: Create backup of current production code
3. **Deploy to Staging**: Test in production-like environment
4. **Schedule Deployment**: Deploy during low-activity periods
5. **Validate Deployment**: Run comprehensive tests post-deployment
6. **Monitor Execution**: Watch first few scheduled runs closely

#### Configuration Updates
1. **Document Changes**: Record all configuration modifications
2. **Test Impact**: Validate changes don't break existing functionality
3. **Staged Rollout**: Update one report at a time
4. **Rollback Plan**: Prepare rollback procedures for issues

### Backup & Recovery

#### Backup Strategy
- **Code Repository**: Regular git backups
- **Configuration Files**: Daily backup of all config.py files
- **Output Archives**: Weekly backup of report outputs
- **Database Queries**: Version control for all SQL queries

#### Recovery Procedures
1. **Code Recovery**: Restore from git repository
2. **Configuration Recovery**: Restore from config backups
3. **Data Recovery**: Restore from network storage backups
4. **System Recovery**: Full system restore procedures

## 🔍 Troubleshooting

### Common Production Issues

#### Report Execution Failures

**Symptoms**: Scheduled reports not running or failing
**Causes**: 
- Environment variable not set
- Network path access issues
- Database connection problems
- Missing input files

**Resolution**:
```bash
# Check environment
echo %REPORT_ENV%

# Test database connection
python -c "import cdutils.database.connect; print('DB OK')"

# Test network paths
python validate_paths.py

# Check input files
dir "\\network\path\to\input\"
```

#### Email Distribution Issues

**Symptoms**: Reports generating but emails not sent
**Causes**:
- Outlook not configured
- PowerShell execution policy
- Attachment file access issues
- Recipient list configuration

**Resolution**:
```powershell
# Check PowerShell execution policy
Get-ExecutionPolicy

# Set execution policy if needed
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Test Outlook automation
$outlook = New-Object -ComObject Outlook.Application
$mail = $outlook.CreateItem(0)
$mail.Display()
```

#### Performance Issues

**Symptoms**: Reports taking too long to execute
**Causes**:
- Database query performance
- Large file processing
- Network latency
- Resource contention

**Resolution**:
- Optimize database queries
- Implement data processing in chunks
- Schedule reports to avoid conflicts
- Monitor system resources

### Emergency Procedures

#### Critical Report Failure
1. **Immediate Response**: Notify stakeholders of issue
2. **Quick Fix**: Attempt manual execution if possible  
3. **Root Cause Analysis**: Identify and document issue
4. **Permanent Fix**: Implement solution and test
5. **Post-Incident Review**: Review and improve procedures

#### System-Wide Outage
1. **Assessment**: Determine scope and impact
2. **Communication**: Notify all affected stakeholders
3. **Escalation**: Engage appropriate technical resources
4. **Recovery**: Execute recovery procedures
5. **Validation**: Verify all systems operational
6. **Documentation**: Document incident and lessons learned

## 📞 Support Contacts

### Escalation Matrix

#### Level 1: Business Intelligence Team
- **Email**: businessintelligence@bcsbmail.com
- **Scope**: Report issues, configuration problems, minor system issues
- **Response Time**: 2-4 hours during business hours

#### Level 2: IT Operations
- **Scope**: System outages, network issues, database problems
- **Response Time**: 1-2 hours for critical issues

#### Level 3: Vendor Support
- **Scope**: Major system failures, infrastructure issues
- **Response Time**: As per support contract

### Emergency Contacts
- **After Hours**: [Emergency contact information]
- **Critical Systems**: [24/7 support contact]
- **Management Escalation**: [Management contact chain]

---

**Document Version**: 2.0  
**Last Updated**: January 2025  
**Maintained By**: BCSB Business Intelligence Team