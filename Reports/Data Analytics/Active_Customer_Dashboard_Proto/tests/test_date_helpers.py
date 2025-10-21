"""
Unit tests for date_helpers.py

Tests date calculation functions with various boundary conditions:
- Month boundaries (first day, last day, mid-month)
- Quarter boundaries (Q1→Q4, Q2→Q1, Q3→Q2, Q4→Q3)
- Year boundaries (Jan 1, Dec 31)
- Leap years
- Deduplication logic
"""

import pytest
from datetime import datetime
from src.utils.date_helpers import (
    get_current_date,
    get_prior_business_day,
    get_prior_month_end,
    get_prior_quarter_end,
    get_prior_year_end,
    get_trailing_month_ends,
    get_prior_n_business_days,
    get_all_required_dates
)


class TestCurrentDate:
    """Test get_current_date function."""

    def test_returns_datetime_object(self):
        result = get_current_date()
        assert isinstance(result, datetime)

    def test_time_set_to_midnight(self):
        result = get_current_date()
        assert result.hour == 0
        assert result.minute == 0
        assert result.second == 0
        assert result.microsecond == 0


class TestPriorBusinessDay:
    """Test get_prior_business_day function."""

    def test_mid_month(self):
        reference = datetime(2025, 10, 21)
        result = get_prior_business_day(reference)
        assert result == datetime(2025, 10, 20)

    def test_first_of_month(self):
        reference = datetime(2025, 10, 1)
        result = get_prior_business_day(reference)
        assert result == datetime(2025, 9, 30)

    def test_first_of_year(self):
        reference = datetime(2025, 1, 1)
        result = get_prior_business_day(reference)
        assert result == datetime(2024, 12, 31)

    def test_leap_year_march_1(self):
        reference = datetime(2024, 3, 1)
        result = get_prior_business_day(reference)
        assert result == datetime(2024, 2, 29)


class TestPriorMonthEnd:
    """Test get_prior_month_end function."""

    def test_mid_month_october(self):
        reference = datetime(2025, 10, 21)
        result = get_prior_month_end(reference)
        assert result == datetime(2025, 9, 30)

    def test_first_of_month(self):
        reference = datetime(2025, 10, 1)
        result = get_prior_month_end(reference)
        assert result == datetime(2025, 9, 30)

    def test_last_of_month(self):
        reference = datetime(2025, 10, 31)
        result = get_prior_month_end(reference)
        assert result == datetime(2025, 9, 30)

    def test_january_returns_december_prior_year(self):
        reference = datetime(2025, 1, 15)
        result = get_prior_month_end(reference)
        assert result == datetime(2024, 12, 31)

    def test_march_leap_year(self):
        reference = datetime(2024, 3, 15)
        result = get_prior_month_end(reference)
        assert result == datetime(2024, 2, 29)

    def test_march_non_leap_year(self):
        reference = datetime(2025, 3, 15)
        result = get_prior_month_end(reference)
        assert result == datetime(2025, 2, 28)

    def test_various_month_lengths(self):
        # April (30 days) -> March (31 days)
        assert get_prior_month_end(datetime(2025, 4, 15)) == datetime(2025, 3, 31)
        # May (31 days) -> April (30 days)
        assert get_prior_month_end(datetime(2025, 5, 15)) == datetime(2025, 4, 30)
        # February (28 days) -> January (31 days)
        assert get_prior_month_end(datetime(2025, 2, 15)) == datetime(2025, 1, 31)


class TestPriorQuarterEnd:
    """Test get_prior_quarter_end function."""

    def test_q1_returns_prior_year_q4(self):
        # January (Q1) -> Dec 31 prior year
        assert get_prior_quarter_end(datetime(2025, 1, 15)) == datetime(2024, 12, 31)
        # February (Q1) -> Dec 31 prior year
        assert get_prior_quarter_end(datetime(2025, 2, 15)) == datetime(2024, 12, 31)
        # March (Q1) -> Dec 31 prior year
        assert get_prior_quarter_end(datetime(2025, 3, 15)) == datetime(2024, 12, 31)

    def test_q2_returns_q1_march_31(self):
        # April (Q2) -> Mar 31
        assert get_prior_quarter_end(datetime(2025, 4, 15)) == datetime(2025, 3, 31)
        # May (Q2) -> Mar 31
        assert get_prior_quarter_end(datetime(2025, 5, 15)) == datetime(2025, 3, 31)
        # June (Q2) -> Mar 31
        assert get_prior_quarter_end(datetime(2025, 6, 15)) == datetime(2025, 3, 31)

    def test_q3_returns_q2_june_30(self):
        # July (Q3) -> Jun 30
        assert get_prior_quarter_end(datetime(2025, 7, 15)) == datetime(2025, 6, 30)
        # August (Q3) -> Jun 30
        assert get_prior_quarter_end(datetime(2025, 8, 15)) == datetime(2025, 6, 30)
        # September (Q3) -> Jun 30
        assert get_prior_quarter_end(datetime(2025, 9, 15)) == datetime(2025, 6, 30)

    def test_q4_returns_q3_september_30(self):
        # October (Q4) -> Sep 30
        assert get_prior_quarter_end(datetime(2025, 10, 21)) == datetime(2025, 9, 30)
        # November (Q4) -> Sep 30
        assert get_prior_quarter_end(datetime(2025, 11, 15)) == datetime(2025, 9, 30)
        # December (Q4) -> Sep 30
        assert get_prior_quarter_end(datetime(2025, 12, 15)) == datetime(2025, 9, 30)

    def test_first_day_of_quarter(self):
        # First day of Q2 (Apr 1) -> Mar 31 (Q1)
        assert get_prior_quarter_end(datetime(2025, 4, 1)) == datetime(2025, 3, 31)
        # First day of Q3 (Jul 1) -> Jun 30 (Q2)
        assert get_prior_quarter_end(datetime(2025, 7, 1)) == datetime(2025, 6, 30)

    def test_last_day_of_quarter(self):
        # Last day of Q1 (Mar 31) -> Dec 31 prior year
        assert get_prior_quarter_end(datetime(2025, 3, 31)) == datetime(2024, 12, 31)
        # Last day of Q2 (Jun 30) -> Mar 31
        assert get_prior_quarter_end(datetime(2025, 6, 30)) == datetime(2025, 3, 31)


class TestPriorYearEnd:
    """Test get_prior_year_end function."""

    def test_mid_year(self):
        reference = datetime(2025, 10, 21)
        result = get_prior_year_end(reference)
        assert result == datetime(2024, 12, 31)

    def test_january_first(self):
        reference = datetime(2025, 1, 1)
        result = get_prior_year_end(reference)
        assert result == datetime(2024, 12, 31)

    def test_december_thirty_first(self):
        reference = datetime(2025, 12, 31)
        result = get_prior_year_end(reference)
        assert result == datetime(2024, 12, 31)

    def test_leap_year(self):
        reference = datetime(2024, 2, 29)
        result = get_prior_year_end(reference)
        assert result == datetime(2023, 12, 31)


class TestTrailingMonthEnds:
    """Test get_trailing_month_ends function."""

    def test_starts_from_prior_month(self):
        reference = datetime(2025, 10, 21)
        result = get_trailing_month_ends(reference, num_months=16)
        # First element should be prior month-end (Sep 30), NOT current month
        assert result[0] == datetime(2025, 9, 30)

    def test_correct_count(self):
        reference = datetime(2025, 10, 21)
        result = get_trailing_month_ends(reference, num_months=16)
        assert len(result) == 16

    def test_descending_order(self):
        reference = datetime(2025, 10, 21)
        result = get_trailing_month_ends(reference, num_months=16)
        # Should be in descending order (most recent first)
        assert result[0] == datetime(2025, 9, 30)
        assert result[1] == datetime(2025, 8, 31)
        assert result[2] == datetime(2025, 7, 31)

    def test_16_months_from_october(self):
        reference = datetime(2025, 10, 21)
        result = get_trailing_month_ends(reference, num_months=16)
        expected = [
            datetime(2025, 9, 30),   # 1 month ago
            datetime(2025, 8, 31),   # 2 months ago
            datetime(2025, 7, 31),   # 3 months ago
            datetime(2025, 6, 30),   # 4 months ago
            datetime(2025, 5, 31),   # 5 months ago
            datetime(2025, 4, 30),   # 6 months ago
            datetime(2025, 3, 31),   # 7 months ago
            datetime(2025, 2, 28),   # 8 months ago
            datetime(2025, 1, 31),   # 9 months ago
            datetime(2024, 12, 31),  # 10 months ago
            datetime(2024, 11, 30),  # 11 months ago
            datetime(2024, 10, 31),  # 12 months ago
            datetime(2024, 9, 30),   # 13 months ago
            datetime(2024, 8, 31),   # 14 months ago
            datetime(2024, 7, 31),   # 15 months ago
            datetime(2024, 6, 30),   # 16 months ago
        ]
        assert result == expected

    def test_year_boundary_crossing(self):
        reference = datetime(2025, 1, 15)
        result = get_trailing_month_ends(reference, num_months=3)
        expected = [
            datetime(2024, 12, 31),  # Prior month
            datetime(2024, 11, 30),  # 2 months ago
            datetime(2024, 10, 31),  # 3 months ago
        ]
        assert result == expected

    def test_leap_year_february(self):
        reference = datetime(2024, 3, 15)
        result = get_trailing_month_ends(reference, num_months=2)
        expected = [
            datetime(2024, 2, 29),  # Leap year Feb
            datetime(2024, 1, 31),
        ]
        assert result == expected

    def test_custom_num_months(self):
        reference = datetime(2025, 10, 21)
        result = get_trailing_month_ends(reference, num_months=5)
        assert len(result) == 5
        assert result[0] == datetime(2025, 9, 30)
        assert result[4] == datetime(2025, 5, 31)

    def test_first_of_month(self):
        # Even on first of month, should start from PRIOR month
        reference = datetime(2025, 10, 1)
        result = get_trailing_month_ends(reference, num_months=2)
        expected = [
            datetime(2025, 9, 30),  # Prior month
            datetime(2025, 8, 31),  # 2 months ago
        ]
        assert result == expected


class TestPriorNBusinessDays:
    """Test get_prior_n_business_days function."""

    def test_includes_current_day(self):
        reference = datetime(2025, 10, 21)
        result = get_prior_n_business_days(reference, num_days=8)
        # First element should be current day
        assert result[0] == reference

    def test_correct_count(self):
        reference = datetime(2025, 10, 21)
        result = get_prior_n_business_days(reference, num_days=8)
        assert len(result) == 8

    def test_descending_order(self):
        reference = datetime(2025, 10, 21)
        result = get_prior_n_business_days(reference, num_days=8)
        expected = [
            datetime(2025, 10, 21),  # Current (T+0)
            datetime(2025, 10, 20),  # T-1
            datetime(2025, 10, 19),  # T-2
            datetime(2025, 10, 18),  # T-3
            datetime(2025, 10, 17),  # T-4
            datetime(2025, 10, 16),  # T-5
            datetime(2025, 10, 15),  # T-6
            datetime(2025, 10, 14),  # T-7
        ]
        assert result == expected

    def test_month_boundary_crossing(self):
        reference = datetime(2025, 10, 2)
        result = get_prior_n_business_days(reference, num_days=5)
        expected = [
            datetime(2025, 10, 2),
            datetime(2025, 10, 1),
            datetime(2025, 9, 30),
            datetime(2025, 9, 29),
            datetime(2025, 9, 28),
        ]
        assert result == expected

    def test_year_boundary_crossing(self):
        reference = datetime(2025, 1, 2)
        result = get_prior_n_business_days(reference, num_days=5)
        expected = [
            datetime(2025, 1, 2),
            datetime(2025, 1, 1),
            datetime(2024, 12, 31),
            datetime(2024, 12, 30),
            datetime(2024, 12, 29),
        ]
        assert result == expected

    def test_custom_num_days(self):
        reference = datetime(2025, 10, 21)
        result = get_prior_n_business_days(reference, num_days=3)
        assert len(result) == 3
        assert result == [
            datetime(2025, 10, 21),
            datetime(2025, 10, 20),
            datetime(2025, 10, 19),
        ]


class TestGetAllRequiredDates:
    """Test get_all_required_dates function."""

    def test_returns_all_keys(self):
        result = get_all_required_dates(datetime(2025, 10, 21))
        expected_keys = {
            'current',
            'prior_day',
            'prior_month_end',
            'prior_quarter_end',
            'prior_year_end',
            'trailing_16_months',
            'prior_8_days'
        }
        assert set(result.keys()) == expected_keys

    def test_october_21_2025(self):
        reference = datetime(2025, 10, 21)
        result = get_all_required_dates(reference)

        assert result['current'] == datetime(2025, 10, 21)
        assert result['prior_day'] == datetime(2025, 10, 20)
        assert result['prior_month_end'] == datetime(2025, 9, 30)
        assert result['prior_quarter_end'] == datetime(2025, 9, 30)
        assert result['prior_year_end'] == datetime(2024, 12, 31)
        assert len(result['trailing_16_months']) == 16
        assert len(result['prior_8_days']) == 8

    def test_january_first_edge_case(self):
        reference = datetime(2025, 1, 1)
        result = get_all_required_dates(reference)

        assert result['current'] == datetime(2025, 1, 1)
        assert result['prior_day'] == datetime(2024, 12, 31)
        assert result['prior_month_end'] == datetime(2024, 12, 31)
        assert result['prior_quarter_end'] == datetime(2024, 12, 31)
        assert result['prior_year_end'] == datetime(2024, 12, 31)

    def test_uses_current_date_if_none(self):
        # Should not raise an error
        result = get_all_required_dates()
        assert 'current' in result
        assert isinstance(result['current'], datetime)


class TestDeduplication:
    """Test deduplication logic for overlapping dates."""

    def test_overlapping_dates_october_21(self):
        """Test that we can identify overlapping dates across categories."""
        reference = datetime(2025, 10, 21)
        dates = get_all_required_dates(reference)

        # Collect all dates into a set for deduplication
        all_dates = set()
        all_dates.add(dates['prior_day'])
        all_dates.add(dates['prior_month_end'])
        all_dates.add(dates['prior_quarter_end'])
        all_dates.add(dates['prior_year_end'])

        for month_end in dates['trailing_16_months']:
            all_dates.add(month_end)

        for day in dates['prior_8_days']:
            all_dates.add(day)

        # Prior month-end (9/30) should overlap with prior quarter-end (9/30)
        assert dates['prior_month_end'] == dates['prior_quarter_end']

        # Prior month-end should be in trailing 16 months
        assert dates['prior_month_end'] in dates['trailing_16_months']

        # Prior quarter-end should be in trailing 16 months
        assert dates['prior_quarter_end'] in dates['trailing_16_months']

        # Current day should be in prior 8 days
        assert dates['current'] in dates['prior_8_days']

        # After deduplication, should have fewer than 29 dates (29 before dedup)
        # 1 + 1 + 1 + 1 + 1 + 16 + 8 = 29 before dedup
        assert len(all_dates) < 29

    def test_unique_dates_count_varies_by_reference_date(self):
        """Different reference dates may have different dedup counts."""
        # January 1 has maximum overlap (prior day = prior month = prior quarter = prior year)
        jan_dates = get_all_required_dates(datetime(2025, 1, 1))
        jan_unique = set()
        jan_unique.add(jan_dates['prior_day'])
        jan_unique.add(jan_dates['prior_month_end'])
        jan_unique.add(jan_dates['prior_quarter_end'])
        jan_unique.add(jan_dates['prior_year_end'])
        for d in jan_dates['trailing_16_months']:
            jan_unique.add(d)
        for d in jan_dates['prior_8_days']:
            jan_unique.add(d)

        # Mid-year date may have less overlap
        june_dates = get_all_required_dates(datetime(2025, 6, 15))
        june_unique = set()
        june_unique.add(june_dates['prior_day'])
        june_unique.add(june_dates['prior_month_end'])
        june_unique.add(june_dates['prior_quarter_end'])
        june_unique.add(june_dates['prior_year_end'])
        for d in june_dates['trailing_16_months']:
            june_unique.add(d)
        for d in june_dates['prior_8_days']:
            june_unique.add(d)

        # Both should have unique deduplication counts
        assert len(jan_unique) >= 20  # Rough estimate
        assert len(june_unique) >= 20

    def test_current_excluded_from_historical_fetches(self):
        """Verify that current date can be excluded from historical fetch list."""
        reference = datetime(2025, 10, 21)
        dates = get_all_required_dates(reference)

        # Build unique dates set (excluding current)
        unique_dates = set()
        unique_dates.add(dates['prior_day'])
        unique_dates.add(dates['prior_month_end'])
        unique_dates.add(dates['prior_quarter_end'])
        unique_dates.add(dates['prior_year_end'])

        for month_end in dates['trailing_16_months']:
            unique_dates.add(month_end)

        for day in dates['prior_8_days']:
            unique_dates.add(day)

        # Remove current date
        unique_dates.discard(dates['current'])

        # Should not contain current date anymore
        assert dates['current'] not in unique_dates
