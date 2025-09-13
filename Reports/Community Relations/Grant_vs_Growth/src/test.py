import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- Assume df_pivot from the previous step already exists ---
# If not, you can recreate it with the previous code.
# Here's a quick recreation for context:
# (You would not need to run this again if it's in the same script)
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


# --- 1. Select Data for the Most Recent Year ---
latest_year = df_pivot.index.max()
df_latest = df_pivot.loc[latest_year]

# We don't want to plot the 'Total' or 'Unmapped' in a regional comparison
regions_to_plot = [r for r in df_latest.index.get_level_values(0).unique() if r not in ['Total', 'Unmapped']]
df_plot_data = df_latest.loc[regions_to_plot]

# --- 2. Prepare for Plotting ---
labels = regions_to_plot
# Use .xs() to select from the second level (level=1) of the index
loan_values = df_plot_data.xs('loan_balance', level=1)
deposit_values = df_plot_data.xs('deposit_balance', level=1)
grant_values = df_plot_data.xs('grant_amount', level=1)

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

# --- 3. Create the Visualization ---
fig, ax1 = plt.subplots(figsize=(14, 8))

# Define formatters for currency axes
def millions_formatter(x, pos):
    return f'${x / 1e6:.0f}M'

def thousands_formatter(x, pos):
    return f'${x / 1e3:.0f}K'

# Plotting the bars for Loans and Deposits on the primary axis (ax1)
rects1 = ax1.bar(x - width/2, loan_values, width, label='Loan Balance', color='royalblue')
rects2 = ax1.bar(x + width/2, deposit_values, width, label='Deposit Balance', color='skyblue')

# Setting labels and formatting for the primary axis
ax1.set_ylabel('Balance (Millions)', fontsize=14)
ax1.set_xlabel('Region', fontsize=14)
ax1.set_title(f'Regional Balances vs. Giving for {latest_year}', fontsize=18, pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Create the secondary axis for the grant data
ax2 = ax1.twinx()
# Plotting grants as a line with markers is often clearer than a third bar
ax2.plot(x, grant_values, color='green', linestyle='--', marker='o', markersize=8, label='Grants Awarded')

# Setting labels and formatting for the secondary axis
ax2.set_ylabel('Grant Amount (Thousands)', color='green', fontsize=14)
ax2.tick_params(axis='y', labelcolor='green')
ax2.set_ylim(bottom=0) # Ensure the grant axis starts at 0
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))

# Create a combined legend for both axes
lines, labels_from_plot = ax1.get_legend_handles_labels()
lines2, labels2_from_plot = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels_from_plot + labels2_from_plot, loc='upper left')

fig.tight_layout()
plt.show()
