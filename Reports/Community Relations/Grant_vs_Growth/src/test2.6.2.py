import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import re

# --- Data (corrected & normalized) ---
years = [2020, 2021, 2022, 2023, 2024]
regions = ['Attleboro/Taunton', 'South Coast', 'Rhode Island', 'Other']  # normalized names

# Deposit actuals by year/region
deposit_data = {
    2020: {
        'Attleboro/Taunton': 1608615918.92,
        'South Coast': 439192149.71999997,
        'Rhode Island': 235707727.13,
        'Other': 0.0,
    },
    2021: {
        'Attleboro/Taunton': 1750593658.56,
        'South Coast': 486256425.48,
        'Rhode Island': 258077676.75,
        'Other': 0.0,
    },
    2022: {
        'Attleboro/Taunton': 1594936398.93,
        'South Coast': 552267175.18,
        'Rhode Island': 252917537.29,
        'Other': 0.0,
    },
    2023: {
        'Attleboro/Taunton': 1691537612.21,
        'South Coast': 534343926.29,
        'Rhode Island': 225298440.06,
        'Other': 0.0,
    },
    2024: {
        'Attleboro/Taunton': 1686588531.68,  # updated per actuals
        'South Coast': 590446754.03,
        'Rhode Island': 232130668.73,
        'Other': 0.0,  # corrected to 0.0 per actuals
    },
}

# Loan actuals by year/region
loan_data = {
    2020: {
        'Attleboro/Taunton': 1106631023.65,
        'South Coast': 581232890.97,
        'Rhode Island': 441419753.47,
        'Other': 22018220.13,
    },
    2021: {
        'Attleboro/Taunton': 1076544087.11,
        'South Coast': 588273517.84,
        'Rhode Island': 411824181.72,
        'Other': 13998442.81,
    },
    2022: {
        'Attleboro/Taunton': 1253226462.19,
        'South Coast': 623830340.89,
        'Rhode Island': 444093307.37,
        'Other': 11570979.59,
    },
    2023: {
        'Attleboro/Taunton': 1284501915.5,
        'South Coast': 640067641.46,
        'Rhode Island': 420613579.39,
        'Other': 15358963.25,
    },
    2024: {
        'Attleboro/Taunton': 1362871747.8799999,
        'South Coast': 659063602.77,
        'Rhode Island': 418885502.08,
        'Other': 14168398.56,
    },
}

# Grant actuals by year/region (USD)
grant_data = {
    2020: {
        'Attleboro/Taunton': 881398.00,
        'South Coast': 933728.84,
        'Rhode Island': 261250.00,
        'Other': 115500.00,
    },
    2021: {
        'Attleboro/Taunton': 815706.67,
        'South Coast': 791106.23,
        'Rhode Island': 244000.00,
        'Other': 98171.76,
    },
    2022: {
        'Attleboro/Taunton': 868427.68,
        'South Coast': 1162538.61,
        'Rhode Island': 314615.00,
        'Other': 77000.00,
    },
    2023: {
        'Attleboro/Taunton': 776439.66,
        'South Coast': 975260.36,
        'Rhode Island': 356715.00,
        'Other': 40800.00,
    },
    2024: {
        'Attleboro/Taunton': 909814.80,
        'South Coast': 1183795.00,
        'Rhode Island': 636957.00,
        'Other': 128550.00,
    },
}

# Build consolidated DataFrame & pivot
records = []
for y in years:
    for r in regions:
        records.append({
            'year': y,
            'region': r,
            'loan_balance': float(loan_data.get(y, {}).get(r, 0.0)),
            'deposit_balance': float(deposit_data.get(y, {}).get(r, 0.0)),
            'grant_amount': float(grant_data.get(y, {}).get(r, 0.0)),
        })

df_consolidated = pd.DataFrame(records)
df_pivot = (
    df_consolidated
    .pivot_table(index='year', columns='region', values=['loan_balance', 'deposit_balance', 'grant_amount'])
    .swaplevel(0, 1, axis=1)
    .sort_index(axis=1)
)

regions_to_plot = list(df_pivot.columns.get_level_values(0).unique())

# --- Formatters ---
def millions_formatter(x, pos):
    return f'${x/1e6:.0f}M'

def thousands_formatter(x, pos):
    return f'${x/1e3:.0f}K'

# --- Helpers ---
def compute_grant_ylim(values, lower_floor=0.0, min_pad=100_000.0, pad_ratio=0.25):
    """
    Create a region-specific y-range for grants:
      - Compute spread-based padding with a minimum absolute buffer.
      - Never dip below lower_floor (defaults to $0).
    """
    v = np.asarray(values, dtype=float)
    vmin = float(np.nanmin(v))
    vmax = float(np.nanmax(v))
    spread = max(vmax - vmin, 0.0)
    pad = max(spread * pad_ratio, min_pad)
    # Handle flat lines (e.g., identical values across years)
    if np.isclose(spread, 0.0):
        lower = max(lower_floor, vmin - pad)
        upper = vmax + pad
    else:
        lower = max(lower_floor, vmin - pad)
        upper = vmax + pad
    # If everything is zero, make a small default range
    if np.isclose(upper, lower):
        upper = lower + 2 * min_pad
    return lower, upper

def safe_filename(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '_', s)

# --- Plot: one PNG per region ---
colors = {
    'loan_balance': '#1f77b4',     # Blue
    'deposit_balance': '#ff7f0e',  # Orange
    'grant_amount': '#2ca02c',     # Green
}

years_index = df_pivot.index  # ensure we keep the index handy

for region in regions_to_plot:
    # Pull series safely; fill missing with 0 to avoid plotting issues
    loan_values = df_pivot.get((region, 'loan_balance'), pd.Series(0.0, index=years_index)).reindex(years_index).fillna(0.0)
    deposit_values = df_pivot.get((region, 'deposit_balance'), pd.Series(0.0, index=years_index)).reindex(years_index).fillna(0.0)
    grant_values = df_pivot.get((region, 'grant_amount'), pd.Series(0.0, index=years_index)).reindex(years_index).fillna(0.0)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Primary axis (Loans & Deposits)
    line_loan, = ax.plot(years_index, loan_values, label='Loan Balance', color=colors['loan_balance'], marker='o', linewidth=2)
    line_deposit, = ax.plot(years_index, deposit_values, label='Deposit Balance', color=colors['deposit_balance'], marker='s', linewidth=2)

    ax.set_ylabel('Balance (Millions)', fontsize=12, fontweight='bold', color='gray')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
    ax.tick_params(axis='y', labelcolor='gray')
    ax.set_xticks(years_index)
    ax.grid(axis='y', linestyle=':', linewidth=0.7, alpha=0.6)

    # Secondary axis (Grants) with dynamic scaling
    ax2 = ax.twinx()
    line_grant, = ax2.plot(years_index, grant_values, label='Grants Awarded',
                           color=colors['grant_amount'], linestyle='--', marker='o', markersize=6, linewidth=2)
    g_lower, g_upper = compute_grant_ylim(grant_values.values, lower_floor=0.0, min_pad=100_000.0, pad_ratio=0.25)
    ax2.set_ylim(g_lower, g_upper)
    ax2.set_ylabel('Grant Amount (Thousands)', color=colors['grant_amount'], fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=colors['grant_amount'])
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))

    # Title & legend
    ax.set_title(f'{region}: 2020–2024 Loans, Deposits & Grants', fontsize=16, fontweight='bold')
    lines = [line_loan, line_deposit, line_grant]
    labels = ['Loan Balance', 'Deposit Balance', 'Grants Awarded']
    ax.legend(lines, labels, loc='upper left', frameon=False)

    fig.tight_layout()
    out_path = f"regional_financial_trends_{safe_filename(region)}.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# If you used to rely on a single image file name in downstream code, update it to load
# the region-specific files created above:
#   regional_financial_trends_Attleboro_Taunton.png
#   regional_financial_trends_South_Coast.png
#   regional_financial_trends_Rhode_Island.png
#   regional_financial_trends_Other.png

