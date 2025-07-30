def isolate_total_past_due(df):
    df['totaldue'] = (
        df['principaldue'] +
        df['interestdue'] + 
        df['escrowdue'] +
        df['latechargedue'] +
        df['notedue'] +
        df['miscdue']
    )
    
    # Create delinquent date (due date + 15 days)
    df['delinquentdate'] = df['duedate']
    
    # Exclude payments billed that are not past due & drop helper field
    df = df[df['delinquentdate'] <= df['rundate']]
    df = df.drop(columns=['delinquentdate'])
    
    # Group by acctnbr, sum totaldue and show earliest due date
    aggregated_df = df.groupby('acctnbr').agg({
        'totaldue':'sum',
        'duedate': 'min'
    }).reset_index()
    
    aggregated_df = aggregated_df.rename(columns={
    'acctnbr': 'Account Number',
    })

    aggregated_df = aggregated_df[['Account Number', 'totaldue']]

    return aggregated_df