// policyMapping.js
// Maps answers to loan policy requirements for Loan Conditions Matrix

export function getRequirements(answers) {
    // Example mapping logic
    if (!answers.loanType || !answers.collateral || !answers.guarantor) {
        return [];
    }
    const reqs = [];
    if (answers.loanType === 'Commercial Real Estate') {
        reqs.push('Appraisal of property');
        reqs.push('Environmental assessment');
    }
    if (answers.collateral === 'Yes') {
        reqs.push('Collateral documentation');
    } else {
        reqs.push('Unsecured loan approval');
    }
    if (answers.guarantor === 'Yes') {
        reqs.push('Guarantor financial statement');
    }
    // Add more mapping logic as needed
    return reqs;
}
