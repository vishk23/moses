/**
 * Questionnaire Module
 * 
 * Handles the user interface logic, question flow, form validation,
 * and user interactions for the Loan Conditions Matrix application.
 */

class QuestionnaireManager {
    constructor() {
        this.currentQuestionIndex = 0;
        this.answers = {};
        this.questions = [];
        this.isInitialized = false;
        
        this.initializeEventListeners();
    }

    /**
     * Initialize event listeners for the questionnaire interface
     */
    initializeEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            this.setupButtonHandlers();
            this.loadQuestions();
        });
    }

    /**
     * Set up button event handlers
     */
    setupButtonHandlers() {
        const startBtn = document.getElementById('start-assessment');
        const nextBtn = document.getElementById('next-btn');
        const prevBtn = document.getElementById('prev-btn');
        const startNewBtn = document.getElementById('start-new');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startAssessment());
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextQuestion());
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousQuestion());
        }

        if (startNewBtn) {
            startNewBtn.addEventListener('click', () => this.resetAssessment());
        }
    }

    /**
     * Load questions from configuration or data source
     */
    async loadQuestions() {
        try {
            // For now, use static questions. In production, load from external source
            this.questions = this.getStaticQuestions();
            this.isInitialized = true;
            this.log('Questions loaded successfully', 'info');
        } catch (error) {
            this.log('Error loading questions: ' + error.message, 'error');
        }
    }

    /**
     * Get static questions for development
     * TODO: Replace with dynamic loading from data source
     */
    getStaticQuestions() {
        return [
            {
                id: 'loan_type',
                category: APP_CONFIG.QUESTION_CATEGORIES.LOAN_TYPE,
                question: 'What type of loan are you processing?',
                type: 'select',
                required: true,
                options: [
                    { value: 'term_loan', text: 'Term Loan' },
                    { value: 'line_of_credit', text: 'Line of Credit' },
                    { value: 'equipment_financing', text: 'Equipment Financing' },
                    { value: 'real_estate', text: 'Commercial Real Estate' },
                    { value: 'sba_loan', text: 'SBA Loan' },
                    { value: 'construction', text: 'Construction Loan' }
                ]
            },
            {
                id: 'loan_amount',
                category: APP_CONFIG.QUESTION_CATEGORIES.FINANCIAL_INFO,
                question: 'What is the requested loan amount?',
                type: 'currency',
                required: true,
                validation: {
                    min: 10000,
                    max: 50000000
                }
            },
            {
                id: 'borrower_type',
                category: APP_CONFIG.QUESTION_CATEGORIES.BORROWER_INFO,
                question: 'What type of borrower is this?',
                type: 'radio',
                required: true,
                options: [
                    { value: 'corporation', text: 'Corporation' },
                    { value: 'llc', text: 'Limited Liability Company (LLC)' },
                    { value: 'partnership', text: 'Partnership' },
                    { value: 'sole_proprietorship', text: 'Sole Proprietorship' },
                    { value: 'non_profit', text: 'Non-Profit Organization' }
                ]
            },
            {
                id: 'industry_type',
                category: APP_CONFIG.QUESTION_CATEGORIES.BORROWER_INFO,
                question: 'What industry is the borrower in?',
                type: 'select',
                required: true,
                options: [
                    { value: 'manufacturing', text: 'Manufacturing' },
                    { value: 'retail', text: 'Retail Trade' },
                    { value: 'services', text: 'Professional Services' },
                    { value: 'healthcare', text: 'Healthcare' },
                    { value: 'real_estate', text: 'Real Estate' },
                    { value: 'agriculture', text: 'Agriculture' },
                    { value: 'construction', text: 'Construction' },
                    { value: 'other', text: 'Other' }
                ]
            },
            {
                id: 'collateral_type',
                category: APP_CONFIG.QUESTION_CATEGORIES.COLLATERAL,
                question: 'What type of collateral will secure this loan?',
                type: 'checkbox',
                required: true,
                options: [
                    { value: 'real_estate', text: 'Real Estate' },
                    { value: 'equipment', text: 'Equipment/Machinery' },
                    { value: 'inventory', text: 'Inventory' },
                    { value: 'accounts_receivable', text: 'Accounts Receivable' },
                    { value: 'personal_guarantee', text: 'Personal Guarantee' },
                    { value: 'cash_deposit', text: 'Cash Deposit/CD' },
                    { value: 'unsecured', text: 'Unsecured' }
                ]
            }
        ];
    }

    /**
     * Start the assessment process
     */
    startAssessment() {
        if (!this.isInitialized) {
            this.log('Questions not loaded yet', 'warn');
            return;
        }

        this.showSection('questionnaire-section');
        this.currentQuestionIndex = 0;
        this.displayCurrentQuestion();
        this.updateProgress();
    }

    /**
     * Display the current question
     */
    displayCurrentQuestion() {
        const container = document.getElementById('question-container');
        const question = this.questions[this.currentQuestionIndex];

        if (!question || !container) return;

        container.innerHTML = this.generateQuestionHTML(question);
        this.updateNavigationButtons();
        
        // Pre-fill with existing answer if available
        this.populateExistingAnswer(question);
    }

    /**
     * Generate HTML for a question based on its type
     */
    generateQuestionHTML(question) {
        let html = `
            <div class="question" data-question-id="${question.id}">
                <h3>${question.question}</h3>
                <div class="question-input">
        `;

        switch (question.type) {
            case 'select':
                html += this.generateSelectHTML(question);
                break;
            case 'radio':
                html += this.generateRadioHTML(question);
                break;
            case 'checkbox':
                html += this.generateCheckboxHTML(question);
                break;
            case 'currency':
                html += this.generateCurrencyHTML(question);
                break;
            case 'text':
                html += this.generateTextHTML(question);
                break;
            default:
                html += '<p>Question type not supported</p>';
        }

        html += `
                </div>
            </div>
        `;

        return html;
    }

    /**
     * Generate HTML for select dropdown
     */
    generateSelectHTML(question) {
        let html = `<select id="${question.id}" ${question.required ? 'required' : ''}>`;
        html += '<option value="">Please select...</option>';
        
        question.options.forEach(option => {
            html += `<option value="${option.value}">${option.text}</option>`;
        });
        
        html += '</select>';
        return html;
    }

    /**
     * Generate HTML for radio buttons
     */
    generateRadioHTML(question) {
        let html = '<div class="radio-group">';
        
        question.options.forEach(option => {
            html += `
                <div class="radio-option">
                    <input type="radio" id="${question.id}_${option.value}" 
                           name="${question.id}" value="${option.value}" 
                           ${question.required ? 'required' : ''}>
                    <label for="${question.id}_${option.value}">${option.text}</label>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }

    /**
     * Generate HTML for checkboxes
     */
    generateCheckboxHTML(question) {
        let html = '<div class="checkbox-group">';
        
        question.options.forEach(option => {
            html += `
                <div class="checkbox-option">
                    <input type="checkbox" id="${question.id}_${option.value}" 
                           name="${question.id}[]" value="${option.value}">
                    <label for="${question.id}_${option.value}">${option.text}</label>
                </div>
            `;
        });
        
        html += '</div>';
        return html;
    }

    /**
     * Generate HTML for currency input
     */
    generateCurrencyHTML(question) {
        return `
            <div class="currency-input">
                <span class="currency-symbol">$</span>
                <input type="number" id="${question.id}" 
                       ${question.required ? 'required' : ''}
                       ${question.validation?.min ? `min="${question.validation.min}"` : ''}
                       ${question.validation?.max ? `max="${question.validation.max}"` : ''}
                       placeholder="Enter amount">
            </div>
        `;
    }

    /**
     * Generate HTML for text input
     */
    generateTextHTML(question) {
        return `
            <input type="text" id="${question.id}" 
                   ${question.required ? 'required' : ''}
                   placeholder="Enter your answer">
        `;
    }

    /**
     * Move to the next question
     */
    nextQuestion() {
        if (this.validateCurrentQuestion()) {
            this.saveCurrentAnswer();
            
            if (this.currentQuestionIndex < this.questions.length - 1) {
                this.currentQuestionIndex++;
                this.displayCurrentQuestion();
                this.updateProgress();
            } else {
                this.completeAssessment();
            }
        }
    }

    /**
     * Move to the previous question
     */
    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.displayCurrentQuestion();
            this.updateProgress();
        }
    }

    /**
     * Validate the current question's answer
     */
    validateCurrentQuestion() {
        const question = this.questions[this.currentQuestionIndex];
        const element = document.getElementById(question.id);

        if (!question.required) return true;

        switch (question.type) {
            case 'checkbox':
                const checkboxes = document.querySelectorAll(`input[name="${question.id}[]"]:checked`);
                return checkboxes.length > 0;
            case 'radio':
                const radio = document.querySelector(`input[name="${question.id}"]:checked`);
                return radio !== null;
            default:
                return element && element.value.trim() !== '';
        }
    }

    /**
     * Save the current question's answer
     */
    saveCurrentAnswer() {
        const question = this.questions[this.currentQuestionIndex];
        
        switch (question.type) {
            case 'checkbox':
                const checkboxes = document.querySelectorAll(`input[name="${question.id}[]"]:checked`);
                this.answers[question.id] = Array.from(checkboxes).map(cb => cb.value);
                break;
            case 'radio':
                const radio = document.querySelector(`input[name="${question.id}"]:checked`);
                this.answers[question.id] = radio ? radio.value : null;
                break;
            default:
                const element = document.getElementById(question.id);
                this.answers[question.id] = element ? element.value : null;
        }

        this.log(`Answer saved for ${question.id}: ${JSON.stringify(this.answers[question.id])}`, 'debug');
    }

    /**
     * Populate existing answer for a question
     */
    populateExistingAnswer(question) {
        const existingAnswer = this.answers[question.id];
        if (!existingAnswer) return;

        switch (question.type) {
            case 'checkbox':
                if (Array.isArray(existingAnswer)) {
                    existingAnswer.forEach(value => {
                        const checkbox = document.getElementById(`${question.id}_${value}`);
                        if (checkbox) checkbox.checked = true;
                    });
                }
                break;
            case 'radio':
                const radio = document.getElementById(`${question.id}_${existingAnswer}`);
                if (radio) radio.checked = true;
                break;
            default:
                const element = document.getElementById(question.id);
                if (element) element.value = existingAnswer;
        }
    }

    /**
     * Update navigation buttons state
     */
    updateNavigationButtons() {
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');

        if (prevBtn) {
            prevBtn.disabled = this.currentQuestionIndex === 0;
        }

        if (nextBtn) {
            const isLastQuestion = this.currentQuestionIndex === this.questions.length - 1;
            nextBtn.textContent = isLastQuestion ? 'Complete Assessment' : 'Next';
        }
    }

    /**
     * Update progress bar
     */
    updateProgress() {
        const progressFill = document.getElementById('progress-fill');
        if (progressFill) {
            const progress = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
            progressFill.style.width = `${progress}%`;
        }
    }

    /**
     * Complete the assessment and show results
     */
    completeAssessment() {
        this.saveCurrentAnswer();
        this.log('Assessment completed', 'info');
        
        // Trigger policy mapping and show results
        if (window.policyMapper) {
            const requirements = window.policyMapper.generateRequirements(this.answers);
            this.displayResults(requirements);
        }
        
        this.showSection('results-section');
    }

    /**
     * Display assessment results
     */
    displayResults(requirements) {
        const summaryContainer = document.getElementById('loan-summary');
        const requirementsContainer = document.getElementById('requirements-list');

        if (summaryContainer) {
            summaryContainer.innerHTML = this.generateSummaryHTML();
        }

        if (requirementsContainer && requirements) {
            requirementsContainer.innerHTML = this.generateRequirementsHTML(requirements);
        }
    }

    /**
     * Generate summary HTML
     */
    generateSummaryHTML() {
        return `
            <div class="loan-summary">
                <h3>Loan Summary</h3>
                <div class="summary-grid">
                    <div class="summary-item">
                        <strong>Loan Type:</strong> ${this.answers.loan_type || 'Not specified'}
                    </div>
                    <div class="summary-item">
                        <strong>Amount:</strong> $${this.formatCurrency(this.answers.loan_amount)}
                    </div>
                    <div class="summary-item">
                        <strong>Borrower Type:</strong> ${this.answers.borrower_type || 'Not specified'}
                    </div>
                    <div class="summary-item">
                        <strong>Industry:</strong> ${this.answers.industry_type || 'Not specified'}
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Generate requirements HTML
     */
    generateRequirementsHTML(requirements) {
        if (!requirements || requirements.length === 0) {
            return '<p>No specific requirements generated.</p>';
        }

        let html = '<div class="requirements-list"><h3>Required Documentation & Conditions</h3><ul>';
        
        requirements.forEach(requirement => {
            html += `<li class="requirement-item">${requirement}</li>`;
        });
        
        html += '</ul></div>';
        return html;
    }

    /**
     * Reset assessment to start over
     */
    resetAssessment() {
        this.currentQuestionIndex = 0;
        this.answers = {};
        this.showSection('welcome-section');
    }

    /**
     * Show a specific section and hide others
     */
    showSection(sectionId) {
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => section.classList.remove('active'));
        
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
        }
    }

    /**
     * Format currency for display
     */
    formatCurrency(amount) {
        if (!amount) return '0';
        return new Intl.NumberFormat('en-US').format(amount);
    }

    /**
     * Logging utility
     */
    log(message, level = 'info') {
        if (APP_CONFIG.CONSOLE_LOGGING && APP_CONFIG.DEBUG) {
            console[level](`[Questionnaire] ${message}`);
        }
    }
}

// Initialize questionnaire manager
window.questionnaireManager = new QuestionnaireManager();
