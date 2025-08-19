def unpack_data(data):
    """
    Unpack the data from the data dictionary and into their respective dataframes
    """
    wh_acctcommon_me = data['wh_acctcommon_me'].copy()
    wh_loans_me = data['wh_loans_me'].copy()
    wh_acctloan_me = data['wh_acctloan_me'].copy()
    wh_acct_me = data['wh_acct_me'].copy()
    wh_prop = data['wh_prop'].copy()
    wh_prop2 = data['wh_prop2'].copy()
    return wh_acctcommon_me, wh_loans_me, wh_acctloan_me, wh_acct_me, wh_prop, wh_prop2