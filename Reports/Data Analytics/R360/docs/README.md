# R360 Customer Relationship Keys

## Project Overview
This project creates centralized customer relationship keys to provide a 360-degree view of customers across different dimensions for various business line applications.

## Authors & Stakeholders
- **Project Lead:** Chad Doorley (chad.doorley@bcsbmail.com)
- **Executive Sponsor:** Tom Foresta
- **Key Stakeholders:**
  - Tim Chaves (Business Line Owner)
  - Francine Ferguson (Business Line Owner)
  - Kati Kelly (Business Line Owner)
  - Retail, Commercial, Marketing Departments

## Project Goals
- Create a centralized key system to better understand Bank customers
- Generate three types of relationship keys:
  - **Portfolio Key:** Groups by address OR ownership (comprehensive relationships)
  - **Address Key:** Groups by address only (household analysis)
  - **Ownership Key:** Groups by ownership only (business concentration analysis)
- Develop robust data pipeline with consistent key generation over time
- Store in database (SQLite for development, targeting COCC for production)

## Technology Stack
- **Language:** Python
- **Database:** SQLite (development), targeting COCC (production)
- **Algorithm:** Union-Find for efficient relationship grouping
- **Integration:** cdutils library for system-wide access

## Project Status
### Completed ✅
- [x] Create portfolio key with persistence across runs
- [x] Create storage for portfolio key (SQLite)
- [x] Fix address grouping issues (29 Broadway exclusion)
- [x] Fix IOLTA shared ownership issues (RI BAR & MA IOLTA Committee)
- [x] Develop ability to modify key if certain shared attributes should not group relationships
- [x] Disable current.db and update references to use cdutils
- [x] Update cdutils from src.cdutils to shared library
- [x] Create ownership-only key that is persistent (for Concentration of Credit reporting)
- [x] Create address-only persistent key (for household analysis)

### Future Enhancements
- [ ] Create GUI or Excel-based way to manage relationship exceptions, give end users or admins ability to make modifications to relationship
    - To be determined whether this is a worthy use of time.


## File Paths
- **Production Home:** `\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\R360`
- **Development:** Local project structure with src/, docs/, notebooks/ directories

## Documentation
- [Executive Overview](./executive-overview.md) - Business-focused overview and impact
- [Project Notes](./project-notes.md) - Comprehensive technical documentation and running notes

## Usage
```bash
# Navigate to project directory
cd Reports/Data\ Analytics/R360

# Run the main process
python -m src.main
```

**Schedule:** Daily automated execution

