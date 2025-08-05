# Loan Conditions Matrix

## Project Overview

The Loan Conditions Matrix is an interactive web application designed for commercial lenders to walk through a series of questions about potential loans. Based on their responses and underlying mapping to loan policy, the system will dynamically display the specific requirements needed for that loan type.

This system replaces the manual process of looking up loan conditions in policy documents and provides a streamlined, automated approach to generating accurate loan requirement summaries.

## Authors & Stakeholders
- **Project Lead:** Chad Doorley 
- **Executive Sponsor:** Tim Chaves
- **Key Stakeholders:** Commercial Loan Officers, Credit, Loan Review
- **Subject Matter Experts:** Eldora Moore, Paul Kocak

## Project Goals

- Provide an intuitive interface for commercial lenders to assess loan requirements
- Automate the mapping of loan characteristics to policy requirements  
- Reduce processing time and improve accuracy in loan condition identification
- Ensure consistent application of loan policies across all commercial lending activities
- Create a self-service tool that reduces dependency on manual policy lookups
- Support conditional logic where questions appear based on previous answers
- Generate clear, formatted summaries that can be copied to loan files

## Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Architecture:** Modular design with separate questionnaire and policy mapping engines
- **Features:** Dynamic survey generation, conditional logic, progress tracking, copy-to-clipboard functionality
- **Deployment:** Static web application (hosted on internal web server or shared location)
- **Data:** JSON-based configuration for easy policy updates

## Current Implementation Features

### User Interface (`survey.html` equivalent)
- **Dynamic Survey Generation**: Questions and options based on JSON configuration
- **Conditional Logic**: Questions appear based on previous answers (e.g., "Yes" reveals follow-up questions)  
- **Multiple Question Types**: Radio buttons (single choice), checkboxes (multiple choice), text input
- **Progress Tracking**: Progress bar showing completion status
- **Requirements Summary**: Section-based summary of loan conditions
- **Copy to Clipboard**: Easy copying of generated requirements
- **Validation**: Ensures required questions are answered before summary generation

### Admin Panel (`admin.html` equivalent)  
- **Drag-and-Drop Configuration**: JSON file management via drag-and-drop
- **Section and Question Management**: Add, edit, delete, and duplicate survey elements
- **Option and Child Question Management**: Define multi-choice options with conditional logic
- **Real-time Editing**: Instant reflection of changes
- **Configuration Download**: Export survey configuration as JSON
- **Validation Tool**: Structure validation with error checking
- **Live Preview**: Visual preview of user experience
- **Embed Code Generation**: JSON for direct embedding in survey files

## Project Status
### Completed ✅
- Project structure and framework setup
- Basic HTML template with responsive design foundation
- Admin panel for survey configuration management
- User-facing survey interface with conditional logic
- JSON-based configuration system
- Copy-to-clipboard functionality for generated summaries
- Progress tracking and validation
- Multi-question type support (radio, checkbox, text input)

### Current Focus Areas
- **Policy Integration**: Mapping specific BCSB loan policies to survey logic
- **Question Refinement**: Based on subject matter expert feedback from Eldora & Paul
- **Condition Categories**: Appraisal, Environmental, Financial Statements, Flood, SWAP loans
- **Conditional Logic Enhancement**: Complex branching based on loan characteristics

### Future Enhancements
- Integration with loan origination systems
- User authentication and session management
- Analytics and usage tracking  
- Mobile optimization
- Automated policy updates from source documents

## File Paths

### Development
- **Source Code:** `Reports/Loan Conditions Matrix/src/`
- **Documentation:** `Reports/Loan Conditions Matrix/docs/`

### Production
- **Deployment:** Internal web server (TBD)
- **Configuration:** Environment-specific settings in config files

## Documentation

### Business Logic
The application guides commercial lenders through:
1. **Loan Type Identification**: Term loans, lines of credit, equipment financing, SWAP loans, SBA guaranteed loans
2. **Borrower Characteristics Assessment**: Industry, size, credit profile, guarantor requirements  
3. **Collateral and Security Requirements**: Real estate secured vs. unsecured, appraisal requirements
4. **Risk Assessment Factors**: Debt service coverage, loan-to-value ratios, environmental assessments
5. **Special Circumstances**: Flood zone determinations, SWAP checklist requirements, policy exceptions

### Key Survey Sections
- **Appraisal**: Loan-to-value calculations, appraisal age requirements, policy exceptions
- **Environmental**: Phase 1 assessments for CRE loans, abundance of caution considerations  
- **Financial Statements**: Corporate guarantor requirements, timing of submissions, interim statements
- **Flood**: Certificate generation, flood zone determinations, insurance requirements
- **SWAP**: Checklist completion, pre-closing documentation requirements

### Conditional Logic Examples
- **Real Estate Secured Loans**: Trigger appraisal, environmental, and flood sections
- **Non-RE Secured**: Skip flood and environmental assessments  
- **SBA Guaranteed with Building Contents**: Limited flood assessment requirements
- **Environmental Low Risk**: Simplified requirements path
- **SWAP Loans**: Specialized checklist and documentation requirements

### Key Features
- **Dynamic Questionnaire:** Progressive disclosure based on previous answers
- **Policy Mapping:** Real-time mapping of responses to specific loan conditions
- **Requirements Output:** Clear, formatted list of all applicable loan requirements
- **Export Functionality:** Ability to save or print requirements for loan files

### Data Sources
- Internal loan policy documentation
- Risk management guidelines
- Regulatory compliance requirements
- Historical loan condition precedents

---

# Template Project Structure & Usage Guide

This project follows a web application structure optimized for the BCSB monorepo system.

### Structure
```
Reports/Credit Loan Review/Loan Conditions Matrix/
├── docs/                   # Documentation, notes, and guides for the project
│   ├── README.md           # This file (project structure, business logic, usage guide)
│   └── project-notes.md    # Running development notes and implementation history
├── notebooks/              # Jupyter notebooks for analysis and development (currently empty)
└── src/                    # Source code for the application
    ├── policy_waterfall_phase2.html  # Main survey implementation
    └── assets/             # Static assets and configuration
        ├── admin.html      # Survey configuration admin panel
        ├── images/         # Images and icons directory
        └── survey-config-2025-05-24 (6).json  # Survey configuration file
```

### How to Use

1. **Development Setup**:
   - Open `src/policy_waterfall_phase2.html` in a web browser for the main survey interface
   - Use `src/assets/admin.html` for survey configuration management
   - Survey configuration stored in `src/assets/survey-config-*.json` files
   - Notebooks directory available for analysis and development work

2. **Survey Configuration**:
   - **Admin Panel**: Use `assets/admin.html` to create/edit survey questions and conditional logic
   - **JSON Configuration**: Current survey definition in `survey-config-2025-05-24 (6).json`
   - **Validation**: Built-in validation tools ensure proper survey structure
   - **Live Preview**: Test survey flow before deployment

3. **Core Files**:
   - **`policy_waterfall_phase2.html`**: Main survey application with embedded logic
   - **`admin.html`**: Configuration management interface
   - **`survey-config-*.json`**: Survey definitions and policy mappings
   - **`docs/project-notes.md`**: Development history and technical implementation notes

4. **Policy Management**:
   - Survey configurations stored as JSON files in `assets/`
   - Admin panel supports drag-and-drop configuration loading
   - Real-time editing with instant preview capabilities
   - Download updated configurations for version control

### Execution

- For local development: Open `src/policy_waterfall_phase2.html` in a web browser
- For configuration: Open `src/assets/admin.html` for survey management
- For production deployment: Deploy `src/` folder contents to web server
- Configuration is handled via JSON files in the `assets/` directory

### Best Practices

- Keep all configuration in JSON files within `assets/` directory for easy policy management
- Use the admin panel (`admin.html`) for survey structure modifications  
- Test survey logic thoroughly using the live preview functionality
- Implement responsive design for various screen sizes
- Document all policy mappings and business rules clearly in project notes
- Version control JSON configuration files for change tracking
- Test thoroughly across different browsers and devices

---

## Usage
```bash
# Navigate to project directory
cd "Reports/Credit Loan Review/Loan Conditions Matrix"

# Open main survey interface
open src/policy_waterfall_phase2.html

# Open admin configuration panel  
open src/assets/admin.html

# Or serve via local web server for testing
python -m http.server 8000
# Then navigate to http://localhost:8000/src/policy_waterfall_phase2.html
```

**Current Implementation**: 
- User survey interface with conditional logic (`policy_waterfall_phase2.html`)
- Admin panel for policy configuration (`assets/admin.html`)
- JSON-based survey definitions (`assets/survey-config-*.json`)
- Copy-to-clipboard functionality for generated requirements

**Schedule:** On-demand usage by commercial lending team

**Key Files:**
- `src/policy_waterfall_phase2.html` - Main user survey interface
- `src/assets/admin.html` - Configuration management panel
- `src/assets/survey-config-2025-05-24 (6).json` - Current policy definitions
- `docs/project-notes.md` - Development history and technical notes

---

This application is designed to be a user-friendly, self-service tool for commercial lenders to quickly and accurately determine loan requirements based on BCSB's lending policies and risk management guidelines.
