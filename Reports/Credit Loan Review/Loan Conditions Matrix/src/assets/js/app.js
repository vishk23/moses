/**
 * Main Application Controller
 * 
 * Coordinates between the questionnaire and policy mapping modules
 * and handles application-wide functionality.
 */

class LoanConditionsApp {
    constructor() {
        this.isInitialized = false;
        this.currentSession = null;
        
        this.initialize();
    }

    /**
     * Initialize the application
     */
    async initialize() {
        try {
            this.log('Initializing Loan Conditions Matrix application', 'info');
            
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.finishInitialization());
            } else {
                this.finishInitialization();
            }
            
        } catch (error) {
            this.log('Error initializing application: ' + error.message, 'error');
        }
    }

    /**
     * Complete initialization after DOM is ready
     */
    async finishInitialization() {
        try {
            // Set up print functionality
            this.setupPrintHandlers();
            
            // Set up export functionality
            this.setupExportHandlers();
            
            // Initialize session management
            this.initializeSession();
            
            this.isInitialized = true;
            this.log('Application initialized successfully', 'info');
            
        } catch (error) {
            this.log('Error finishing initialization: ' + error.message, 'error');
        }
    }

    /**
     * Set up print functionality
     */
    setupPrintHandlers() {
        const printBtn = document.getElementById('print-results');
        if (printBtn) {
            printBtn.addEventListener('click', () => this.printResults());
        }
    }

    /**
     * Set up export functionality
     */
    setupExportHandlers() {
        const exportBtn = document.getElementById('export-results');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportToPDF());
        }
    }

    /**
     * Initialize session management
     */
    initializeSession() {
        this.currentSession = {
            sessionId: this.generateSessionId(),
            startTime: new Date(),
            answers: {},
            requirements: [],
            lastActivity: new Date()
        };

        // Set up session timeout if enabled
        if (APP_CONFIG.SESSION_TIMEOUT > 0) {
            this.setupSessionTimeout();
        }

        this.log(`Session initialized: ${this.currentSession.sessionId}`, 'debug');
    }

    /**
     * Generate a unique session ID
     */
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Set up session timeout handling
     */
    setupSessionTimeout() {
        const timeoutMinutes = APP_CONFIG.SESSION_TIMEOUT;
        const timeoutMs = timeoutMinutes * 60 * 1000;

        this.sessionTimer = setTimeout(() => {
            this.handleSessionTimeout();
        }, timeoutMs);

        // Reset timer on user activity
        this.setupActivityTracking();
    }

    /**
     * Set up activity tracking to reset session timer
     */
    setupActivityTracking() {
        const activityEvents = ['click', 'keypress', 'change', 'input'];
        
        activityEvents.forEach(event => {
            document.addEventListener(event, () => {
                this.updateLastActivity();
            });
        });
    }

    /**
     * Update last activity time and reset session timer
     */
    updateLastActivity() {
        if (this.currentSession) {
            this.currentSession.lastActivity = new Date();
            
            // Reset session timer
            if (this.sessionTimer) {
                clearTimeout(this.sessionTimer);
                this.setupSessionTimeout();
            }
        }
    }

    /**
     * Handle session timeout
     */
    handleSessionTimeout() {
        this.log('Session timed out', 'warn');
        
        if (confirm('Your session has timed out due to inactivity. Would you like to start a new assessment?')) {
            this.resetApplication();
        } else {
            this.log('User chose not to restart after timeout', 'info');
        }
    }

    /**
     * Print the results page
     */
    printResults() {
        try {
            // Create a print-friendly version
            const printWindow = window.open('', '_blank');
            const printContent = this.generatePrintableContent();
            
            printWindow.document.write(printContent);
            printWindow.document.close();
            
            // Print after content loads
            printWindow.onload = () => {
                printWindow.print();
                printWindow.close();
            };
            
            this.log('Print dialog opened', 'info');
            
        } catch (error) {
            this.log('Error printing results: ' + error.message, 'error');
            alert('Unable to print. Please try using your browser\'s print function (Ctrl+P).');
        }
    }

    /**
     * Generate printable content
     */
    generatePrintableContent() {
        const summaryContainer = document.getElementById('loan-summary');
        const requirementsContainer = document.getElementById('requirements-list');
        
        const summaryHTML = summaryContainer ? summaryContainer.innerHTML : '';
        const requirementsHTML = requirementsContainer ? requirementsContainer.innerHTML : '';
        
        const currentDate = new Date().toLocaleDateString();
        
        return `
            <!DOCTYPE html>
            <html>
            <head>
                <title>Loan Conditions Matrix - Results</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .header { text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 10px; }
                    .summary { margin-bottom: 30px; }
                    .requirements { margin-bottom: 30px; }
                    .requirement-item { margin-bottom: 10px; padding: 8px; border: 1px solid #ddd; }
                    .footer { margin-top: 30px; text-align: center; font-size: 12px; color: #666; }
                    @media print { .no-print { display: none; } }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Loan Conditions Matrix</h1>
                    <h2>Commercial Lending Requirements</h2>
                    <p>Generated on: ${currentDate}</p>
                </div>
                
                <div class="summary">
                    ${summaryHTML}
                </div>
                
                <div class="requirements">
                    ${requirementsHTML}
                </div>
                
                <div class="footer">
                    <p>BCSB Commercial Banking - Confidential Document</p>
                    <p>This document contains proprietary lending requirements and should not be distributed outside the organization.</p>
                </div>
            </body>
            </html>
        `;
    }

    /**
     * Export results to PDF
     */
    exportToPDF() {
        try {
            if (!APP_CONFIG.PDF_EXPORT.enabled) {
                alert('PDF export is not currently available.');
                return;
            }

            // For now, use print functionality as PDF export
            // In production, this would integrate with a PDF generation library
            this.log('PDF export requested - using print dialog', 'info');
            alert('Please use your browser\'s print function and select "Save as PDF" as the destination.');
            this.printResults();
            
        } catch (error) {
            this.log('Error exporting to PDF: ' + error.message, 'error');
            alert('Unable to export to PDF. Please try the print function instead.');
        }
    }

    /**
     * Reset the application to initial state
     */
    resetApplication() {
        try {
            // Clear session data
            this.currentSession = null;
            
            // Clear session timer
            if (this.sessionTimer) {
                clearTimeout(this.sessionTimer);
                this.sessionTimer = null;
            }
            
            // Reset questionnaire if available
            if (window.questionnaireManager) {
                window.questionnaireManager.resetAssessment();
            }
            
            // Initialize new session
            this.initializeSession();
            
            this.log('Application reset successfully', 'info');
            
        } catch (error) {
            this.log('Error resetting application: ' + error.message, 'error');
        }
    }

    /**
     * Save current session data
     */
    saveSession() {
        if (!APP_CONFIG.FEATURES.saveSession) return;
        
        try {
            if (this.currentSession && window.questionnaireManager) {
                this.currentSession.answers = window.questionnaireManager.answers;
                this.currentSession.currentQuestionIndex = window.questionnaireManager.currentQuestionIndex;
                
                // Save to localStorage
                localStorage.setItem('loanConditionsSession', JSON.stringify(this.currentSession));
                
                this.log('Session saved', 'debug');
            }
        } catch (error) {
            this.log('Error saving session: ' + error.message, 'error');
        }
    }

    /**
     * Load saved session data
     */
    loadSession() {
        if (!APP_CONFIG.FEATURES.saveSession) return null;
        
        try {
            const savedSession = localStorage.getItem('loanConditionsSession');
            if (savedSession) {
                const sessionData = JSON.parse(savedSession);
                
                // Check if session is still valid (not expired)
                const sessionAge = new Date() - new Date(sessionData.lastActivity);
                const maxAge = APP_CONFIG.SESSION_TIMEOUT * 60 * 1000;
                
                if (sessionAge < maxAge) {
                    this.log('Loaded saved session', 'info');
                    return sessionData;
                } else {
                    // Remove expired session
                    localStorage.removeItem('loanConditionsSession');
                    this.log('Removed expired session', 'info');
                }
            }
        } catch (error) {
            this.log('Error loading session: ' + error.message, 'error');
        }
        
        return null;
    }

    /**
     * Get application status
     */
    getStatus() {
        return {
            isInitialized: this.isInitialized,
            sessionId: this.currentSession ? this.currentSession.sessionId : null,
            uptime: this.currentSession ? new Date() - this.currentSession.startTime : 0,
            config: APP_CONFIG
        };
    }

    /**
     * Logging utility
     */
    log(message, level = 'info') {
        if (APP_CONFIG.CONSOLE_LOGGING && 
            this.shouldLog(level)) {
            
            const timestamp = new Date().toISOString();
            console[level](`[${timestamp}] [LoanConditionsApp] ${message}`);
        }
    }

    /**
     * Check if message should be logged based on log level
     */
    shouldLog(level) {
        const levels = { debug: 0, info: 1, warn: 2, error: 3 };
        const configLevel = levels[APP_CONFIG.LOG_LEVEL] || 1;
        const messageLevel = levels[level] || 1;
        
        return messageLevel >= configLevel;
    }
}

// Initialize the application when the script loads
document.addEventListener('DOMContentLoaded', () => {
    window.loanConditionsApp = new LoanConditionsApp();
});
