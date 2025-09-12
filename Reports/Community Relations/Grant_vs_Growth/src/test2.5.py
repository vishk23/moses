import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# --- Assume df_pivot from the previous step already exists ---
# If not, you can recreate it with the previous code.
# Here's a quick recreation for context:
# (You would not need to run this again if it's in the same script)
years = [2021, 2022, 2023, 2024]
regions = ['Rhode Island', 'Southcoast', 'Attleboro/Taunton', 'Other']
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

# Determine regions to plot (exclude 'Other' as the equivalent of 'Unmapped')
regions_to_plot = [col for col in df_pivot.columns.get_level_values(0).unique() if col not in ['Other']]
# Assuming regions_to_plot = ['Rhode Island', 'Southcoast', 'Attleboro/Taunton']
num_regions = len(regions_to_plot)
nrows = int(np.ceil(np.sqrt(num_regions)))
ncols = int(np.ceil(num_regions / nrows))

# Initialize subplots with a clean, professional style
plt.style.use('seaborn-v0_8')  # Use a clean style akin to business reporting tools
fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(16, 12), sharex=True)
axes = axes.flatten()  # Flatten for easy iteration

# Get the years from df_pivot index
years = df_pivot.index

# Define formatters for currency axes (professional currency formatting)
def millions_formatter(x, pos):
    return f'${x / 1e6:.0f}M'

def thousands_formatter(x, pos):
    return f'${x / 1e3:.0f}K'

# Professional color palette (inspired by business intelligence tools like Tableau/PowerBI)
color_palette = {
    'loan_balance': '#1f77b4',  # Conservative blue
    'deposit_balance': '#aec7e8',  # Lighter blue
    'grant_amount': '#2ca02c'  # Professional green
}

# Loop through each region and its subplot
for i, region in enumerate(regions_to_plot):
    ax = axes[i]
    
    # Extract data for the region
    loan_values = df_pivot.loc[:, (region, 'loan_balance')]
    deposit_values = df_pivot.loc[:, (region, 'deposit_balance')]
    grant_values = df_pivot.loc[:, (region, 'grant_amount')]
    
    # Plot loan and deposit balances on primary axis
    ax.plot(years, loan_values, label='Loan Balance', color=color_palette['loan_balance'], marker='o', linewidth=2)
    ax.plot(years, deposit_values, label='Deposit Balance', color=color_palette['deposit_balance'], marker='s', linewidth=2)
    
    # Format primary y-axis
    ax.set_ylabel('Balance (Millions)', fontsize=12, fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(millions_formatter))
    ax.grid(axis='y', linestyle=':', alpha=0.5, color='gray')  # Subtle grid
    ax.set_facecolor('white')  # Ensure clean background
    
    # Create secondary y-axis for grants
    ax2 = ax.twinx()
    ax2.plot(years, grant_values, label='Grants Awarded', color=color_palette['grant_amount'], linestyle='--', marker='o', markersize=6, linewidth=2)
    
    # Format secondary y-axis
    ax2.set_ylabel('Grant Amount (Thousands)', color=color_palette['grant_amount'], fontsize=12, fontweight='bold')
    ax2.tick_params(axis='y', labelcolor=color_palette['grant_amount'])
    ax2.set_ylim(bottom=0)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(thousands_formatter))
    
    # Set subplot title
    ax.set_title(region, fontsize=14, fontweight='bold')
    
    # Add legends for both axes
    lines, labels_line = ax.get_legend_handles_labels()
    lines2, labels2_line = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels_line + labels2_line, loc='upper left', fontsize=10, frameon=False)

# Turn off unused subplots if necessary
for i in range(num_regions, nrows * ncols):
    fig.delaxes(axes[i])

# Set x-axis label for the entire figure (since shared)
fig.text(0.5, 0.04, 'Year', ha='center', fontsize=14, fontweight='bold')

# Add overarching title
fig.suptitle('Regional Financial Performance: Loan/Deposit Balances vs. Grants Awarded', fontsize=18, fontweight='bold')

# Adjust layout to prevent overlaps and enhance professional appearance
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the figure as a high-quality PNG
plt.savefig('regional_financial_trends.png', dpi=300, bbox_inches='tight')
