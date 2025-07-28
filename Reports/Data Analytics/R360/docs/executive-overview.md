# R360 Customer Relationship Keys - Executive Overview

## What is R360?

The R360 (Relationship 360) system provides BCSB with a **360-degree view of customer relationships** across all business lines. It creates standardized customer relationship keys that enable the bank to understand how customers are connected through addresses, ownership structures, and financial relationships.

## Business Problem Solved

**Challenge:** BCSB's customers often have multiple accounts across different business lines (retail, commercial), but there was no systematic way to understand these relationships. This made it difficult to:
- Identify total customer exposure for risk management
- Provide coordinated customer service across departments  
- Understand household relationships for marketing and analytics
- Analyze business relationship concentrations for regulatory reporting

**Solution:** R360 creates three types of relationship keys that automatically group customer accounts based on different business criteria, providing a unified customer view across the entire organization.

## How R360 Works

### 1. Data Sources
- **Account Data:** All customer accounts from OSIBANK.WH_ACCTCOMMON
- **Address Data:** Physical addresses from WH_ADDR, PERSADDRUSE, ORGADDRUSE
- **Ownership Data:** Legal ownership relationships from WH_ALLROLES

### 2. Key Generation Process

The system uses an implementation of the **Union-Find algorithm** to efficiently group customer accounts into relationship clusters. All customers are modeled as nodes in a graph. This approach ensures that if Account A is related to Account B, and Account B is related to Account C, then all three accounts automatically belong to the same relationship group.

### 3. Three Key Types for Different Business Needs

#### **Portfolio Key** (The Super Household)
- **Purpose:** Complete 360-degree customer view
- **Grouping Logic:** Accounts connected by address OR ownership
- **Business Use:** Total customer exposure, coordinated relationship management
- **Example:** John Smith's personal checking account groups with his business loan because he's an owner of the business

#### **Address Key** (Household Analysis) 
- **Purpose:** Household and family relationship analysis
- **Grouping Logic:** Accounts connected by shared addresses only
- **Business Use:** Retail banking, household income analysis, marketing campaigns
- **Example:** All accounts for family members living at the same address are grouped together

#### **Ownership Key** (Business Relationships)
- **Purpose:** Commercial relationship and concentration analysis
- **Grouping Logic:** Accounts connected by shared ownership only
- **Business Use:** Commercial lending, regulatory concentration reporting
- **Example:** All businesses owned by the same person or entity are grouped together

### 4. Smart Business Rules

The system includes sophisticated logic to handle real-world banking complexities:

- **IOLTA Exclusions:** Legal trust accounts (IOLTA) are automatically excluded from grouping to prevent artificial mega-households
- **Problematic Addresses:** Shared business addresses (like "29 Broadway") that shouldn't group unrelated customers are excluded
- **Historical Persistence:** Keys remain stable over time - once assigned, a customer keeps the same relationship key even as their account portfolio changes

## Technical Architecture

### Daily Processing Pipeline
1. **Data Extraction:** Pulls fresh data from OSIBANK data warehouse
2. **Data Cleaning:** Applies business rules and creates hash keys for addresses/ownership
3. **Relationship Grouping:** Uses Union-Find algorithm to identify connected accounts  
4. **Key Assignment:** Assigns persistent keys using historical data for consistency
5. **Database Storage:** Stores results in SQLite databases (current.db, address.db, ownership.db)
6. **Integration:** Makes keys available to other systems via cdutils library

### Operational Excellence
- **Daily Execution:** Fully automated daily refresh ensures data is always current
- **Environment Safety:** Development mode prevents accidental database changes during testing
- **Error Handling:** Comprehensive logging and monitoring for operational reliability
- **Scalability:** Efficiently processes millions of accounts in minutes

## Business Impact

### For Risk Management
- **Concentration Monitoring:** Identify total exposure to related entities
- **Regulatory Compliance:** Automated concentration of credit reporting
- **Portfolio Analysis:** Understand customer relationship risks

### For Customer Experience  
- **Coordinated Service:** All departments see complete customer relationships
- **Cross-Selling Opportunities:** Identify accounts that could benefit from additional services
- **Relationship Banking:** Provide white-glove service to high-value relationship clusters

### For Analytics & Marketing
- **Customer Segmentation:** Group households and businesses for targeted campaigns
- **Profitability Analysis:** Calculate true relationship profitability across all accounts
- **Business Intelligence:** Power dashboards and reports across all business lines

## Current Status

- **Production Ready:** Daily automated execution for 2+ months without failure
- **Integration Complete:** Available via cdutils library for use across all systems
- **Proven Results:** Successfully identified and resolved complex relationship grouping challenges
- **Business Adoption:** Actively used by Commercial, Retail, and Data Analytics teams

## Future Enhancements

- **Exception Management GUI:** User-friendly interface for managing grouping exceptions
- **Advanced Analytics:** Historical trending and relationship change detection
- **API Development:** RESTful API for real-time relationship lookups
- **Business Intelligence Integration:** Direct integration with reporting platforms

---

*R360 represents a foundational investment in customer data architecture that enables BCSB to operate as a truly relationship-focused bank, with comprehensive customer insights driving better business decisions across all departments.*
