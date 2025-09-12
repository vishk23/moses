import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Assumption: You have a DataFrame 'df' with columns: region, year, loan_balance, deposit_balance, grant_amount
# If not, provide your actual df setup. Here's an example to get started:

# Example data generation (replace with your actual df loading)
np.random.seed(42)
years = [2018, 2019, 2020, 2021, 2022]
regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West', 'Total', 'Unmapped']
n = 500

df = pd.DataFrame({
    'region': np.random.choice(regions, n),
    'year': np.random.choice(years, n),
    'loan_balance': np.random.uniform(10e6, 1000e6, n),
    'deposit_balance': np.random.uniform(20e6, 1500e6, n),
    'grant_amount': np.random.uniform(1e3, 500e3, n)  # in thousands
})

# Group and aggregate (sum) by region and year
df_grouped = df.groupby(['region', 'year'], as_index=False).sum()

# Pivot to MultiIndex format: index=year, columns=(metric, region)
df_pivot = df_grouped.pivot(index='year', columns='region', values=['loan_balance', 'deposit_balance', 'grant_amount'])

# Formatter functions (kept as-is)
def millions_formatter(x, pos):
    return f'{x / 1e6:.0f}'

def thousands_formatter(x, pos):
    return f'{x / 1e3:.0f}'

# --- 1. Put Year on X-Axis and include ALL regions ---
# Regions available (level 1 of columns now, since level 0 is metrics)
all_regions = df_pivot.columns.get_level_values(1).unique().tolist()  # Level 0: metrics, Level 1: regions
regions_to_use = [r for r in all_regions if r not in ['Total', 'Unmapped']]

# Year positions
years = df_pivot.index.values
n_years = len(years)
n_regions = len(regions_to_use)
x_year = np.arange(n_years)

# Build metric matrices shaped [n_regions, n_years]
# Columns in df_pivot are (metric, region)
loan_mat = np.vstack([df_pivot[('loan_balance', region)].values for region in regions_to_use])
deposit_mat = np.vstack([df_pivot[('deposit_balance', region)].values for region in regions_to_use])
giving_mat = np.vstack([df_pivot[('grant_amount', region)].values for region in regions_to_use])

# --- 3. Create the Visualization: Grouped bars by Region within each Year ---
fig, ax1 = plt.subplots(figsize=(16, 9))

# Layout math for grouped bars inside each year "cluster"
group_width = 0.85                 # total width allocated per year
region_slot = group_width / n_regions
bar_width = region_slot * 0.42     # two bars (loan/deposit) per region slot

# Colors: keep metric colors for bars; color lines by region
loan_color = 'royalblue'
deposit_color = 'skyblue'
cmap = plt.get_cmap('tab10')
region_colors = [cmap(i % 10) for i in range(n_regions)]

# Primary y-axis (balances, in millions)
for r, region in enumerate(regions_to_use):
    # left edge of this region's slot across all years
    slot_left = x_year - group_width/2 + r*region_slot + (region_slot - 2*bar_width)/2

    # Two bars per region: loan (left), deposit (right)
    ax1.bar(slot_left,            loan_mat[r],    width=bar_width, label='Loan Balance' if r == 0 else None,    color=loan_color)
    ax1.bar(slot_left + bar_width, deposit_mat[r], width=bar_width, label='Deposit Balance' if r == 0 else None, color=deposit_color)

ax1.set_xlabel('Year', fontsize=14)
ax1.set_ylabel('Balance (Millions)', fontsize=14)
ax1.set_xticks(x_year)
ax1.set_xticklabels(years)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.set_ylim(bottom=0)

# Secondary y-axis (foundation giving, in thousands), drawn as region-colored lines
ax2 = ax1.twinx()
for r, region in enumerate(regions_to_use):
    # center of the region slot (midpoint between the two bars)
    slot_left = x_year - group_width/2 + r*region_slot + (region_slot - 2*bar_width)/2
    centers = slot_left + bar_width/2
    ax2.plot(centers, giving_mat[r], linestyle='--', marker='o', linewidth=2, markersize=6,
             color=region_colors[r], label=region)

ax2.set_ylabel('Foundation Giving (Thousands)', color='green', fontsize=14)
ax2.tick_params(axis='y', labelcolor='green')
ax2.set_ylim(bottom=0)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))

# Title & legends
ax1.set_title(f'All Regions: Loan/Deposit vs. Foundation Giving ({years.min()}–{years.max()})', fontsize=18, pad=20)

# Two concise legends: one for metrics (bars) on the right
handles1, labels1 = ax1.get_legend_handles_labels()
leg1 = ax1.legend(handles1, labels1, title='Balances', loc='upper right')

# Regions legend (lines) across the top
handles2, labels2 = ax2.get_legend_handles_labels()
leg2 = ax2.legend(handles2, labels2, title='Regions (Giving)', loc='upper center',
                  ncol=min(n_regions, 5), bbox_to_anchor=(0.5, 1.12), frameon=False)

# Ensure both legends render
ax1.add_artist(leg1)

fig.tight_layout()

# --- 4. Write to PNG instead of showing a pop-up ---
outfile = f"regional_trend_all_regions_{years.min()}-{years.max()}.png"
plt.savefig(outfile, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"Chart saved as {outfile}")
