/**
 * Policy Mapping Module
 * 
 * Handles the business rules engine, policy lookup, and requirements generation
 * for the Loan Conditions Matrix application.
 */

class PolicyMapper {
    constructor() {
        this.policyRules = {};
        this.requirementTemplates = {};
        this.isInitialized = false;
        
        this.initializePolicyData();
    }

    /**
     * Initialize policy data and rules
     */
    async initializePolicyData() {
        try {
            // Load static policy rules for development
            // TODO: Replace with dynamic loading from external data source
            this.policyRules = this.getStaticPolicyRules();
            this.requirementTemplates = this.getStaticRequirementTemplates();
            
            this.isInitialized = true;
            this.log('Policy data initialized successfully', 'info');
        } catch (error) {
            this.log('Error initializing policy data: ' + error.message, 'error');
        }
    }

    /**
     * Get static policy rules for development
     * TODO: Replace with dynamic loading from policy database
     */
    getStaticPolicyRules() {
        return {
            // Loan Type Rules
            loan_type_rules: {
                term_loan: {
                    base_requirements: ['financial_statements', 'business_plan', 'personal_guarantee'],
                    min_amount: 10000,
                    max_amount: 10000000,
                    collateral_requirements: ['primary_collateral']
                },
                line_of_credit: {
                    base_requirements: ['financial_statements', 'cash_flow_analysis', 'personal_guarantee'],
                    min_amount: 25000,
                    max_amount: 5000000,
                    collateral_requirements: ['accounts_receivable', 'inventory']
                },
                equipment_financing: {
                    base_requirements: ['equipment_appraisal', 'vendor_invoice', 'insurance_coverage'],
                    min_amount: 15000,
                    max_amount: 2000000,
                    collateral_requirements: ['equipment_security']
                },
                real_estate: {
                    base_requirements: ['appraisal', 'environmental_report', 'title_insurance'],
                    min_amount: 100000,
                    max_amount: 25000000,
                    collateral_requirements: ['real_estate_mortgage']
                },
                sba_loan: {
                    base_requirements: ['sba_forms', 'financial_statements', 'business_plan', 'personal_history'],
                    min_amount: 50000,
                    max_amount: 5000000,
                    collateral_requirements: ['sba_collateral_requirements']
                },
                construction: {
                    base_requirements: ['construction_plans', 'contractor_information', 'cost_breakdown'],
                    min_amount: 250000,
                    max_amount: 15000000,
                    collateral_requirements: ['construction_mortgage', 'completion_bond']
                }
            },

            // Amount-based Rules
            amount_thresholds: {
                under_100k: {
                    additional_requirements: []
                },
                between_100k_500k: {
                    additional_requirements: ['management_interview', 'credit_bureau_reports']
                },
                between_500k_1m: {
                    additional_requirements: ['board_resolution', 'annual_cpa_statements']
                },
                over_1m: {
                    additional_requirements: ['board_resolution', 'audited_financials', 'loan_committee_approval']
                },
                over_5m: {
                    additional_requirements: ['board_resolution', 'audited_financials', 'loan_committee_approval', 'regulatory_review']
                }
            },

            // Industry-specific Rules
            industry_rules: {
                manufacturing: {
                    additional_requirements: ['inventory_reports', 'accounts_receivable_aging']
                },
                retail: {
                    additional_requirements: ['sales_reports', 'lease_agreements']
                },
                healthcare: {
                    additional_requirements: ['licensing_verification', 'regulatory_compliance']
                },
                real_estate: {
                    additional_requirements: ['rent_rolls', 'property_management_agreements']
                },
                construction: {
                    additional_requirements: ['contractor_license', 'bonding_capacity', 'job_completion_history']
                },
                agriculture: {
                    additional_requirements: ['crop_insurance', 'usda_compliance', 'seasonal_cash_flow']
                }
            },

            // Collateral Rules
            collateral_rules: {
                real_estate: {
                    requirements: ['appraisal', 'title_search', 'property_insurance', 'environmental_assessment']
                },
                equipment: {
                    requirements: ['equipment_appraisal', 'ucc_filing', 'equipment_insurance']
                },
                inventory: {
                    requirements: ['inventory_reports', 'ucc_filing', 'warehouse_receipts']
                },
                accounts_receivable: {
                    requirements: ['ar_aging', 'customer_concentration_analysis', 'ucc_filing']
                },
                personal_guarantee: {
                    requirements: ['personal_financial_statement', 'personal_credit_report', 'guarantee_agreement']
                },
                cash_deposit: {
                    requirements: ['deposit_agreement', 'pledge_documentation']
                },
                unsecured: {
                    requirements: ['strong_cash_flow', 'excellent_credit_history', 'board_resolution']
                }
            },

            // Borrower Type Rules
            borrower_type_rules: {
                corporation: {
                    additional_requirements: ['articles_of_incorporation', 'bylaws', 'board_resolutions']
                },
                llc: {
                    additional_requirements: ['operating_agreement', 'member_resolutions']
                },
                partnership: {
                    additional_requirements: ['partnership_agreement', 'partner_personal_guarantees']
                },
                sole_proprietorship: {
                    additional_requirements: ['business_license', 'personal_tax_returns']
                },
                non_profit: {
                    additional_requirements: ['501c3_determination', 'board_minutes', 'donor_information']
                }
            }
        };
    }

    /**
     * Get static requirement templates
     */
    getStaticRequirementTemplates() {
        return {
            // Financial Documents
            financial_statements: "Current financial statements (balance sheet, income statement, cash flow) for the last 3 years",
            audited_financials: "Audited financial statements for the last 3 years",
            annual_cpa_statements: "CPA-prepared annual financial statements for the last 3 years",
            personal_financial_statement: "Personal financial statement for all guarantors",
            business_plan: "Comprehensive business plan including market analysis and financial projections",
            cash_flow_analysis: "12-month cash flow projection with supporting assumptions",
            
            // Legal Documents
            board_resolution: "Board resolution authorizing the loan and designating signing authority",
            articles_of_incorporation: "Certified copy of articles of incorporation",
            bylaws: "Current corporate bylaws",
            operating_agreement: "LLC operating agreement",
            partnership_agreement: "Partnership agreement",
            business_license: "Current business license and permits",
            
            // Collateral Documents
            appraisal: "Current appraisal by certified appraiser (within 12 months)",
            equipment_appraisal: "Equipment appraisal by certified equipment appraiser",
            title_search: "Title search and title insurance policy",
            title_insurance: "Title insurance policy",
            environmental_report: "Phase I environmental assessment",
            environmental_assessment: "Environmental assessment appropriate to property type",
            
            // Insurance
            property_insurance: "Property insurance with bank named as loss payee",
            equipment_insurance: "Equipment insurance with bank named as loss payee",
            insurance_coverage: "Comprehensive insurance coverage appropriate to collateral type",
            
            // Credit and Background
            personal_credit_report: "Personal credit reports for all guarantors",
            credit_bureau_reports: "Business and personal credit bureau reports",
            personal_history: "Personal history statements for all owners (SBA Form 912)",
            
            // Industry-Specific
            inventory_reports: "Current inventory reports and aging analysis",
            accounts_receivable_aging: "Accounts receivable aging report",
            ar_aging: "Current accounts receivable aging report",
            sales_reports: "Monthly sales reports for the last 12 months",
            rent_rolls: "Current rent rolls for income-producing properties",
            
            // Legal Filings
            ucc_filing: "UCC-1 financing statement filing",
            guarantee_agreement: "Personal guarantee agreement",
            deposit_agreement: "Deposit account pledge agreement",
            
            // Approvals and Reviews
            management_interview: "Management interview and site visit",
            loan_committee_approval: "Senior loan committee approval required",
            regulatory_review: "Regulatory review and approval process",
            
            // SBA-Specific
            sba_forms: "Completed SBA loan application forms (Form 1919, 912, 413)",
            
            // Construction-Specific
            construction_plans: "Detailed construction plans and specifications",
            contractor_information: "General contractor information and references",
            cost_breakdown: "Detailed cost breakdown and construction budget",
            construction_mortgage: "Construction mortgage documentation",
            completion_bond: "Completion and performance bond",
            contractor_license: "Contractor license and bonding information",
            bonding_capacity: "Contractor bonding capacity documentation",
            job_completion_history: "Contractor job completion history and references",
            
            // Specialized Requirements
            vendor_invoice: "Vendor invoice or purchase agreement for equipment",
            warehouse_receipts: "Warehouse receipts for inventory collateral",
            customer_concentration_analysis: "Customer concentration analysis for accounts receivable",
            licensing_verification: "Professional licensing verification",
            regulatory_compliance: "Industry regulatory compliance documentation",
            lease_agreements: "Current lease agreements for business premises",
            property_management_agreements: "Property management agreements (if applicable)",
            crop_insurance: "Crop insurance documentation",
            usda_compliance: "USDA compliance and certification",
            seasonal_cash_flow: "Seasonal cash flow analysis",
            strong_cash_flow: "Demonstration of strong, consistent cash flow",
            excellent_credit_history: "Excellent credit history documentation",
            donor_information: "Major donor information and funding sources"
        };
    }

    /**
     * Generate requirements based on loan answers
     */
    generateRequirements(answers) {
        if (!this.isInitialized) {
            this.log('Policy mapper not initialized', 'error');
            return [];
        }

        let requirements = new Set(); // Use Set to avoid duplicates

        try {
            // Add base requirements based on loan type
            this.addLoanTypeRequirements(answers, requirements);
            
            // Add amount-based requirements
            this.addAmountBasedRequirements(answers, requirements);
            
            // Add industry-specific requirements
            this.addIndustryRequirements(answers, requirements);
            
            // Add borrower type requirements
            this.addBorrowerTypeRequirements(answers, requirements);
            
            // Add collateral requirements
            this.addCollateralRequirements(answers, requirements);

            const finalRequirements = Array.from(requirements).map(req => 
                this.requirementTemplates[req] || req
            );

            this.log(`Generated ${finalRequirements.length} requirements`, 'info');
            return finalRequirements.sort();

        } catch (error) {
            this.log('Error generating requirements: ' + error.message, 'error');
            return [];
        }
    }

    /**
     * Add loan type specific requirements
     */
    addLoanTypeRequirements(answers, requirements) {
        const loanType = answers.loan_type;
        if (!loanType) return;

        const loanTypeRule = this.policyRules.loan_type_rules[loanType];
        if (loanTypeRule && loanTypeRule.base_requirements) {
            loanTypeRule.base_requirements.forEach(req => requirements.add(req));
        }
    }

    /**
     * Add amount-based requirements
     */
    addAmountBasedRequirements(answers, requirements) {
        const amount = parseFloat(answers.loan_amount) || 0;
        
        let amountRule;
        if (amount >= 5000000) {
            amountRule = this.policyRules.amount_thresholds.over_5m;
        } else if (amount >= 1000000) {
            amountRule = this.policyRules.amount_thresholds.over_1m;
        } else if (amount >= 500000) {
            amountRule = this.policyRules.amount_thresholds.between_500k_1m;
        } else if (amount >= 100000) {
            amountRule = this.policyRules.amount_thresholds.between_100k_500k;
        } else {
            amountRule = this.policyRules.amount_thresholds.under_100k;
        }

        if (amountRule && amountRule.additional_requirements) {
            amountRule.additional_requirements.forEach(req => requirements.add(req));
        }
    }

    /**
     * Add industry-specific requirements
     */
    addIndustryRequirements(answers, requirements) {
        const industry = answers.industry_type;
        if (!industry) return;

        const industryRule = this.policyRules.industry_rules[industry];
        if (industryRule && industryRule.additional_requirements) {
            industryRule.additional_requirements.forEach(req => requirements.add(req));
        }
    }

    /**
     * Add borrower type requirements
     */
    addBorrowerTypeRequirements(answers, requirements) {
        const borrowerType = answers.borrower_type;
        if (!borrowerType) return;

        const borrowerRule = this.policyRules.borrower_type_rules[borrowerType];
        if (borrowerRule && borrowerRule.additional_requirements) {
            borrowerRule.additional_requirements.forEach(req => requirements.add(req));
        }
    }

    /**
     * Add collateral-specific requirements
     */
    addCollateralRequirements(answers, requirements) {
        const collateralTypes = answers.collateral_type;
        if (!collateralTypes || !Array.isArray(collateralTypes)) return;

        collateralTypes.forEach(collateralType => {
            const collateralRule = this.policyRules.collateral_rules[collateralType];
            if (collateralRule && collateralRule.requirements) {
                collateralRule.requirements.forEach(req => requirements.add(req));
            }
        });
    }

    /**
     * Validate loan parameters against policy rules
     */
    validateLoanParameters(answers) {
        const validationResults = {
            isValid: true,
            errors: [],
            warnings: []
        };

        // Validate loan amount against loan type limits
        this.validateAmountLimits(answers, validationResults);
        
        // Validate collateral requirements
        this.validateCollateralRequirements(answers, validationResults);

        return validationResults;
    }

    /**
     * Validate loan amount against type-specific limits
     */
    validateAmountLimits(answers, validationResults) {
        const loanType = answers.loan_type;
        const amount = parseFloat(answers.loan_amount) || 0;

        if (!loanType || amount <= 0) return;

        const loanTypeRule = this.policyRules.loan_type_rules[loanType];
        if (loanTypeRule) {
            if (amount < loanTypeRule.min_amount) {
                validationResults.errors.push(
                    `Loan amount ($${amount.toLocaleString()}) is below minimum for ${loanType} ($${loanTypeRule.min_amount.toLocaleString()})`
                );
                validationResults.isValid = false;
            }
            
            if (amount > loanTypeRule.max_amount) {
                validationResults.errors.push(
                    `Loan amount ($${amount.toLocaleString()}) exceeds maximum for ${loanType} ($${loanTypeRule.max_amount.toLocaleString()})`
                );
                validationResults.isValid = false;
            }
        }
    }

    /**
     * Validate collateral requirements
     */
    validateCollateralRequirements(answers, validationResults) {
        const loanType = answers.loan_type;
        const collateralTypes = answers.collateral_type;

        if (!loanType || !collateralTypes) return;

        const loanTypeRule = this.policyRules.loan_type_rules[loanType];
        if (loanTypeRule && loanTypeRule.collateral_requirements) {
            // Check if unsecured loan meets criteria
            if (collateralTypes.includes('unsecured')) {
                const amount = parseFloat(answers.loan_amount) || 0;
                if (amount > 250000) {
                    validationResults.warnings.push(
                        'Unsecured loans over $250,000 require exceptional credit profile and cash flow'
                    );
                }
            }
        }
    }

    /**
     * Get policy summary for display
     */
    getPolicySummary(answers) {
        const validation = this.validateLoanParameters(answers);
        const requirements = this.generateRequirements(answers);

        return {
            validation: validation,
            requirementCount: requirements.length,
            estimatedProcessingTime: this.estimateProcessingTime(answers, requirements),
            riskLevel: this.assessRiskLevel(answers)
        };
    }

    /**
     * Estimate processing time based on loan complexity
     */
    estimateProcessingTime(answers, requirements) {
        const baseTime = 5; // 5 business days base
        const amount = parseFloat(answers.loan_amount) || 0;
        
        let additionalTime = 0;
        
        // Add time based on amount
        if (amount > 1000000) additionalTime += 10;
        else if (amount > 500000) additionalTime += 5;
        
        // Add time based on requirements complexity
        if (requirements.length > 15) additionalTime += 5;
        else if (requirements.length > 10) additionalTime += 3;
        
        // Add time for specific loan types
        if (answers.loan_type === 'construction') additionalTime += 10;
        if (answers.loan_type === 'sba_loan') additionalTime += 15;
        
        return `${baseTime + additionalTime} business days`;
    }

    /**
     * Assess risk level based on loan characteristics
     */
    assessRiskLevel(answers) {
        let riskScore = 0;
        
        const amount = parseFloat(answers.loan_amount) || 0;
        if (amount > 5000000) riskScore += 3;
        else if (amount > 1000000) riskScore += 2;
        else if (amount > 500000) riskScore += 1;
        
        if (answers.collateral_type && answers.collateral_type.includes('unsecured')) {
            riskScore += 2;
        }
        
        if (answers.loan_type === 'construction') riskScore += 2;
        if (answers.loan_type === 'line_of_credit') riskScore += 1;
        
        if (riskScore >= 5) return 'High';
        if (riskScore >= 3) return 'Medium';
        return 'Low';
    }

    /**
     * Logging utility
     */
    log(message, level = 'info') {
        if (APP_CONFIG.CONSOLE_LOGGING && APP_CONFIG.DEBUG) {
            console[level](`[PolicyMapper] ${message}`);
        }
    }
}

// Initialize policy mapper
window.policyMapper = new PolicyMapper();
