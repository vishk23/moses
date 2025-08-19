Delinquency Report
===

Meta Information
---
Developed by CD
v1.8
Month End Data

Directory:
\\10.161.85.66\Home\Share\Data & Analytics Initiatives\Project Management\Chad Projects\Resolution Committee Automation\Delinquency

Overview:
- This report automates a 30 minute task in Loan Review
- This is attached to loan review's monthly resolution package

Milestones
--- 

### IN-PROGRESS

### TO-DO

### DONE
- Refactor source code into a module
- Code in Alteryx
- Code Report in python
- Add email distribution
- Handle total amount due definition
- Fix NDPD to calculate off the end of the month
- Remove ACH Manager products

### 2025-04-24 (Chad Doorley)
- Refactored this a bit. Taking inventory for PTO. This documentation will get a revamp.

### 2025-01-25
- Haven't had the time to get to refactoring this, but it's on my list. This is running in production and works fine, but just needs a couple small tweaks

### 2025-02-06 [v2.0.0-prod]
- Just beware this is a bit brittle in the sense that as people add new products into the mix, we have to continuosly update this because it is all coded into sections by product.
- Need to get clarification on the Reduced to $0 section.