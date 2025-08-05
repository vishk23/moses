// questionFlow.js
// Handles question/answer logic and UI for Loan Conditions Matrix
import { getRequirements } from './policyMapping.js';

const questions = [
    {
        id: 'loanType',
        text: 'What type of loan are you requesting?',
        options: ['Commercial Real Estate', 'Term Loan', 'Line of Credit']
    },
    {
        id: 'collateral',
        text: 'Is collateral being provided?',
        options: ['Yes', 'No']
    },
    {
        id: 'guarantor',
        text: 'Is there a guarantor?',
        options: ['Yes', 'No']
    }
];

let answers = {};

function renderQuestions() {
    const container = document.getElementById('question-container');
    container.innerHTML = '';
    questions.forEach(q => {
        const div = document.createElement('div');
        div.className = 'question-block';
        div.innerHTML = `<label><strong>${q.text}</strong></label><br>`;
        q.options.forEach(opt => {
            const input = document.createElement('input');
            input.type = 'radio';
            input.name = q.id;
            input.value = opt;
            input.onchange = () => {
                answers[q.id] = opt;
                updateRequirements();
            };
            div.appendChild(input);
            div.appendChild(document.createTextNode(opt));
            div.appendChild(document.createElement('br'));
        });
        container.appendChild(div);
    });
}

function updateRequirements() {
    const reqs = getRequirements(answers);
    const reqContainer = document.getElementById('requirements-container');
    reqContainer.innerHTML = '<h2>Required Documents & Conditions</h2>';
    if (reqs.length === 0) {
        reqContainer.innerHTML += '<p>Please answer all questions to see requirements.</p>';
    } else {
        const ul = document.createElement('ul');
        reqs.forEach(r => {
            const li = document.createElement('li');
            li.textContent = r;
            ul.appendChild(li);
        });
        reqContainer.appendChild(ul);
    }
}

// Initial render
renderQuestions();
