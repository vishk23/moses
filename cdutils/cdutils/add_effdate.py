import pandas as pd
from datetime import datetime
from pandas.tseries.holiday import USFederalHolidayCalendar

def add_effdate(df):
    """
    Adds a new column 'effdate' to the input df containing the last business day (excluding weekends and US federal bank holidays) as of the current date.
    """
    today = datetime.now().date()

    cal = USFederalHolidayCalendar()
    holidays = cal.holidays(start='1900-01-01', end='2100-12-31').date

    current_date = today - pd.Timedelta(days=1)
    while True:
        if current_date.weekday() < 5 and current_date not in holidays:
            last_business_day = current_date
            break
        current_date -= pd.Timedelta(days=1)

    df_with_effdate = df.assign(effdate=pd.Timestamp(last_business_day))

    return df_with_effdate