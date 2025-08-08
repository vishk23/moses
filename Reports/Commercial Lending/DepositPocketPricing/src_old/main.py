# %%
# Building a parser for input file
from pathlib import Path
import pandas as pd
from src._version import __version__

# %%
def main():
    INPUT_PATH = Path("./assets/DepositPocketPricing.xlsx")

    # %%
    df = pd.read_excel(INPUT_PATH)


    df = df[~(df['New Acct. Open Date'].isnull())].copy()

    df = df[['Region','CLO','Customer','New Acct. Open Date','New Acct Type','New Money 2','New Rate','Source of Funds (What bank?)']].copy()

    df['New Acct. Open Date'] = pd.to_datetime(df['New Acct. Open Date'])
    df = df.sort_values(by='New Acct. Open Date').copy()

    # %%
    df['New Money 2'] = df['New Money 2'].fillna(0)

    # %%
    df['Cumulative New Money'] = df['New Money 2'].cumsum()


    # %%
    OUTPUT_PATH = Path('./output/deposit_pocket_pricing_raw.xlsx')
    df.to_excel(OUTPUT_PATH, index=False)
    return True

if __name__ == '__main__':
    print(f"Starting [{__version__}]")
    # main(production_flag=True)
    main()
    print("Complete!")





