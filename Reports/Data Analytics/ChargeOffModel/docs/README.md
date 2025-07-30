# Loan Charge-Off Prediction Pipeline
===
This project implements a logistic regrsesion pipeline to predict loan charge-offs based on borrower and loan characteristics.
<br>
A charge-off occurs when a borrower fails to repay a loan and the lender classifies it as a loss. By identifying high-risk loans before they are approved, the bank can make more informed lending decisions and reduce future charge-offs. This pipeline queries the database, performs preprocessing, trains a logistic regression model, evaluates its performance, and makes predictions. 

## Authors & Stakeholders
- Developed by: 
    - Troy Caron (troy.caron@bcsbmail.com)
- Key Stakeholders:
    - Risk Management, Credit Underwriting

## File Paths
- Project Home:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\ChargeOffModel
- Input Data:
    - Queried from database
- Output:
    - \\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\ChargeOffModel\Production\output

## Overview of Pipelines

### Training
1. Query the database and preprocess to get relevant data for training
2. Split data into training and test and scale numerical features
3. Train the model using training data.
4. Save the model and scaler to their respective directories
5. Test model using testing data and print accuracies and weights to the console.

### Predicting
1. Load the model and scaler from their respective directories
2. Query the database and preprocess to get data ready to make predictions
3. Make copies of original data before scaling to preserve readability in output
4. Use model to predict processed data.
5. Append copies of original data to predictions
6. Calculate danger zone (false positives where we predicted a cobal but one doesn't exist yet)
7. Format and output danger zone to excel in Production/output/


## How to run

1. If you haven't already, cd to Production and run <pre>pip install -r requirements.txt <pre>
2. If you want to retrain the model, navigate to Production and run <pre>python -m src.main train </pre>
3. If you want to predict new loans with the model, navigate to Production and run <pre>python -m src.main predict </pre>