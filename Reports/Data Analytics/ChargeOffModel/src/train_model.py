from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
from pathlib import Path

import src.getDataWithAcctStats as getDataWithAcctStats
from src.config import BASE_PATH

import joblib
import numpy as np
import os

def train_model():

    # Getting data
    X, y, dataWithAcctStats = getDataWithAcctStats.getDataWithAcctStats()

    X = X.drop(columns="NSF") # Trivial
    # X.iloc[:, 25:] = X.iloc[:, 25:].astype(int)


    # Splitting and scaling data
    features_to_be_scaled = ['noteintrate', 'origintrate', 'riskratingcd',
                            'contract_to_maturity_days', 'DOD', 'EFEE', 'EXT', 'KITE', 'MCHG', 'PD', 'PD12',
        'PD15', 'PD18', 'PD30', 'PD60', 'PD90', 'RGD3', 'RGD6', 'RNEW', 'SKIP',
        'UCF']
    scaler = StandardScaler()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    X_train[features_to_be_scaled] = scaler.fit_transform(X_train[features_to_be_scaled])
    X_test[features_to_be_scaled] = scaler.transform(X_test[features_to_be_scaled])

    
    # Training model
    print("Training model...")
    model = LogisticRegression(class_weight='balanced', max_iter=100000)
    model.fit(X_train, y_train)


    # grabbing date for filenames
    today = datetime.today()
    date = f"{today.strftime('%B')} {today.day} {today.year}"

    # saving model and scaler in their respective directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('scalers', exist_ok=True)
    joblib.dump(model, BASE_PATH / Path("models/cobal_model " + date + ".joblib"))
    joblib.dump(scaler, BASE_PATH / Path("scalers/scaler " + date + ".joblib"))

    print("Model trained and saved.")

    # Outputting accuracies and weights to console
    print("\n\nAccuracy on test set:")
    y_pred = model.predict(X_test)
    print("Accuracy score: " + str(accuracy_score(y_test, y_pred)) + "\n")
    print("Accuracy when y is 1: " 
          + (str(((y_test == y_pred) & (y_test == 1)).sum() / len(y_test[y_test == 1]) * 100) + "% \n"))

    coefficients = model.coef_[0]
    feature_names = X.columns

    # Sort coefficients by absolute value
    sorted_indices = np.argsort((coefficients))[::-1]  # Sort in descending order

    # Print sorted coefficients and feature names
    print("Sorted Coefficients:")
    for index in sorted_indices:
        print(f"{feature_names[index]}: {coefficients[index]}")