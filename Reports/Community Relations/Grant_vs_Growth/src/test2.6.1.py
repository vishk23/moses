import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# =====================================================================
# === DATA ENTRY (full $ amounts; replace these with your actuals) ====
# =====================================================================
# Add one row per (year, region) with full-dollar amounts.
# Regions expected: 'Rhode Island', 'Southcoast', 'Attleboro/Taunton', 'Other', 'Unmapped'
# Years shown as an example: 2022–2024 (extend by adding more rows if needed).
data_rows = [
    # ---------- 2022 ----------
    {"year": 2022, "region": "Rhode Island",       "loan_balance": 520_000_000, "deposit_balance": 950_000_000,  "grant_amount": 1_100_000},
    {"year": 2022, "region": "Southcoast",         "loan_balance": 410_000_000, "deposit_balance": 720_000_000,  "grant_amount":   800_000},
    {"year": 2022, "region": "Attleboro/Taunton",  "loan_balance": 280_000_000, "deposit_balance": 480_000_000,  "grant_amount":   600_000},
    {"year": 2022, "region": "Other",              "loan_balance": 150_000_000, "deposit_balance": 300_000_000,  "grant_amount":   300_000},
    {"year": 2022, "region": "Unmapped",           "loan_balance":  40_000_000, "deposit_balance":  90_000_000,  "grant_amount":   100_000},

    # ---------- 2023 ----------
    {"year": 2023, "region": "Rhode Island",       "loan_balance": 552_000_000, "deposit_balance": 1_026_000_000, "grant_amount": 1_200_000},
    {"year": 2023, "region": "Southcoast",         "loan_balance": 435_000_000, "deposit_balance":   778_000_000, "grant_amount":   900_000},
    {"year": 2023, "region": "Attleboro/Taunton",  "loan_balance": 300_000_000, "deposit_balance":   518_000_000, "grant_amount":   650_000},
    {"year": 2023, "region": "Other",              "loan_balance": 165_000_000, "deposit_balance":   324_000_000, "grant_amount":   350_000},
    {"year": 2023, "region": "Unmapped",           "loan_balance":  42_000_000, "deposit_balance":    95_000_000, "grant_amount":   110_000},

    # ---------- 2024 ----------
    {"year": 2024, "region": "Rhode Island",       "loan_balance": 585_000_000, "deposit_balance": 1_108_000_000, "grant_amount": 1_350_000},
    {"year": 2024, "region": "Southcoast",         "loan_balance": 460_000_000, "deposit_balance":   840_000_000, "grant_amount": 1_000_000},
    {"year": 2024, "region": "Attleboro/Taunton",  "loan_balance": 320_000_000, "deposit_balance":   560_000_000, "grant_amount":   700_000},
    {"year": 2024, "region": "Other",              "loan_balance": 180_000_000, "deposit_balance":   350_000_000, "grant_amount":   400_000},
    {"year": 2024, "region": "Unmapped",           "loan_balance":  45_000_000, "deposit_balance":   100_000_000, "grant_amount":   120_000},
]
# =====================================================================
# === END DATA ENTRY ===================================================
# =====================================================================

# Build DataFrame from the data-entry rows
df_consolidated = pd.DataFrame(data_rows)

# Pivot to wide format: multi-index columns (region, metric)
df_pivot = df_consolidated.pivot_table(
    index='year',
    columns='region',
    values=['loan_balance', 'deposit_balance', 'grant_amount'],
    aggfunc='sum'  # if duplicates exist, they'll be summed
)

# Reorder the multiindex to (region, metric) for easier slicing
df_pivot = df_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)

# Determine regions to plot (exclude 'Unmapped' from visuals)
regions_to_plot = [col for col in df_pivot.columns.get_level_values(0).unique() if col not in ['Unmapped']]

# Grid layout based on number of regions
num_regions = len(regions_to_plot)
nrows = int(np.ceil(np.sqrt(num_regions)))
ncols = int(np.ceil(num_regions / nrows))

# Initialize subplots
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 12), sharex=True)
# Ensure axes is iterable even if only one subplot
if num_regions == 1:
    axes = np.array([axes])
axes = axes.flatten()

# X-axis years
years = df_pivot.index

# Currency formatters
def millions_formatter(x, pos):
    return f'${x / 1e6:.0f}M'

def thousands_formatter(x, pos):
    return f'${x / 1e3:.0f}K'

# Professional color palette
colors = {
    'loan_balance': '#1f77b4',   # Blue
    'deposit_balance': '#ff7f0e',# Orange
    'grant_amount': '#2ca02c'    # Green
}

# Plot per region
for i, region in enumerate(regions_to_plot):
    ax = axes[i]

    # Safely pull series; fill missing with 0 to avoid plotting errors if any gaps
    loan_values = df_pivot.get((region, 'loan_balance'), pd.Series(0, index=years)).reindex(years).fillna(0)
    deposit_values = df_pivot.get((region, 'deposit_balance'), pd.Series(0, index=years)).reindex(years).fillna(0)
    grant_values = df_pivot.get((region, 'grant_amount'), pd.Series(0, index=years)).reindex(years).fillna(0)

    # Primary axis: loan & deposit
    ax.plot(years, loan_values, label='Loan Balance', color=colors['loan_balance'], marker='o', linewidth=2)
    ax.plot(years, deposit_values, label='Deposit Balance', color=colors['deposit_balance'], marker='s', linewidth=2)

    ax.set_ylabel('Balance (Millions)', fontsize=12, fontweight='bold', color='gray')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
    ax.tick_params(axis='y', labelcolor='gray')

    # Secondary axis: grants
    ax2 = ax.twinx()
    ax2.plot(years, grant_values, label='Grants Awarded', color=colors['grant_amount'],
             linestyle='--', marker='o', markersize=6, linewidth=2)

    ax2.set_ylabel('Grant Amount (Thousands)', color=colors['grant_amount'], fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=colors['grant_amount'])
    ax2.set_ylim(bottom=0)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))

    # Titles & ticks
    ax.set_title(region, fontsize=14, fontweight='bold')
    ax.set_xticks(years)

    # Combined legend
    lines, labels_line = ax.get_legend_handles_labels()
    lines2, labels2_line = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels_line + labels2_line, loc='upper left', frameon=False)

# Remove any unused subplots
for i in range(num_regions, nrows * ncols):
    fig.delaxes(axes[i])

# Global labels & title
fig.text(0.5, 0.04, 'Year', ha='center', fontsize=14, fontweight='bold')
fig.suptitle('Annual Loan/Deposit Growth vs. Grant Giving by Region', fontsize=20, fontweight='bold')

# Layout & save
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('regional_financial_trends.png', dpi=300, bbox_inches='tight')
# plt.show()  # Uncomment to display interactively

