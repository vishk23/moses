"""
Date calculation utilities for Customer 360 Dashboard.

This module provides functions to calculate various time periods needed for
multi-period balance analysis, including:
- Current date and prior business day
- Prior month-end, quarter-end, and year-end
- Trailing month-ends for trend analysis
- Recent business days for activity charts
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Dict


def get_current_date() -> datetime:
    """
    Get current date (or latest business day if weekend).

    Returns:
        datetime: Current date with time set to midnight (00:00:00)
    """
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def get_prior_business_day(reference_date: datetime) -> datetime:
    """
    Get prior business day (T-1).

    Note: This returns a simple day-1 calculation. The actual business day
    adjustment for weekends and holidays is handled by cdutils.query_df_on_date()
    during data fetching.

    Args:
        reference_date: The reference date to calculate from

    Returns:
        datetime: Date one day prior to reference_date
    """
    prior = reference_date - timedelta(days=1)
    return prior


def get_prior_month_end(reference_date: datetime) -> datetime:
    """
    Get last day of prior month.

    Example: If today is 2025-10-21, returns 2025-09-30

    Args:
        reference_date: The reference date to calculate from

    Returns:
        datetime: Last day of the prior month
    """
    first_of_current_month = reference_date.replace(day=1)
    last_day_prior_month = first_of_current_month - timedelta(days=1)
    return last_day_prior_month


def get_prior_quarter_end(reference_date: datetime) -> datetime:
    """
    Get last day of prior quarter.

    Quarters: Q1=Mar 31, Q2=Jun 30, Q3=Sep 30, Q4=Dec 31

    Examples:
        - If in Q1 (Jan-Mar): Returns Dec 31 of prior year
        - If in Q2 (Apr-Jun): Returns Mar 31 of current year
        - If in Q3 (Jul-Sep): Returns Jun 30 of current year
        - If in Q4 (Oct-Dec): Returns Sep 30 of current year

    Args:
        reference_date: The reference date to calculate from

    Returns:
        datetime: Last day of the prior quarter
    """
    current_quarter = (reference_date.month - 1) // 3 + 1

    if current_quarter == 1:
        # Prior quarter is Q4 of prior year
        return datetime(reference_date.year - 1, 12, 31)
    else:
        prior_quarter_end_month = (current_quarter - 1) * 3
        # Get last day of that month
        first_of_next_month = datetime(reference_date.year, prior_quarter_end_month + 1, 1)
        return first_of_next_month - timedelta(days=1)


def get_prior_year_end(reference_date: datetime) -> datetime:
    """
    Get December 31 of prior year.

    Example: If today is 2025-10-21, returns 2024-12-31

    Args:
        reference_date: The reference date to calculate from

    Returns:
        datetime: December 31 of the prior year
    """
    return datetime(reference_date.year - 1, 12, 31)


def get_trailing_month_ends(reference_date: datetime, num_months: int = 16) -> List[datetime]:
    """
    Get last day of trailing N months (starting from PRIOR month, not current).

    Example (if today = 2025-10-21, num_months=16):
        Returns: [2025-09-30, 2025-08-31, 2025-07-31, ..., 2024-06-30]

    Note: Starts from prior month-end (first day of current month - 1 day).
          This ensures we only include completed months.

    Args:
        reference_date: The reference date to calculate from
        num_months: Number of trailing months to return (default: 16)

    Returns:
        List[datetime]: List of month-end dates in descending order
    """
    month_ends = []

    for i in range(num_months):
        # Calculate date (i+1) months ago to start from prior month
        target_month = reference_date - relativedelta(months=i+1)

        # Get last day of that month
        # Move to first of next month, then back one day
        if target_month.month == 12:
            first_of_next = datetime(target_month.year + 1, 1, 1)
        else:
            first_of_next = datetime(target_month.year, target_month.month + 1, 1)

        month_end = first_of_next - timedelta(days=1)
        month_ends.append(month_end)

    return month_ends


def get_prior_n_business_days(reference_date: datetime, num_days: int = 8) -> List[datetime]:
    """
    Get prior N business days (simple day subtraction).

    Example (if today = 2025-10-21, num_days=8):
        Returns: [2025-10-21, 2025-10-20, 2025-10-19, ..., 2025-10-14]

    Note: This returns calendar days in descending order. The actual business day
          adjustment for weekends and holidays is handled by cdutils.query_df_on_date()
          during data fetching.

    Args:
        reference_date: The reference date to calculate from
        num_days: Number of days to return (default: 8)

    Returns:
        List[datetime]: List of dates in descending order (most recent first)
    """
    business_days = []

    for i in range(num_days):
        day = reference_date - timedelta(days=i)
        business_days.append(day)

    return business_days


def get_all_required_dates(reference_date: datetime = None) -> Dict[str, any]:
    """
    Get all required dates for the Customer 360 pipeline.

    This function calculates all date snapshots needed for comprehensive
    time-series analysis in the PowerBI dashboard.

    Args:
        reference_date: Optional reference date (defaults to current date)

    Returns:
        Dictionary with keys:
        - 'current': Current date
        - 'prior_day': T-1 (prior business day)
        - 'prior_month_end': Last day of prior month
        - 'prior_quarter_end': Last day of prior quarter
        - 'prior_year_end': December 31 of prior year
        - 'trailing_16_months': List of 16 month-end dates
        - 'prior_8_days': List of 8 recent business days
    """
    if reference_date is None:
        reference_date = get_current_date()

    return {
        'current': reference_date,
        'prior_day': get_prior_business_day(reference_date),
        'prior_month_end': get_prior_month_end(reference_date),
        'prior_quarter_end': get_prior_quarter_end(reference_date),
        'prior_year_end': get_prior_year_end(reference_date),
        'trailing_16_months': get_trailing_month_ends(reference_date, num_months=16),
        'prior_8_days': get_prior_n_business_days(reference_date, num_days=8)
    }
