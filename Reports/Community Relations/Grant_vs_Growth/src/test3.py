import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- Assume df_pivot from the previous step already exists ---
# If not, you can recreate it with the previous code.
# (The recreation is included below for completeness)
years = [2021, 2022, 2023, 2024]
regions = ['North', 'South', 'East', 'West', 'Unmapped']
data = []
for year in years:
    for region in regions:
        data.append({
            'year': year,
            'region': region,
            'loan_balance': np.random.uniform(250e6, 800e6) * (1 + (year-2021)*0.06),
            'deposit_balance': np.random.uniform(400e6, 1200e6) * (1 + (year-2021)*0.08),
            'grant_amount': np.random.uniform(0.5e6, 2e6) * (1 + (year-2021)*0.1)
        })
df_consolidated = pd.DataFrame(data)
df_pivot = df_consolidated.pivot_table(index='year', columns='region', values=['loan_balance', 'deposit_balance', 'grant_amount'])
df_pivot = df_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)
# --- End of recreation ---

# --- 1. Choose Region and Put Year on X-Axis ---
# Regions available (top level of columns after swaplevel)
all_regions = df_pivot.columns.get_level_values(0).unique().tolist()
regions_to_use = [r for r in all_regions if r not in ['Total', 'Unmapped']]

# Choose ONE region to visualize across time (edit as needed)
region_to_plot = regions_to_use[0]  # e.g., 'North'

# Extract time series for the chosen region; columns become the metrics
df_region = df_pivot.xs(region_to_plot, axis=1, level=0).sort_index().copy()

# Year vector (x-axis) and series
years = df_region.index.values
loan_series = df_region['loan_balance'].values
deposit_series = df_region['deposit_balance'].values
giving_series = df_region['grant_amount'].values  # Foundation giving

# --- 2. Create the Visualization (Year on X-Axis) ---
fig, ax1 = plt.subplots(figsize=(14, 8))

# Define formatters for currency axes
def millions_formatter(x, pos):
    return f'${x / 1e6:.0f}M'

def thousands_formatter(x, pos):
    return f'${x / 1e3:.0f}K'

# Primary y-axis: loan & deposit balances (in millions)
ax1.plot(years, loan_series, label='Loan Balance', marker='o', linewidth=2, color='royalblue')
ax1.plot(years, deposit_series, label='Deposit Balance', marker='s', linewidth=2, color='skyblue')
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Balance (Millions)', fontsize=14)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Secondary y-axis: foundation giving (in thousands)
ax2 = ax1.twinx()
ax2.plot(years, giving_series, label='Foundation Giving', linestyle='--', marker='D', markersize=7, linewidth=2, color='green')
ax2.set_ylabel('Foundation Giving (Thousands)', color='green', fontsize=14)
ax2.tick_params(axis='y', labelcolor='green')
ax2.set_ylim(bottom=0)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))

# Title reflects time span and region
ax1.set_title(f'{region_to_plot}: Loan/Deposit vs. Foundation Giving ({years.min()}–{years.max()})', fontsize=18, pad=20)

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

fig.tight_layout()

# --- 4. Write to PNG instead of showing a pop-up ---
outfile = f"regional_trend_{region_to_plot}_{years.min()}-{years.max()}.png"
plt.savefig(outfile, dpi=300, bbox_inches='tight')
plt.close(fig)
