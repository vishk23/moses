# Loan Conditions Survey

This repository contains a simple web application designed to help users generate a summary of loan conditions based on a customizable survey. It features both a user-facing survey interface and an administrative panel for managing survey questions and options.

## Project Structure

The project consists of two main HTML files, each serving a distinct purpose:

*   **`survey.html`**: The user-facing survey application. Users interact with this page to answer questions, and based on their responses, a summarized list of requirements is generated.
*   **`admin.html`**: The administration panel for creating, editing, and managing the survey's content (sections, questions, and options). It allows for dynamic configuration of the survey structure.

## Features

### `survey.html` (User Interface)

*   **Dynamic Survey Generation**: Displays survey questions and options based on an embedded JSON configuration.
*   **Conditional Logic**: Supports conditional questions, where certain questions only appear based on previous answers (e.g., selecting "Yes" reveals follow-up questions).
*   **Multiple Question Types**: Includes support for radio buttons (single choice), checkboxes (multiple choice), and free-form text input.
*   **Progress Tracking**: A progress bar indicates how much of the survey has been completed.
*   **Requirements Summary**: Generates a clear, section-based summary of loan conditions based on the user's answers.
*   **Copy to Clipboard**: Users can easily copy the generated requirements summary to their clipboard for external use.
*   **Validation**: Ensures all required questions are answered before generating the summary.

## `admin.html` (Admin Panel)

*   **Intuitive Drag-and-Drop Configuration**: Easily load and manage survey configurations via JSON files. Supports drag-and-drop file uploads.
*   **Section and Question Management**: Add, edit, delete, and duplicate sections and questions within the survey.
*   **Option and Child Question Management**: Define options for multi-choice questions and link them to conditional child questions.
*   **Real-time Editing**: Changes are reflected instantly in the editor.
*   **Configuration Download**: Download the current survey configuration as a JSON file.
*   **Validation Tool**: Validates the survey structure for common errors and provides warnings, ensuring a robust configuration.
*   **Live Preview**: Get a quick visual preview of how the survey will appear to users.
*   **Embed Code Generation**: Generates the JSON required to directly embed the survey configuration into `survey.html`.

## Getting Started

To use this application:

1.  **Clone the Repository**:

2.  **Open `admin.html`**: Start by opening `admin.html` in your web browser. This is where you will configure your survey.

3.  **Configure Your Survey**:
    *   Use the "Add New Section" button to begin building your survey.
    *   Add questions, options, and define summary labels for the conditions you want to capture.
    *   Utilize the "Validate" button periodically to check for errors in your configuration.
    *   Use the "Preview" button to see how your survey will look.

4.  **Copy for Embedding**: Once your survey is configured, click the "Copy for Embedding" button. This will provide you with the JSON code of your survey configuration.

5.  **Embed in `survey.html`**: Open `survey.html` in a text editor. Locate the embedded JSON configuration section (usually identified by a comment block containing backticks ``` `` ```) and paste the copied JSON code within those backticks.

6.  **Open `survey.html`**: Now, open `survey.html` in your web browser. Your newly configured survey should be displayed, ready for use!

## Technologies Used

*   **HTML5**: Structure of the web pages.
*   **CSS3**: Styling for a modern and responsive user interface.
*   **JavaScript (ES6+)**: Core logic for dynamic survey generation, admin panel functionality, and interaction.




Tweaks to make:
- Justify bullet points to be at the first line of each item (not centered)
- abundance of caution (typo)
- Environmental
    - Yes
        - if low risk category (ends there, remove rest of text)
- Flood
    - Yes -> Yes -> Yes

Should like the below:
The following conditions are required: 
- Customer was informed 10 days prior to closing, 
- The flood insurance been reviewed by compliance, 
- Sufficient flood insurance has been obtained

Other section
    - Add child questions
Corporate guarantor section
    - Add child questions

If not secured by RE (Appraisal Q1 = No)
- skip flood
- skip environmental

    