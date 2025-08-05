# Loan Conditions Matrix

## Project Overview
This web application helps commercial lenders walk through a series of questions. Based on their answers and the underlying mapping to loan policy, it lists out the requirements needed for that loan.

## Authors & Stakeholders
- **Project Lead:** Commercial Lending Team
- **Executive Sponsor:** Chief Lending Officer
- **Key Stakeholders:** Commercial Lenders, Credit Analysts

## Project Goals
- Streamline loan conditions assessment for commercial lending
- Provide a dynamic, policy-driven requirements checklist
- Improve compliance and consistency in loan origination

## Technology Stack
- **Frontend:** HTML, CSS, JavaScript
- **Modules:** Question Flow, Policy Mapping

## Project Status
### Completed ✅
- Starter structure and documentation

### Future Enhancements
- Add backend integration for policy updates
- Add user authentication and audit logging

## File Paths
- `docs/` - Documentation and guides
- `notebooks/` - Prototyping and design notes
- `src/` - Source code (HTML, JS modules)

## Documentation
- This file (project structure, business logic, usage guide)

---

# Template Project Structure & Usage Guide

This folder provides a starter template for the Loan Conditions Matrix web application. Copy this folder and use it as a base for new work.

### Structure
```
Loan Conditions Matrix/
├── docs/                   # Documentation, notes, and guides for the project
│   └── README.md           # This file (project structure, business logic, usage guide)
├── notebooks/              # Prototyping, design notes, or UI sketches
├── src/                    # Source code for the project
│   ├── index.html          # Main HTML entry point
│   ├── modules/            # JavaScript modules for app logic
│   │   ├── questionFlow.js # Handles question/answer logic and UI
│   │   └── policyMapping.js# Maps answers to loan policy requirements
│   └── styles.css          # App-wide CSS styles
```

### How to Use

1. **Copy the entire `Loan Conditions Matrix` folder** to your new project location and rename as needed.
2. **Edit `src/index.html`** to update project title, branding, and layout.
3. **Implement your question flow logic in `src/modules/questionFlow.js`.**
4. **Implement your policy mapping logic in `src/modules/policyMapping.js`.**
5. **Document your project** in the `docs/` folder and keep notes up to date.
6. **Use the `notebooks/` folder** for prototyping, design notes, or UI sketches.

### Execution
- Open `src/index.html` in your browser to run the app.
- All logic should be modularized in the `modules/` folder for maintainability.

### Best Practices
- Keep all business logic in JS modules for clarity and reusability.
- Avoid hardcoding policy rules in HTML; use mapping logic in JS.
- Keep documentation and design notes organized for future reference.
- Use the provided structure for easy integration and maintainability.

---

## Usage
```bash
# Open the app in your browser
open Reports/Loan Conditions Matrix/src/index.html
```

---

This template is designed to be a clean, robust, and reusable starting point for any new web-based loan conditions matrix project. Follow the structure and conventions for seamless integration and maintainability.
