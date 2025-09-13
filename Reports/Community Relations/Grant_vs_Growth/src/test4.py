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

# --- 1. Prepare Data for Multi-Region Plotting ---
# Get the years for the x-axis
years = df_pivot.index.values

# Get the list of regions to plot, excluding 'Total' and 'Unmapped'
all_regions = df_pivot.columns.get_level_values(0).unique().tolist()
regions_to_plot = [r for r in all_regions if r not in ['Total', 'Unmapped']]

# You can add any custom code here if needed, but it's optional.

# --- 2. Prepare for Plotting ---
# Use .xs() to select from the second level (level=1) of the index
# Note: We keep the formatters here as requested.
# Define formatters for currency axes
def millions_formatter(x, pos):
    return f'${x / 1e6:.0f}M'

def thousands_formatter(x, pos):
    return f'${x / 1e3:.0f}K'

# --- 3. Create the Visualization (All Regions Over Time) ---
fig, ax1 = plt.subplots(figsize=(16, 9))

# Create a color map to cycle through for regions
colors = plt.cm.viridis(np.linspace(0, 1, len(regions_to_plot)))

# --- Primary Y-Axis: Loan and Deposit Balances ---
ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Balance (Millions)', fontsize=14)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# --- Secondary Y-Axis: Foundation Giving ---
ax2 = ax1.twinx()
ax2.set_ylabel('Foundation Giving (Thousands)', color='gray', fontsize=14)
ax2.tick_params(axis='y', labelcolor='gray')
ax2.set_ylim(bottom=0)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))

# --- Loop through regions to plot their data ---
for i, region in enumerate(regions_to_plot):
    # Extract the time series data for the current region
    df_region = df_pivot.xs(region, axis=1, level=0)
    
    # Plot Balances on the primary axis (ax1)
    # Solid line for Loans, dashed for Deposits
    ax1.plot(years, df_region['loan_balance'], label=f'{region} Loans', marker='o', color=colors[i], linestyle='-')
    ax1.plot(years, df_region['deposit_balance'], label=f'{region} Deposits', marker='s', color=colors[i], linestyle='--')
    
    # Plot Giving on the secondary axis (ax2)
    # Use the same color but a distinct style (dotted line, different marker)
    ax2.plot(years, df_region['grant_amount'], label=f'{region} Giving', color=colors[i], linestyle=':', marker='D')

# --- Final Touches: Title and Legend ---
start_year, end_year = years.min(), years.max()
ax1.set_title(f'Regional Trends: Balances vs. Foundation Giving ({start_year}–{end_year})', fontsize=18, pad=20)

# Create a consolidated legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
# To avoid clutter, it's better to place the legend outside the plot
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', 
           bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=len(regions_to_plot))

fig.tight_layout()

# --- 4. Write to PNG instead of showing a pop-up ---
outfile = f"all_regions_trend_{years.min()}-{years.max()}.png"
plt.savefig(outfile, dpi=300, bbox_inches='tight')
plt.close(fig)
