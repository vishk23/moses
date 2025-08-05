# Loan Conditions Matrix

## Project Overview

The Loan Conditions Matrix is an interactive web application designed for commercial lenders to walk through a series of questions about potential loans. Based on their responses and underlying mapping to loan policy, the system will dynamically display the specific requirements needed for that loan type.

## Authors & Stakeholders
- **Project Lead:** Business Intelligence Team
- **Executive Sponsor:** Commercial Banking
- **Key Stakeholders:** Commercial Loan Officers, Credit Risk Management, Loan Operations

## Project Goals

- Provide an intuitive interface for commercial lenders to assess loan requirements
- Automate the mapping of loan characteristics to policy requirements
- Reduce processing time and improve accuracy in loan condition identification
- Ensure consistent application of loan policies across all commercial lending activities
- Create a self-service tool that reduces dependency on manual policy lookups

## Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Modules:** Two core JavaScript modules for questionnaire logic and policy mapping
- **Assets:** CSS stylesheets, images, configuration files
- **Deployment:** Static web application (can be hosted on internal web server)

## Project Status
### Completed ✅
- Project structure and framework setup
- Basic HTML template with responsive design foundation

### Future Enhancements
- Interactive questionnaire module implementation
- Policy mapping engine development
- Results display and export functionality
- User authentication and session management
- Analytics and usage tracking
- Integration with loan origination systems

## File Paths

### Development
- **Source Code:** `Reports/Loan Conditions Matrix/src/`
- **Documentation:** `Reports/Loan Conditions Matrix/docs/`

### Production
- **Deployment:** Internal web server (TBD)
- **Configuration:** Environment-specific settings in config files

## Documentation

### Business Logic
The application will guide commercial lenders through:
1. Loan type identification (term loans, lines of credit, equipment financing, etc.)
2. Borrower characteristics assessment (industry, size, credit profile)
3. Collateral and security requirements evaluation
4. Risk assessment factors (debt service coverage, loan-to-value ratios)
5. Special circumstances and exceptions handling

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
loan_conditions_matrix/
├── docs/                   # Documentation, notes, and guides for the project
│   └── README.md           # This file (project structure, business logic, usage guide)
├── src/                    # Source code for the application
│   ├── index.html          # Main HTML page (entry point)
│   ├── config.js           # Application configuration and environment settings
│   ├── modules/            # Core JavaScript modules
│   │   ├── questionnaire.js    # Questions logic and user interface
│   │   └── policyMapping.js    # Policy mapping and requirements engine
│   └── assets/             # Static assets
│       ├── css/            # Stylesheets
│       ├── images/         # Images and icons
│       └── data/           # Configuration files and policy data
```

### How to Use

1. **Development Setup**:
   - Open `src/index.html` in a web browser for local development
   - Edit `src/config.js` for environment-specific settings
   - Modify modules in `src/modules/` for business logic

2. **Core Development Areas**:
   - **`index.html`**: Main application structure and layout
   - **`config.js`**: Application settings, API endpoints, environment configuration
   - **`questionnaire.js`**: User interface logic, question flow, form validation
   - **`policyMapping.js`**: Business rules engine, policy lookup, requirements generation

3. **Static Assets**:
   - Place stylesheets in `src/assets/css/`
   - Store images and icons in `src/assets/images/`
   - Keep policy data and configuration in `src/assets/data/`

### Execution

- For local development: Open `src/index.html` in a web browser
- For production deployment: Deploy entire `src/` folder to web server
- Configuration is handled via `config.js` for environment-specific settings

### Best Practices

- Keep all configuration in `config.js` for easy environment management
- Separate business logic into discrete modules (`questionnaire.js`, `policyMapping.js`)
- Use modern JavaScript (ES6+) features and best practices
- Implement responsive design for various screen sizes
- Document all policy mappings and business rules clearly
- Test thoroughly across different browsers and devices

---

## Usage
```bash
# Navigate to project directory
cd "Reports/Loan Conditions Matrix"

# Open in browser for development
open src/index.html

# Or serve via local web server
python -m http.server 8000
```

**Schedule:** On-demand usage by commercial lending team

---

This application is designed to be a user-friendly, self-service tool for commercial lenders to quickly and accurately determine loan requirements based on BCSB's lending policies and risk management guidelines.
