/**
 * Loan Conditions Matrix Configuration
 * 
 * This file contains all configuration settings for the application.
 * Modify these settings based on your environment (development/production).
 */

const CONFIG = {
    // Application Info
    APP_NAME: "Loan Conditions Matrix",
    VERSION: "1.0.0",
    BUSINESS_LINE: "Commercial Banking",
    OWNER: "Business Intelligence Team",
    
    // Environment Settings
    ENVIRONMENT: "development", // "development" or "production"
    DEBUG: true,
    
    // Application Settings
    MAX_QUESTIONS: 20,
    SESSION_TIMEOUT: 30, // minutes
    AUTO_SAVE: true,
    
    // UI Settings
    ANIMATION_SPEED: 300, // milliseconds
    PROGRESS_UPDATE_DELAY: 100,
    
    // Policy Data Sources
    POLICY_DATA_URL: "assets/data/loan-policies.json",
    REQUIREMENTS_DATA_URL: "assets/data/requirements.json",
    
    // Export Settings
    PDF_EXPORT: {
        enabled: true,
        company_logo: "assets/images/bcsb-logo.png",
        footer_text: "BCSB Commercial Lending - Confidential"
    },
    
    // Logging
    LOG_LEVEL: "info", // "debug", "info", "warn", "error"
    CONSOLE_LOGGING: true,
    
    // Features Flags
    FEATURES: {
        advancedFiltering: true,
        exportToPDF: true,
        saveSession: false,
        analyticsTracking: false
    },
    
    // Question Categories
    QUESTION_CATEGORIES: {
        LOAN_TYPE: "loan_type",
        BORROWER_INFO: "borrower_info",
        COLLATERAL: "collateral",
        FINANCIAL_INFO: "financial_info",
        RISK_FACTORS: "risk_factors"
    },
    
    // Loan Types
    LOAN_TYPES: {
        TERM_LOAN: "term_loan",
        LINE_OF_CREDIT: "line_of_credit",
        EQUIPMENT_FINANCING: "equipment_financing",
        REAL_ESTATE: "real_estate",
        SBA_LOAN: "sba_loan",
        CONSTRUCTION: "construction"
    },
    
    // Default Values
    DEFAULTS: {
        currency: "USD",
        dateFormat: "MM/DD/YYYY",
        numberFormat: "en-US"
    }
};

// Environment-specific overrides
if (CONFIG.ENVIRONMENT === "production") {
    CONFIG.DEBUG = false;
    CONFIG.CONSOLE_LOGGING = false;
    CONFIG.LOG_LEVEL = "error";
}

// Make config globally available
window.APP_CONFIG = CONFIG;
