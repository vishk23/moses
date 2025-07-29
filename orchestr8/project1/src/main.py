import pandas as pd
from pathlib import Path

def main():
    x = {'col1':[1,2,3]}
    df = pd.DataFrame(x)

    OUTPUT_PATH = Path('./data.csv')
    df.to_csv(OUTPUT_PATH, index=False)
    print("Complete proj1 haha this is great!")

if __name__ == '__main__':
    main()