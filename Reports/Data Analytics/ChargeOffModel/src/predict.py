import joblib
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

import src.format_excel_file as format_excel_file
import src.getDataWithAcctStats as getDataWithAcctStats
from src.config import OUTPUT_DIR

def predict():

    # Ensuring model and scaler are present in directory
    if (not os.listdir("models")) or not os.listdir("scalers"):
        raise ValueError("The models or scalers directory is empty.")
    else:
        model = joblib.load("models/cobal_model.joblib")
        scaler = joblib.load("scalers/scaler.joblib")

    # Getting data
    X, y, dataWithAcctStats = getDataWithAcctStats.getDataWithAcctStats()
    
    X = X.drop(columns="NSF") # Trivial
    X_original = X.copy()

    # X.iloc[:, 25:] = X.iloc[:, 25:].astype(int)
    identifiers = dataWithAcctStats[['ownersortname', 'product']]

    # Scaling before making predictions
    features_to_be_scaled = ['noteintrate', 'origintrate', 'riskratingcd',
                            'contract_to_maturity_days', 'DOD', 'EFEE', 'EXT', 'KITE', 'MCHG', 'PD', 'PD12',
        'PD15', 'PD18', 'PD30', 'PD60', 'PD90', 'RGD3', 'RGD6', 'RNEW', 'SKIP',
        'UCF']
    X[features_to_be_scaled] = scaler.transform(X[features_to_be_scaled])


    y_pred = model.predict(X)


    # Aggregating data and results for output
    X_original = X_original.iloc[:, :23]
    X_original['ownersortname'] = identifiers['ownersortname']
    X_original['product'] = identifiers['product']
    cols = ['ownersortname', 'product'] + [col for col in X_original.columns if col not in ['ownersortname', 'product']]
    X_original = X_original[cols]
    X_original['y'] = y
    X_original['y_pred'] = y_pred

    # Calculating danger zone (false positives, loans with a high risk of charge off)
    danger_zone = X_original[(X_original['y'] == 0) & (X_original['y_pred'] == 1)]


    # grabbing date for filename
    today = datetime.today()
    date = f"{today.strftime('%B')} {today.day} {today.year}"
    output_file_path = OUTPUT_DIR / Path("Danger Zone " + date + ".xlsx")

    danger_zone.to_excel(output_file_path, index=False)
    format_excel_file.format_excel_file(output_file_path)
    print("Complete.")




