
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# --- Data ---
# Years & regions covered by the actuals
years = [2020, 2021, 2022, 2023, 2024]
regions = ['Rhode Island', 'Southcoast', 'Attleboro/Taunton', 'Other', 'Unmapped']

# Deposit actuals by year/region
deposit_data = {
    2020: {
        'Attleboro/Taunton': 1608615918.92,
        'Southcoast': 439192149.71999997,
        'Rhode Island': 235707727.13,
        'Other': 0.0,
        'Unmapped': 0.0,
    },
    2021: {
        'Attleboro/Taunton': 1750593658.56,
        'Southcoast': 486256425.48,
        'Rhode Island': 258077676.75,
        'Other': 0.0,
        'Unmapped': 0.0,
    },
    2022: {
        'Attleboro/Taunton': 1594936398.93,
        'Southcoast': 552267175.18,
        'Rhode Island': 252917537.29,
        'Other': 0.0,
        'Unmapped': 0.0,
    },
    2023: {
        'Attleboro/Taunton': 1691537612.21,
        'Southcoast': 534343926.29,
        'Rhode Island': 225298440.06,
        'Other': 0.0,
        'Unmapped': 0.0,
    },
    2024: {
        'Attleboro/Taunton': 1674127115.5,
        'Southcoast': 590446754.03,
        'Rhode Island': 232130668.73,
        'Other': 12461416.18,
        'Unmapped': 0.0,
    },
}

# Loan actuals by year/region
loan_data = {
    2020: {
        'Attleboro/Taunton': 1106631023.65,
        'Southcoast': 581232890.97,
        'Rhode Island': 441419753.47,
        'Other': 22018220.13,
        'Unmapped': 0.0,
    },
    2021: {
        'Attleboro/Taunton': 1076544087.11,
        'Southcoast': 588273517.84,
        'Rhode Island': 411824181.72,
        'Other': 13998442.81,
        'Unmapped': 0.0,
    },
    2022: {
        'Attleboro/Taunton': 1253226462.19,
        'Southcoast': 623830340.89,
        'Rhode Island': 444093307.37,
        'Other': 11570979.59,
        'Unmapped': 0.0,
    },
    2023: {
        'Attleboro/Taunton': 1284501915.5,
        'Southcoast': 640067641.46,
        'Rhode Island': 420613579.39,
        'Other': 15358963.25,
        'Unmapped': 0.0,
    },
    2024: {
        'Attleboro/Taunton': 1362871747.8799999,
        'Southcoast': 659063602.77,
        'Rhode Island': 418885502.08,
        'Other': 14168398.56,
        'Unmapped': 0.0,
    },
}

# Grant actuals by year/region (USD)
grant_data = {
    2020: {
        'Attleboro/Taunton': 881398.00,
        'Southcoast': 933728.84,
        'Rhode Island': 261250.00,
        'Other': 115500.00,
        'Unmapped': 0.0,
    },
    2021: {
        'Attleboro/Taunton': 815706.67,
        'Southcoast': 791106.23,
        'Rhode Island': 244000.00,
        'Other': 98171.76,
        'Unmapped': 0.0,
    },
    2022: {
        'Attleboro/Taunton': 868427.68,
        'Southcoast': 1162538.61,
        'Rhode Island': 314615.00,
        'Other': 77000.00,
        'Unmapped': 0.0,
    },
    2023: {
        'Attleboro/Taunton': 776439.66,
        'Southcoast': 975260.36,
        'Rhode Island': 356715.00,
        'Other': 40800.00,
        'Unmapped': 0.0,
    },
    2024: {
        'Attleboro/Taunton': 909814.80,
        'Southcoast': 1183795.00,
        'Rhode Island': 636957.00,
        'Other': 128550.00,
        'Unmapped': 0.0,
    },
}

# Build the consolidated DataFrame and pivot to match the rest of the script
data = []
for y in years:
    for r in regions:
        data.append({
            'year': y,
            'region': r,
            'loan_balance': float(loan_data.get(y, {}).get(r, 0.0)),
            'deposit_balance': float(deposit_data.get(y, {}).get(r, 0.0)),
            'grant_amount': float(grant_data.get(y, {}).get(r, 0.0)),
        })

df_consolidated = pd.DataFrame(data)
df_pivot = df_consolidated.pivot_table(
    index='year',
    columns='region',
    values=['loan_balance', 'deposit_balance', 'grant_amount']
)
df_pivot = df_pivot.swaplevel(0, 1, axis=1).sort_index(axis=1)

# --- END DATA SECTION ---
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

# For a single, global legend (collect handles once)
legend_handles, legend_labels = None, None

# Plot per region
for i, region in enumerate(regions_to_plot):
    ax = axes[i]

    # Safely pull series; fill missing with 0 to avoid plotting errors if any gaps
    loan_values = df_pivot.get((region, 'loan_balance'), pd.Series(0, index=years)).reindex(years).fillna(0)
    deposit_values = df_pivot.get((region, 'deposit_balance'), pd.Series(0, index=years)).reindex(years).fillna(0)
    grant_values = df_pivot.get((region, 'grant_amount'), pd.Series(0, index=years)).reindex(years).fillna(0)

    # Primary axis: loan & deposit
    line_loan, = ax.plot(years, loan_values, label='Loan Balance', color=colors['loan_balance'], marker='o', linewidth=2)
    line_deposit, = ax.plot(years, deposit_values, label='Deposit Balance', color=colors['deposit_balance'], marker='s', linewidth=2)

    ax.set_ylabel('Balance (Millions)', fontsize=12, fontweight='bold', color='gray')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
    ax.tick_params(axis='y', labelcolor='gray')

    # Secondary axis: grants
    ax2 = ax.twinx()
    line_grant, = ax2.plot(years, grant_values, label='Grants Awarded', color=colors['grant_amount'],
                           linestyle='--', marker='o', markersize=6, linewidth=2)

    ax2.set_ylabel('Grant Amount (Thousands)', color=colors['grant_amount'], fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=colors['grant_amount'])
    ax2.set_ylim(bottom=0)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))

    # Titles & ticks
    ax.set_title(region, fontsize=14, fontweight='bold')
    ax.set_xticks(years)

    # Collect legend handles from the first subplot only
    if i == 0:
        legend_handles = [line_loan, line_deposit, line_grant]
        legend_labels = ['Loan Balance', 'Deposit Balance', 'Grants Awarded']

# Remove any unused subplots
for i in range(num_regions, nrows * ncols):
    fig.delaxes(axes[i])

# Global labels & title
fig.text(0.5, 0.04, 'Year', ha='center', fontsize=14, fontweight='bold')
fig.suptitle('Annual Loan/Deposit Growth vs. Grant Giving by Region', fontsize=20, fontweight='bold', y=0.99)

# Single, compact global legend at the top
if legend_handles is not None:
    fig.legend(legend_handles, legend_labels,
               loc='upper center', bbox_to_anchor=(0.5, 0.965),
               ncol=3, frameon=False, fontsize=11,
               handlelength=2, handletextpad=0.6, borderaxespad=0.2)

# Layout & save (leave room at the top for the legend and title)
plt.tight_layout(rect=[0, 0.03, 1, 0.92])
plt.savefig('regional_financial_trends.png', dpi=300, bbox_inches='tight')
# plt.show()  # Uncomment to display interactively

