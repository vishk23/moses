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

# Regions to plot (exclude 'Unmapped') - expect 4 regions
regions_all = df_pivot.columns.get_level_values(0).unique().tolist()
regions_to_plot = [r for r in regions_all if r != 'Unmapped'][:4]

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

# Precompute global max for consistent y-scales across subplots
primary_vals = []
grant_vals = []
for r in regions_to_plot:
    primary_vals.extend(df_pivot.loc[years, (r, 'loan_balance')].values.tolist())
    primary_vals.extend(df_pivot.loc[years, (r, 'deposit_balance')].values.tolist())
    grant_vals.extend(df_pivot.loc[years, (r, 'grant_amount')].values.tolist())

ymax_primary = max(primary_vals) * 1.15 if primary_vals else 1
ymax_grants = max(grant_vals) * 1.25 if grant_vals else 1

# --- Figure with 4 subplots (one per region) ---
fig, axes = plt.subplots(2, 2, figsize=(18, 10), sharex=False)
axes = axes.flatten()

centers = np.arange(len(years))
bar_width = 0.25

legend_patches = [
    Patch(facecolor=colors['loan_balance'], label='Loans'),
    Patch(facecolor=colors['deposit_balance'], label='Deposits'),
    Patch(facecolor=colors['grant_amount'], label='Grants')
]

for ax, region in zip(axes, regions_to_plot):
    # Extract series for this region
    L_vals = df_pivot.loc[years, (region, 'loan_balance')].values
    D_vals = df_pivot.loc[years, (region, 'deposit_balance')].values
    G_vals = df_pivot.loc[years, (region, 'grant_amount')].values

    # Positions for grouped bars per year
    pos_L = centers - bar_width
    pos_D = centers
    pos_G = centers + bar_width

    # Primary axis (Loans & Deposits)
    ax.bar(pos_L, L_vals, width=bar_width, color=colors['loan_balance'], label='Loans', zorder=3)
    ax.bar(pos_D, D_vals, width=bar_width, color=colors['deposit_balance'], label='Deposits', zorder=3)

    # Secondary axis (Grants)
    ax_g = ax.twinx()
    ax_g.bar(pos_G, G_vals, width=bar_width, color=colors['grant_amount'], label='Grants', alpha=0.95, zorder=2)

    # Formatting y-axes
    ax.set_ylabel('Loans & Deposits (Millions)', fontsize=11, color='gray', fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
    ax.tick_params(axis='y', labelcolor='gray')
    ax.set_ylim(0, ymax_primary)

    ax_g.set_ylabel('Grants (Thousands)', fontsize=11, color=colors['grant_amount'], fontweight='bold')
    ax_g.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))
    ax_g.tick_params(axis='y', labelcolor=colors['grant_amount'])
    ax_g.set_ylim(0, ymax_grants)

    # X-axis tick labels (years)
    ax.set_xticks(centers)
    ax.set_xticklabels([str(y) for y in years], fontsize=10)
    ax.set_xlabel('Year', fontsize=11, fontweight='bold')

    # Optional top axis mirroring years for readability
    ax_top = ax.secondary_xaxis('top', functions=(lambda u: u, lambda u: u))
    ax_top.set_xticks(centers)
    ax_top.set_xticklabels([str(y) for y in years], fontsize=10, fontweight='bold')
    ax_top.set_xlabel('Year', fontsize=11, fontweight='bold')

    # Light alternating year shading to reduce visual clutter
    for i in range(len(years)):
        if i % 2 == 0:
            ax.axvspan(i - 0.5, i + 0.5, color='0.96', zorder=0)

    # Grid (primary y only)
    ax.grid(axis='y', linestyle='-', linewidth=0.5, color='0.9')
    ax.set_axisbelow(True)

    # Title per subplot
    ax.set_title(region, fontsize=14, fontweight='bold')

# If fewer than 4 regions for any reason, remove extra axes
for j in range(len(regions_to_plot), 4):
    fig.delaxes(axes[j])

# Figure-level legend (single, not repeated on each subplot)
fig.legend(handles=legend_patches, loc='lower center', ncol=3, frameon=False, fontsize=11, bbox_to_anchor=(0.5, 0.00))

# Title and layout
fig.suptitle('Loans, Deposits, and Grants by Year — Regional View (4 Subplots)', fontsize=18, fontweight='bold')
plt.tight_layout(rect=[0, 0.04, 1, 0.95])

# Save (no display)
plt.savefig('year_region_financials_4_subplots.png', dpi=300, bbox_inches='tight')
plt.close(fig)

