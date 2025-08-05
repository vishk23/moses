# Loan Conditions Matrix - Project Notes

## Overview
Interactive web application for commercial lenders to determine loan requirements based on loan characteristics and bank policy.

## File Structure
```
Reports/Loan Conditions Matrix/
├── src/
│   ├── index.html          # Main application interface
│   ├── config.js           # Application configuration
│   ├── app.js              # Main application controller
│   ├── modules/
│   │   ├── questionnaire.js  # Question logic and flow
│   │   └── policyMapping.js  # Policy rules and requirements
│   ├── styles/
│   │   ├── styles.css        # Global styles
│   │   └── questionnaire.css # Questionnaire-specific styles
│   └── assets/
│       └── images/           # Application images
├── docs/
│   └── project_notes.md      # This file
└── README.md                 # Project documentation
```

## Key Features
1. **Interactive Questionnaire**: Step-by-step questions about loan characteristics
2. **Dynamic Requirements**: Real-time calculation of required documents/conditions
3. **Policy Integration**: Mapping of answers to specific bank policies
4. **Export Functionality**: Print and save results
5. **Session Management**: Temporary storage of progress

## Technical Notes
- Pure HTML/CSS/JavaScript (no external dependencies)
- Responsive design for desktop and mobile
- Modular architecture for easy maintenance
- Local storage for session persistence

## Development Status
- ✅ Project structure created
- ✅ Core modules implemented
- ✅ Styling completed
- ⏳ Testing and refinement needed
- ⏳ Policy data integration needed

## Next Steps
1. Test the application in a browser
2. Refine questionnaire flow based on lender feedback
3. Add specific policy mappings for BCSB loan products
4. Integrate with existing systems if needed
5. Deploy to production environment

## Usage
Open `src/index.html` in a web browser to start the application.
