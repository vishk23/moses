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

# Regions to plot (exclude Unmapped)
regions_to_plot = [r for r in df_pivot.columns.get_level_values(0).unique() if r != 'Unmapped']

# --- Helpers & formatting ---
def fmt_millions(x, pos):
    return f'${x/1e6:.0f}M'

def fmt_thousands(x, pos):
    return f'${x/1e3:.0f}K'

def nice_grant_limits(series: pd.Series):
    """
    Compute a 'nice' Y range for grants (in raw USD), per region.
    - Finds min/max across available years (ignoring zeros if all zero -> fallback).
    - Adds a buffer by rounding down/up to a sensible step.
    """
    vals = series.dropna().values.astype(float)
    if len(vals) == 0 or np.all(vals == 0):
        return (0, 1)  # trivial safe default

    vmin, vmax = float(np.min(vals)), float(np.max(vals))
    if vmin == vmax:
        # If flat, give ±10% (min 50k) on each side
        buffer_amt = max(0.10 * vmax, 50_000.0)
        return (max(0.0, vmin - buffer_amt), vmax + buffer_amt)

    span = vmax - vmin
    # Choose a "nice" step from a limited set based on span
    candidates = np.array([25_000, 50_000, 100_000, 200_000, 250_000, 500_000, 1_000_000], dtype=float)
    target = span / 8.0  # aim for ~8 steps
    step = candidates[np.argmin(np.abs(candidates - target))]

    lower = max(0.0, step * floor((vmin - step) / step))   # one step below
    upper = step * ceil((vmax + step) / step)              # one step above
    # Ensure at least some span
    if upper - lower < step * 3:
        upper = lower + step * 3
    return (lower, upper)

# Colors
colors = {
    'loan_balance': '#1f77b4',     # Blue
    'deposit_balance': '#ff7f0e',  # Orange
    'grant_amount': '#2ca02c',     # Green
}

# X-axis categories
x_years = df_pivot.index.tolist()

# --- Per-region figures ---
for region in regions_to_plot:
    # Pull series (safe reindex in case of missing)
    loans = df_pivot.get((region, 'loan_balance'), pd.Series(0, index=x_years)).reindex(x_years).fillna(0.0)
    deposits = df_pivot.get((region, 'deposit_balance'), pd.Series(0, index=x_years)).reindex(x_years).fillna(0.0)
    grants = df_pivot.get((region, 'grant_amount'), pd.Series(0, index=x_years)).reindex(x_years).fillna(0.0)

    # Create figure for this region
    fig, ax = plt.subplots(figsize=(10, 6))

    # Primary axis: loans & deposits
    line_loan, = ax.plot(x_years, loans, label='Loan Balance', color=colors['loan_balance'], marker='o', linewidth=2)
    line_dep,  = ax.plot(x_years, deposits, label='Deposit Balance', color=colors['deposit_balance'], marker='s', linewidth=2)
    ax.set_ylabel('Balance (Millions)', fontsize=12, fontweight='bold', color='gray')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_millions))
    ax.tick_params(axis='y', labelcolor='gray')
    ax.set_xticks(x_years)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')

    # Secondary axis: grants
    ax2 = ax.twinx()
    line_grant, = ax2.plot(
        x_years, grants,
        label='Grants Awarded',
        color=colors['grant_amount'],
        linestyle='--', marker='o', markersize=6, linewidth=2
    )
    ax2.set_ylabel('Grant Amount (Thousands)', fontsize=12, fontweight='bold', color=colors['grant_amount'])
    ax2.tick_params(axis='y', labelcolor=colors['grant_amount'])
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_thousands))

    # Dynamic per-region Y range for grants with buffer
    gmin, gmax = nice_grant_limits(grants)
    ax2.set_ylim(gmin, gmax)

    # Title
    ax.set_title(f'{region}: Loan/Deposit vs. Grant Giving (2020–2024)', fontsize=16, fontweight='bold', pad=10)

    # Legend OUTSIDE the axes, bottom-right of the figure
    handles = [line_loan, line_dep, line_grant]
    labels = ['Loan Balance', 'Deposit Balance', 'Grants Awarded']
    fig.legend(
        handles, labels,
        loc='lower right', bbox_to_anchor=(0.98, 0.02),
        frameon=False, ncol=1, handlelength=2, handletextpad=0.6, borderaxespad=0.2
    )

    # Layout: reserve a bit of right/bottom margin for the outside legend
    plt.tight_layout(rect=[0.05, 0.08, 0.92, 0.95])

    # Safe filename
    safe_region = (
        region.lower()
        .replace('&', 'and')
        .replace('/', '_')
        .replace(' ', '')
        .replace('-', '_')
    )
    out_path = f'regional_financial_trends_{safe_region}.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# If you want to confirm outputs visually, uncomment the following line for any single region run:
# plt.show()

