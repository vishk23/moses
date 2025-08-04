# 2025-08-04
Manage engine raw data

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 15690 entries, 0 to 15689
Data columns (total 15 columns):
 #   Column                Non-Null Count  Dtype 
---  ------                --------------  ----- 
 0   Patch ID              15690 non-null  int64 
 1   Bulletin ID           15690 non-null  object
 2   Patch Description     15690 non-null  object
 3   Patch Status          15690 non-null  object
 4   Computer Name         15690 non-null  object
 5   Operating System      15690 non-null  object
 6   Deployed Date         7218 non-null   object
 7   Remarks               7218 non-null   object
 8   Patch Uninstallation  15690 non-null  object
 9   Release Date          15690 non-null  object
 10  Deployed By           5670 non-null   object
 11  Severity              15690 non-null  object
 12  Deployment Status     7218 non-null   object
 13  Patch Type            15690 non-null  object
 14  Remote Office         15690 non-null  object
dtypes: int64(1), object(14)
memory usage: 1.8+ MB

If Remote Office in ('Domain Controllers, Member Servers), then 'Server' else 'Workstation'

New table
ComputerCompliance =
ADDCOLUMNS (
    SUMMARIZE (
        'patch_data',
        'patch_data'[Computer Name]
    ),
    "OutOfComplianceStatus",
    IF (
        CALCULATE (
            COUNTROWS ( 'patch_data' ),
            'patch_data'[Computer Name] = EARLIER ( 'patch_data'[Computer Name] ),
            'patch_data'[Compliance Flag] = 1
        ) > 0,
        "Out of Compliance",
        "Compliant"
    )
)