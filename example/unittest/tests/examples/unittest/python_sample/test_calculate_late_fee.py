import pytest
from examples.unittest.python_sample.library import calculate_late_fee

@pytest.mark.parametrize("days_overdue, expected_fee", [
    (0, 0),          # test_no_overdue
    (1, 0.5),        # test_one_day_overdue
    (7, 3.5),        # test_seven_days_overdue
    (8, 4.5),        # test_eight_days_overdue
    (-1, 0),         # test_negative_days_overdue
    (0, 0),          # test_boundary_zero_days
    (1, 0.5),        # test_boundary_one_day
    (7, 3.5),        # test_boundary_seven_days
    (8, 4.5)         # test_boundary_eight_days
])
def test_calculate_late_fee(days_overdue, expected_fee):
    assert calculate_late_fee(days_overdue) == expected_fee