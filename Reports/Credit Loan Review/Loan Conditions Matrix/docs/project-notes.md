# Loan Conditions Matrix - Project Development Notes

## Development History & Running Notes

### 2025-02-11 - Project Initiation Meeting
- **Stakeholders**: Eldora & Paul Kocak
- **Decision**: Web-based approach instead of Excel due to complex conditional logic needs
- **Tech Stack Decided**: Vanilla HTML/CSS/JS for maximum compatibility
- **Deployment Strategy**: Browser-based, shared location or bookmark access
- **Modular Approach**: Sections split by complexity (Appraisal → Environmental → Financial Statements)

### 2025-02-25 [v1.0.0-dev] - First Working Demo  
- **Milestone**: Completed initial demo version
- **Sections Implemented**: 3 core sections (Appraisal, Environmental, Financial Statements)
- **File**: `condition_matrix.html` 
- **Feedback**: From Paul & Eldora based on Excel form requirements
- **Status**: Demo ready for stakeholder review

### 2025-05-22 - Conditional Logic Implementation
- **Feature**: Advanced conditional question branching
- **CRE Secured Loan Logic**:
  - "Is this a CRE Secured loan, other than 1-4 family residential property or real estate taken as abundance of caution?"
  - 6 checkbox options with follow-up questions
  - "Is further action required?" with open-ended detail box
- **Status**: Base conditional framework completed

### 2025-05-24 - Survey Output Refinement  
- **Milestone**: Example output generation and formatting improvements
- **Requirements Summary Format**:
  ```
  Appraisal
  ─────────
  • An appraisal is required and should not be dated more than 12 months prior to loan closing
  • Secured property is subject to a bank ordered appraisal showing maximum LTV not to exceed XX%
  
  Environmental  
  ─────────────
  • A Phase 1 assessment is required
  
  Flood
  ─────
  • Customer was informed 10 days prior to closing
  • Flood insurance been reviewed by compliance  
  • Sufficient flood insurance has been obtained
  ```

### 2025-08-05 - Project Restructure & Documentation Update
- **Action**: Moved project from `Reports/Loan Conditions Matrix/` to `Reports/Credit Loan Review/Loan Conditions Matrix/`
- **Reason**: Better organization within Credit Loan Review department structure
- **Updated**: Documentation structure, README.md enhanced with historical context
- **Status**: Documentation consolidated from old project versions

---

## Technical Implementation Notes

### Architecture Decisions
- **Modular Design**: Separate modules for questionnaire logic and policy mapping
- **JSON Configuration**: Easy policy updates without code changes  
- **No External Dependencies**: Ensures compatibility across environments
- **Static Deployment**: Can be hosted anywhere or run locally

### Key Implementation Details

#### Survey Configuration Structure
```javascript
{
  "sections": [
    {
      "title": "Section Name",
      "questions": [
        {
          "id": "q1", 
          "text": "Question text",
          "type": "radio|checkbox|text",
          "options": [...],
          "children": [...]  // Conditional questions
        }
      ]
    }
  ]
}
```

#### Conditional Logic Patterns
1. **Simple Branching**: Yes/No → Show/Hide next question
2. **Multi-Option Branching**: Checkbox selection → Multiple conditional paths  
3. **Risk-Based Logic**: Low/Medium/High risk → Different requirement sets
4. **Loan Type Logic**: Different paths for RE secured vs. unsecured loans

### Current Policy Mappings

#### Appraisal Section
- **Trigger**: Real estate secured loans
- **Requirements**: 
  - 12-month appraisal age limit
  - LTV calculations (lesser of purchase price or appraised value)
  - Policy exception handling for older appraisals

#### Environmental Section  
- **Trigger**: CRE loans (with abundance of caution consideration)
- **Low Risk Path**: Simplified requirements
- **Standard Path**: Phase 1 assessment required
- **Risk Categories**: 6 checkbox options with follow-up details

#### Flood Section
- **Decision Tree**:
  ```
  Real Estate Secured? → Yes
    ├── Flood Certificate Generated? → Yes  
    │   └── Property in Flood Zone (AE/V)? → Yes
    │       └── Require: Customer notification, Compliance review, Insurance
    └── SBA Guaranteed with Building Contents? → Yes
        └── [Same flood zone logic]
  ```

#### Financial Statements Section
- **Corporate Guarantors**: FYE statements within 120 days, Interims if required
- **Loan Type Specific**: Different requirements for special loans
- **Supporting Documents**: Projections, additional statements as needed

#### SWAP Section
- **Trigger**: SWAP loan identification
- **Requirements**: Checklist completion, Pre-closing documentation
- **Validation**: All documents received before proceeding

---

## Known Issues & Improvements Needed

### Formatting Issues
- ✅ **Fixed**: Bullet point alignment (was centered, now left-aligned)
- ✅ **Fixed**: Typo correction ("abundance of caution")  
- ⏳ **Pending**: Environmental low-risk category early termination
- ⏳ **Pending**: Flood section question flow refinement

### User Experience Enhancements
- **Progress Indicators**: More granular progress tracking
- **Save/Resume**: Session persistence across browser sessions
- **Validation Messaging**: Clearer error messages for incomplete sections
- **Mobile Optimization**: Touch-friendly interface improvements

### Policy Integration 
- **Data Sources**: Integration with loan policy documentation system
- **Version Control**: Policy change tracking and historical versions
- **Approval Workflow**: SME review process for policy updates
- **Audit Trail**: User interaction logging for compliance

---

## Stakeholder Feedback & Requests

### From Eldora & Paul (Latest)
1. **Environmental Section**: Simplify low-risk category path
2. **Flood Logic**: Refine Yes→Yes→Yes decision tree  
3. **Output Format**: Improve bullet point formatting and alignment
4. **Corporate Guarantor**: Add child questions for detailed requirements
5. **Conditional Skipping**: Skip flood/environmental for non-RE secured loans

### Implementation Priority
1. **High**: Fix conditional logic flow issues
2. **High**: Improve output formatting consistency  
3. **Medium**: Add missing child question branches
4. **Medium**: Enhance validation and error handling
5. **Low**: Visual design improvements

---

## Deployment & Usage Notes

### Current Access Methods
- **Local**: Open `survey.html` in web browser
- **Shared**: Place HTML file in shared network location
- **Bookmark**: Users bookmark file location for easy access
- **Internal Server**: Future hosting on internal web server

### User Training Requirements
- **Admin Users**: Survey configuration and policy updates
- **End Users**: Basic navigation and survey completion
- **SMEs**: Policy review and validation processes

### Performance Considerations
- **Load Time**: JSON configuration size impact
- **Browser Compatibility**: Testing across IE, Chrome, Firefox, Safari
- **Mobile Performance**: Touch interface responsiveness
- **Offline Capability**: Local storage for completed surveys

---

## Future Roadmap

### Phase 2 Enhancements
- **User Authentication**: Role-based access control
- **Analytics Dashboard**: Usage statistics and completion rates
- **Integration APIs**: Connect with loan origination systems  
- **Document Generation**: Auto-populate loan condition templates
- **Workflow Integration**: Direct export to loan processing systems

### Phase 3 Vision
- **AI Enhancement**: Natural language policy interpretation
- **Regulatory Updates**: Automated compliance requirement updates
- **Multi-Bank Support**: Configurable for different institution policies
- **Advanced Reporting**: Trend analysis and policy gap identification

---

## Contact & Support

- **Technical Lead**: Business Intelligence Team
- **Subject Matter Experts**: Eldora, Paul Kocak  
- **Development Questions**: BI Team via internal channels
- **Policy Questions**: Credit Risk Management team
- **User Support**: Commercial Banking operations

---

*Last Updated: August 5, 2025*
*Next Review: Pending stakeholder feedback on current implementation*

# 2025-08-05
Making fixes based on feedback:

An appraisal is optional - Secured property is subject to a MAI bank ordered appraisal showing an 'as is' value and 'as stablilized' value with a maximum loan to value to exceed XX%.


For an obligation secured by CRE <$500M or a residential loan <$400M, a recent (under 12 months) tax assessed value with a bank site visit showing a maximum loan to value not to exceed 70%.