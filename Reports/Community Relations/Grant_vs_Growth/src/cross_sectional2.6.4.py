import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from math import floor, ceil

# ------------------------------------------------------------
# Drop-in script to generate one PNG per region
# using the ACTUAL data provided in the prompt.
#
# Changes vs. your previous version:
# - Deposits and Loans updated to your new 2020–2024 totals.
# - Regions list preserved; "Unmapped" remains but is zero-filled.
# - Creates a separate PNG for each region (no subplots grid).
# - Grants (right Y axis) use a dynamic per-region range with a buffered min/max.
# - Single, figure-level legend placed at the bottom-right OUTSIDE the plot.
# ------------------------------------------------------------

# --- Data (ACTUALS) ---
years = [2020, 2021, 2022, 2023, 2024]
regions = ['Attleboro/Taunton', 'South Coast', 'Rhode Island', 'Other', 'Unmapped']

# Deposits by year/region (UPDATED TOTALS)
deposit_data = {
    2020: {
        'Attleboro/Taunton': 1283329351.36,
        'South Coast': 390332232.38,
        'Rhode Island': 274046931.20,
        'Other': 335807280.83,
        'Unmapped': 0.0,
    },
    2021: {
        'Attleboro/Taunton': 1354851013.02,
        'South Coast': 430208218.07,
        'Rhode Island': 297490407.67,
        'Other': 412378122.03,
        'Unmapped': 0.0,
    },
    2022: {
        'Attleboro/Taunton': 1234648743.59,
        'South Coast': 506933511.90,
        'Rhode Island': 272669870.47,
        'Other': 385868985.44,
        'Unmapped': 0.0,
    },
    2023: {
        'Attleboro/Taunton': 1344039693.32,
        'South Coast': 484917908.16,
        'Rhode Island': 249830466.05,
        'Other': 372391911.03,
        'Unmapped': 0.0,
    },
    2024: {
        'Attleboro/Taunton': 1293358041.54,
        'South Coast': 518602757.96,
        'Rhode Island': 268775299.16,
        'Other': 428429855.78,
        'Unmapped': 0.0,
    },
}

# Loans by year/region (UPDATED TOTALS)
loan_data = {
    2020: {
        'Attleboro/Taunton': 561706669.78,
        'South Coast': 386954559.43,
        'Rhode Island': 531009913.66,
        'Other': 671630745.35,
        'Unmapped': 0.0,
    },
    2021: {
        'Attleboro/Taunton': 508184138.72,
        'South Coast': 385354495.65,
        'Rhode Island': 537998738.38,
        'Other': 659102856.73,
        'Unmapped': 0.0,
    },
    2022: {
        'Attleboro/Taunton': 527476376.64,
        'South Coast': 434047540.88,
        'Rhode Island': 629057054.01,
        'Other': 742140118.51,
        'Unmapped': 0.0,
    },
    2023: {
        'Attleboro/Taunton': 508956474.41,
        'South Coast': 441558622.19,
        'Rhode Island': 604175380.77,
        'Other': 805851622.23,
        'Unmapped': 0.0,
    },
    2024: {
        'Attleboro/Taunton': 500647400.35,
        'South Coast': 478482385.33,
        'Rhode Island': 623901471.37,
        'Other': 851957994.24,
        'Unmapped': 0.0,
    },
}

# Grants by year/region (USD) — unchanged
grant_data = {
    2020: {
        'Attleboro/Taunton': 881398.00,
        'South Coast': 933728.84,
        'Rhode Island': 261250.00,
        'Other': 115500.00,
        'Unmapped': 0.0,
    },
    2021: {
        'Attleboro/Taunton': 815706.67,
        'South Coast': 791106.23,
        'Rhode Island': 244000.00,
        'Other': 98171.76,
        'Unmapped': 0.0,
    },
    2022: {
        'Attleboro/Taunton': 868427.68,
        'South Coast': 1162538.61,
        'Rhode Island': 314615.00,
        'Other': 77000.00,
        'Unmapped': 0.0,
    },
    2023: {
        'Attleboro/Taunton': 776439.66,
        'South Coast': 975260.36,
        'Rhode Island': 356715.00,
        'Other': 40800.00,
        'Unmapped': 0.0,
    },
    2024: {
        'Attleboro/Taunton': 909814.80,
        'South Coast': 1183795.00,
        'Rhode Island': 636957.00,
        'Other': 128550.00,
        'Unmapped': 0.0,
    },
}

# Build the consolidated DataFrame and pivot to match the plotting code
rows = []
for y in years:
    for r in regions:
        rows.append({
            'year': y,
            'region': r,
            'loan_balance': float(loan_data.get(y, {}).get(r, 0.0)),
            'deposit_balance': float(deposit_data.get(y, {}).get(r, 0.0)),
            'grant_amount': float(grant_data.get(y, {}).get(r, 0.0)),
        })

df = pd.DataFrame(rows)
df_pivot = df.pivot_table(
    index='year',
    columns='region',
    values=['loan_balance', 'deposit_balance', 'grant_amount']
)
df_pivot = df_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)


# Regions to compare (exclude Unmapped)
regions_to_plot = [r for r in df_pivot.columns.get_level_values(0).unique() if r != 'Unmapped']
x_years = df_pivot.index.tolist()

# Formatters
def fmt_millions(x, pos): return f'${x/1e6:.0f}M'
def fmt_thousands(x, pos): return f'${x/1e3:.0f}K'

# --- Plot 1: Loans across regions ---
fig1, ax1 = plt.subplots(figsize=(12, 7))
for region in regions_to_plot:
    y = df_pivot.get((region, 'loan_balance'), pd.Series(0, index=x_years)).reindex(x_years).fillna(0.0)
    ax1.plot(x_years, y, marker='o', linewidth=2, label=region)
ax1.set_title('Loans by Region (2020–2024)')
ax1.set_xlabel('Year')
ax1.set_ylabel('Balance (Millions)')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
ax1.set_xticks(x_years)
ax1.legend(ncol=2, fontsize=9)
plt.tight_layout()
plt.savefig('loans_across_regions.png', dpi=300, bbox_inches='tight')
plt.close(fig1)

# --- Plot 2: Deposits across regions ---
fig2, ax2 = plt.subplots(figsize=(12, 7))
for region in regions_to_plot:
    y = df_pivot.get((region, 'deposit_balance'), pd.Series(0, index=x_years)).reindex(x_years).fillna(0.0)
    ax2.plot(x_years, y, marker='o', linewidth=2, label=region)
ax2.set_title('Deposits by Region (2020–2024)')
ax2.set_xlabel('Year')
ax2.set_ylabel('Balance (Millions)')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
ax2.set_xticks(x_years)
ax2.legend(ncol=2, fontsize=9)
plt.tight_layout()
plt.savefig('deposits_across_regions.png', dpi=300, bbox_inches='tight')
plt.close(fig2)

# --- Plot 3: Giving (Grants) across regions ---
fig3, ax3 = plt.subplots(figsize=(12, 7))
for region in regions_to_plot:
    y = df_pivot.get((region, 'grant_amount'), pd.Series(0, index=x_years)).reindex(x_years).fillna(0.0)
    ax3.plot(x_years, y, marker='o', linewidth=2, label=region)
ax3.set_title('Giving (Grants) by Region (2020–2024)')
ax3.set_xlabel('Year')
ax3.set_ylabel('Grant Amount (Thousands)')
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_thousands))
ax3.set_xticks(x_years)
ax3.legend(ncol=2, fontsize=9)
plt.tight_layout()
plt.savefig('grants_across_regions.png', dpi=300, bbox_inches='tight')
plt.close(fig3)
# If you want to confirm outputs visually, uncomment the following line for any single region run:
# plt.show()

