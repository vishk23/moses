from datetime import datetime


def isolate_total_past_due(df):
    df['totalpaymentsdue'] = (
        df['principaldue'] +
        df['interestdue'] + 
        df['escrowdue'] +
        df['latechargedue'] +
        df['notedue'] +
        df['miscdue']
    )

    now = datetime.now()
    first_day_of_month = datetime(now.year, now.month, 1, 0, 0, 0)
    formatted_date = first_day_of_month.strftime("%Y-%m-%d %H:%M:%S")

    df['rundate'] = formatted_date
    
    # Create delinquent date (due date + 15 days)
    df['delinquentdate'] = df['duedate']
    
    # Exclude payments billed that are not past due & drop helper field
    df = df[df['delinquentdate'] < df['rundate']]
    df = df.drop(columns=['delinquentdate'])
    
    # Group by acctnbr, sum totaldue and show earliest due date
    aggregated_df = df.groupby('acctnbr').agg({
        'totalpaymentsdue':'sum',
        'duedate': 'min'
    }).reset_index()
    
    # aggregated_df = aggregated_df.rename(columns={
    # 'acctnbr': 'Account Number',
    # })

    aggregated_df = aggregated_df[['acctnbr', 'totalpaymentsdue']]

    return aggregated_df