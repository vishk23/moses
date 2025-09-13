
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Patch

# --- Adjusted data creation for 2022-2024 and new regions ---
years = [2022, 2023, 2024]
regions = ['Rhode Island', 'Southcoast', 'Attleboro/Taunton', 'Other', 'Unmapped']
data = []
for year in years:
    for region in regions:
        data.append({
            'year': year,
            'region': region,
            'loan_balance': np.random.uniform(250e6, 800e6) * (1 + (year-2022)*0.06),
            'deposit_balance': np.random.uniform(400e6, 1200e6) * (1 + (year-2022)*0.08),
            'grant_amount': np.random.uniform(0.5e6, 2e6) * (1 + (year-2022)*0.1)
        })
df_consolidated = pd.DataFrame(data)

# Pivot for easy lookup
df_pivot = (
    df_consolidated
    .pivot_table(index='year', columns='region',
                 values=['loan_balance', 'deposit_balance', 'grant_amount'], aggfunc='sum')
    .swaplevel(0, 1, axis=1)
    .sort_index(axis=1)
)

# Regions to use (exclude 'Unmapped')
regions_all = df_pivot.columns.get_level_values(0).unique().tolist()
regions_to_plot = [r for r in regions_all if r != 'Unmapped']

# --- Helpers for formatting ---
def millions_formatter(x, pos):
    return f'${x/1e6:.0f}M'

def thousands_formatter(x, pos):
    return f'${x/1e3:.0f}K'

colors = {
    'loan_balance': '#1f77b4',   # Loans
    'deposit_balance': '#ff7f0e',# Deposits
    'grant_amount': '#2ca02c'    # Grants
}

# --- Build hierarchical x positions: Year -> Region (per year) -> 3 bars (L/D/G) ---
bar_width = 0.22
region_gap = 0.18
year_gap = 0.7

positions_loan = []
positions_deposit = []
positions_grant = []
heights_loan = []
heights_deposit = []
heights_grant = []

region_tick_positions = []
region_tick_labels = []

year_centers = []
year_boundaries = []

x = 0.0
for y in years:
    year_start = x
    for r in regions_to_plot:
        # Heights
        L = df_pivot.loc[y, (r, 'loan_balance')]
        D = df_pivot.loc[y, (r, 'deposit_balance')]
        G = df_pivot.loc[y, (r, 'grant_amount')]

        # Bar positions within this region group
        pos_L = x
        pos_D = x + bar_width
        pos_G = x + 2*bar_width

        positions_loan.append(pos_L)
        positions_deposit.append(pos_D)
        positions_grant.append(pos_G)

        heights_loan.append(L)
        heights_deposit.append(D)
        heights_grant.append(G)

        # Region tick centered under the 3 bars
        region_center = x + 1.5*bar_width
        region_tick_positions.append(region_center)
        region_tick_labels.append(r)

        # Advance to next region group
        x += 3*bar_width + region_gap

    # Compute and store year center & boundaries
    year_end = x - region_gap  # last increment added region_gap; back off for end boundary
    year_centers.append((year_start + year_end) / 2)
    year_boundaries.append((year_start, year_end))

    # Gap between years
    x += year_gap

# Axis limits
xmin = year_boundaries[0][0] - bar_width
xmax = year_boundaries[-1][1] + year_gap*0.35

# --- Create single chart with dual y-axes ---
fig, ax = plt.subplots(figsize=(18, 9))
ax_g = ax.twinx()  # grants axis

# Primary axis (Loans & Deposits)
bars_L = ax.bar(positions_loan, heights_loan, width=bar_width, color=colors['loan_balance'], label='Loans', zorder=3)
bars_D = ax.bar(positions_deposit, heights_deposit, width=bar_width, color=colors['deposit_balance'], label='Deposits', zorder=3)

# Secondary axis (Grants)
bars_G = ax_g.bar(positions_grant, heights_grant, width=bar_width, color=colors['grant_amount'], label='Grants', alpha=0.9, zorder=2)

# Y-axis formatting
ax.set_ylabel('Loans & Deposits (Millions)', fontsize=12, fontweight='bold', color='gray')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
ax.tick_params(axis='y', labelcolor='gray')

ax_g.set_ylabel('Grants (Thousands)', fontsize=12, fontweight='bold', color=colors['grant_amount'])
ax_g.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))
ax_g.tick_params(axis='y', labelcolor=colors['grant_amount'])

# Harmonize primary y-limit for clarity across loans/deposits
ymax_primary = max(max(heights_loan), max(heights_deposit))
ax.set_ylim(0, ymax_primary * 1.15)
ax_g.set_ylim(0, max(heights_grant) * 1.25)

# X-axis labeling:
#   - Bottom axis: regions (repeated within each year)
ax.set_xlim(xmin, xmax)
ax.set_xticks(region_tick_positions)
ax.set_xticklabels(region_tick_labels, fontsize=10)
ax.set_xlabel('Region (within each Year)', fontsize=12, fontweight='bold')

#   - Top axis: years centered across each year block
ax_year = ax.secondary_xaxis('top', functions=(lambda u: u, lambda u: u))
ax_year.set_xticks(year_centers)
ax_year.set_xticklabels([str(y) for y in years], fontsize=12, fontweight='bold')
ax_year.set_xlabel('Year', fontsize=12, fontweight='bold')

# Light alternating shading to visually separate year groups
for i, (ystart, yend) in enumerate(year_boundaries):
    if i % 2 == 0:
        ax.axvspan(ystart - bar_width*0.3, yend + bar_width*0.3, color='0.95', zorder=0)

# Vertical separators at year boundaries
for (ystart, yend) in year_boundaries:
    ax.axvline(ystart - region_gap*0.5, color='0.85', linewidth=1, zorder=1)
    ax.axvline(yend + region_gap*0.5, color='0.85', linewidth=1, zorder=1)

# Grid (y only, primary)
ax.grid(axis='y', linestyle='-', linewidth=0.5, color='0.9')
ax.set_axisbelow(True)

# Legend (single, color-coded by series)
legend_patches = [
    Patch(facecolor=colors['loan_balance'], label='Loans'),
    Patch(facecolor=colors['deposit_balance'], label='Deposits'),
    Patch(facecolor=colors['grant_amount'], label='Grants')
]
ax.legend(handles=legend_patches, loc='upper left', ncol=3, frameon=False, fontsize=11)

# Title and layout
fig.suptitle('Loans, Deposits, and Grants by Year and Region', fontsize=18, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save (no display)
plt.savefig('year_region_financials_single_chart.png', dpi=300, bbox_inches='tight')
plt.close(fig)

