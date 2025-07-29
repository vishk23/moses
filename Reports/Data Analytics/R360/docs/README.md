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
- [x] Create address-only persistent key (for household analysis)
  - Sep 2024
- [x] Create ownership-only key that is persistent (for Concentration of Credit reporting)
  - Sep 2024
- [x] Update cdutils from src.cdutils to shared library
  - Oct 2024
- [x] Create workflow specific storage for portfolio key (SQLite)
  - Nov 2025
- [x] Develop ability to modify key if certain shared attributes should not group relationships
  - Dec 2024
- [x] Fix IOLTA shared ownership issues (RI BAR & MA IOLTA Committee)
  - Jan 2025
- [x] Fix address grouping issues (29 Broadway exclusion)
  - Jan 2025
- [x] Create portfolio key with persistence across runs
  - May 2025
- [x] Upload keys into HHNU userfield in COCC
  - Jun 2025

### Future Enhancements
- [ ] Create GUI or Excel-based way to manage relationship exceptions, give end users or admins ability to make modifications to relationship
    - To be determined whether this is a worthy use of time.


## File Paths
- **Production Home:** Reports/Data Analytics/R360
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

