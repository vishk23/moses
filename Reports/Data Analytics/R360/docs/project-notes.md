# R360 Customer Relationship Keys - Project Notes

*Consolidated documentation and running notes for the R360 project*

---

## Current Development Status (2025-07-25)

### Recent Issues & Resolutions

**Unicode Encoding Error (Windows)**
- **Issue:** R360 fails when run through testing framework due to Unicode emoji characters in config.py
- **Error:** `UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f527'`
- **Solution:** Set `PYTHONIOENCODING=utf-8` environment variable in subprocess execution
- **Status:** Fixed in testing framework

**Testing Framework Integration**
- **Issue:** R360 runs successfully with direct `python -m src.main` but fails through `run_reports.py --daily`
- **Root Cause:** Virtual environment and Unicode encoding issues in subprocess execution
- **Solution:** Updated `run_reports.py` to use virtual environment Python and UTF-8 encoding
- **Status:** Resolved

### Current Configuration
- **Environment:** Dev mode with database operations disabled for safety
- **Historical DB:** Disabled (can be re-enabled in config)
- **Key Generation:** All three key types (portfolio, address, ownership) active
- **Storage:** SQLite databases in project directory during dev

---

## Project Overview & Documentation Archive

### Authors & Stakeholders
- **Project Lead:** Chad Doorley (chad.doorley@bcsbmail.com)
- **Executive Sponsor:** Tom Foresta
- **Key Stakeholders:**
  - Tim Chaves (Business Line Owner)
  - Francine Ferguson (Business Line Owner) 
  - Kati Kelly (Business Line Owner)
  - Retail, Commercial, Marketing Departments

### Project Goals
The goal is to create a centralized key to better understand the Bank's customers. This involves the creation of relationship keys (portfolio_key, address_key, ownership_key) which group customers based on different relationship criteria:

- **Portfolio Key:** Groups by address OR ownership (superhousehold/comprehensive relationships)
- **Address Key:** Groups by address only (household analysis)
- **Ownership Key:** Groups by ownership only (business concentration analysis)

### Technology Stack
- **Language:** Python
- **Database:** SQLite (development), targeting COCC (production)
- **Algorithm:** Union-Find for efficient relationship grouping
- **Integration:** cdutils library for system-wide access

### File Paths
- **Production Home:** `\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\R360`
- **Development:** Local project structure with src/, docs/, notebooks/ directories

---

## Technical Implementation Details

### Core Business Logic
1. **Data Extraction:** Pull account common, address, and ownership data from OSIBANK warehouse tables
2. **Data Cleaning:** Apply business rules and create hash keys for address and ownership matching
3. **Relationship Grouping:** Use Union-Find algorithm to group accounts by specified criteria
4. **Key Assignment:** Assign persistent keys using historical data for consistency
5. **Storage:** Store results in SQLite databases for downstream consumption
6. **Integration:** Make available via cdutils for use across all systems

### Key Business Rules
- **IOLTA Exclusions:** Exclude legal trust accounts from grouping
- **Address Exclusions:** Exclude problematic shared business addresses (e.g., "29 Broadway")
- **Ownership Filtering:** Handle null CIFs and IOLTA committee structures
- **Persistence:** Keys remain stable across daily runs using historical databases

### Data Sources
- `OSIBANK.WH_ACCTCOMMON` - Account data
- `PERSADDRUSE`, `ORGADDRUSE` - Address relationships
- `WH_ADDR` - Address details
- `WH_ALLROLES` - Ownership relationships

### Output Files
- `r360_portfolio_YYYYMMDD.csv` - Portfolio keys
- `r360_address_YYYYMMDD.csv` - Address keys  
- `r360_ownership_YYYYMMDD.csv` - Ownership keys
- SQLite databases: `current.db`, `address.db`, `ownership.db`

---

## Project Status Tracking

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
- [x] Environment-aware configuration system (dev/prod modes)
- [x] Testing framework integration with proper virtual environment handling
- [x] Unicode encoding fixes for Windows compatibility

### In Progress 🔄
- [ ] GUI or Excel-based exception management system
- [ ] Enhanced unit tests and edge case detection
- [ ] Documentation consolidation and executive reporting

### Future Enhancements 🔮
- [ ] Create GUI or Excel-based way to manage relationship exceptions
- [ ] Build out comprehensive unit tests and state-based assertions
- [ ] Historical trending and analytics capabilities
- [ ] API development for real-time lookups
- [ ] Direct integration with core banking system (COCC)

---

## Version History & Changelog

### v2.6.0-prod (2025-05-08) - Chad Doorley
- Added ownership_main and address_main scripts
- Separate databases for ownership.db and address.db with persistent keys
- Integration with cdutils for cross-project accessibility

### v2.5.0-prod (2025-05-08) - Chad Doorley  
- Stopped writing to historical.db (configurable)
- Pointed functions to shared cdutils instead of embedded src.cdutils
- Enabled cross-project functionality and centralized maintenance

### v2.4.0-prod (2024-03-12)
- Added SQLite database for improved I/O performance
- Maintained CSV output for backward compatibility
- SQLite provides easier interface for downstream consumption

### v2.3.0-prod (2024-02-27)
- Fixed mega household issue identified by Retail
- Improved handling of null CIFs in ownership roles
- Enhanced helper key grouping rules

### v2.2.0-prod (2024-02-02)
- Major code base cleanup and modularization
- Broke monolithic script into maintainable modules
- Improved readability and maintainability
- Implemented type hinting for static analysis
- No changes to grouping/business logic

### v2.0.9-prod (2024-12-27)
- Initial production version with change log implementation
- Baseline working version

---

## Technical Notes & Decisions

### 2025-07-25 - Testing Framework Integration
- Added virtual environment detection and UTF-8 encoding to resolve execution issues
- Testing framework now properly executes R360 through subprocess with correct Python environment
- Comprehensive logging added for debugging subprocess execution problems

### 2025-05-08 - Historical Database Strategy
- Historical database disabled due to size concerns and limited utilization
- No failed runs in over 2 months of daily execution
- Historical data strategy needs refinement:
  - Current approach creates large files with limited business value
  - Future approach should focus on tracking portfolio_key account counts over time
  - Useful for detecting early payoffs or non-standard contract behaviors
  - Priority should be current customer understanding before historical analytics

### Key Technical Decisions
- **Union-Find Algorithm:** Chosen for efficient handling of large datasets with complex relationship graphs
- **SQLite Storage:** Lightweight, reliable, and easily accessible across systems
- **Modular Architecture:** Enables maintenance and testing of individual components
- **Environment Safety:** Development mode prevents accidental production database modifications
- **cdutils Integration:** Centralized utility library enables cross-project functionality

---

## Operational Notes

### Daily Execution
- **Schedule:** Daily automated execution
- **Runtime:** Typically completes in under 5 minutes
- **Reliability:** 2+ months without failure
- **Monitoring:** Comprehensive logging to environment-specific log files

### Error Handling
- **Unicode Issues:** Resolved with PYTHONIOENCODING=utf-8
- **Virtual Environment:** Automatic detection and usage
- **Database Safety:** Dev mode prevents accidental production writes
- **Exception Logging:** Full error capture with truncated summaries

### Business Validation
- **Portfolio Key:** Successfully tested and validated by business stakeholders
- **Exception Handling:** Hard-coded exclusions for known problematic data
- **Key Persistence:** Stable keys across daily runs using historical data
- **Business Rule Compliance:** Handles complex banking relationship structures

---

## Questions & Future Considerations

### Immediate Priorities
1. **Exception Management:** Need user-friendly interface for managing grouping exceptions (currently hard-coded)
2. **Test Coverage:** Expand unit tests and edge case detection for production reliability
3. **Performance Monitoring:** Add metrics and alerting for daily execution monitoring

### Strategic Considerations
1. **Historical Analytics:** Develop business case for historical relationship tracking
2. **API Development:** Consider real-time lookup capabilities for other systems
3. **COCC Integration:** Plan migration from SQLite to core banking system storage
4. **Business Intelligence:** Direct integration with reporting and dashboard platforms

### Technical Debt
1. **Hard-coded Exclusions:** Move to configuration-driven exception management
2. **Type Hinting:** Complete type hinting implementation across all modules
3. **Documentation:** Maintain technical documentation as system evolves
4. **Testing Strategy:** Develop comprehensive test suite for production confidence

---

## Archived Documentation from r360_doc.md

### Historical Notes & Decisions

#### 2025-05-08 (Chad Doorley)
- Tweaking this a bit. The historical database takes up a lot of space and is not being utilized at all. I made some adjustments (eliminating static dependencies and configuring it to use cdutils)
- Historical db can be turned back on
- This is really working great though, this hasn't had a failed run in over 2 months and it runs daily.
- Thinking about the approach to using the historical:
  - there must be a more efficient and better way to store this. I can't write out to historical.db every day, otherwise this balloons in size and I also haven't had a single use for it yet
  - I'm thinking the use would be to look at a particular portfolio_key and track # of accounts. This is noisy though, as CDs could just pay off or loans close and they are still customers, but they just reached maturity.
    - Maybe tracking things like they pay off early or do things outside of the normal timing set on contract.
    - I think this is something to explore down the line. It makes sense to first understand our customers at this point in time, segment into different categories, build reports/dashboards/applications around this to help us know our customers. Other items can be tackled in later phases.

### Additional Technical Context
- **Original Brief Description:** The goal is to create a centralized key to better understand the Bank's customers. This involves the creation of the portfolio_key, which is a superhousehold. This groups on ownership similarities or shared address.
- **Core Objectives:** The development of a robust data pipeline to accurately group customers and generate a key for each acctnbr that is consistent over time
- **Database Strategy:** Store this in a database (COCC is the goal, it is stored in a lightweight relational database for now (sqlite))

---

*This document serves as the central repository for all R360 project information, technical decisions, and ongoing development notes. It should be updated as the project evolves and new decisions are made.*


----
Project Technical Documentation: R360
===

## Usage
1. Navigate to the Project Home directory
```bash
cd Production
python -m src.main
```

Cadence of Execution:
Daily

## Filters & Calculations

## Changelog
[v2.4.0-prod] 2024-03-12
- Added a sqlite database to improve I/O
    - did not remove existing csv extract as output, but going forward, using SQLite is easier interface to pull from

[v2.3.0-prod] 2024-02-27
- Retail identified a mega household and helper key grouping rules were adjusted to resolve issue
    - this included the handling of null CIFs in the ownership roles/helper key component
- minor tweaks/improvements

[2.2.0-prod] 2024-02-02
- Code base has been cleaned up
- Rather than one big script, it is broken up into modular parts that are easy to maintain
- More readable
- No grouping/business logic modifications
- Implemented type hinting for static analysis in the future
    - not consistent throughout yet

[v2.0.9-prod] 2024-12-27
- I have recently started implementing a change log for every time I modify the code base
- This is the existing working version


---
2025-07-24 (Chad Doorley)
Will clean up documentation