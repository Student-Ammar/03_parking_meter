"""Unit tests for parking_fee.calculate_parking_fee (Spec 3.1).

Each test maps to a test case ID in the Test Case Specification (PM-TCS).
Rule under test: 200 cents per STARTED hour; 0 minutes costs 0.
"""
import pytest

from parking_fee import calculate_parking_fee


# ---------- Valid inputs (Req 3.1.1, 3.1.2) ----------

# Checks: zero minutes. Expected: charge is 0.
def test_fee_001_zero_minutes_costs_zero():
    assert calculate_parking_fee(0) == 0


# Checks: 1 minute (any part of an hour counts). Expected: 200 cents.
def test_fee_002_one_minute_charged_one_full_hour():
    assert calculate_parking_fee(1) == 200


# Checks: 59 minutes, still inside the first hour. Expected: 200 cents.
def test_fee_003_59_minutes_charged_one_full_hour():
    assert calculate_parking_fee(59) == 200


# Checks: upper boundary of hour 1. Expected: 200 cents.
def test_fee_004_exactly_60_minutes_charged_one_hour():
    assert calculate_parking_fee(60) == 200


# Checks: just over the boundary starts hour 2. Expected: 400 cents.
def test_fee_005_61_minutes_charged_two_hours():
    assert calculate_parking_fee(61) == 400


# Checks: upper boundary of hour 2. Expected: 400 cents.
def test_fee_006_exactly_120_minutes_charged_two_hours():
    assert calculate_parking_fee(120) == 400


# Checks: just over hour 2 starts hour 3. Expected: 600 cents.
def test_fee_007_121_minutes_charged_three_hours():
    assert calculate_parking_fee(121) == 600


# Checks: a large exact multiple (10 hours). Expected: 2000 cents.
def test_fee_008_large_exact_multiple_of_hours():
    assert calculate_parking_fee(600) == 2000  # 10 hours


# Checks: the return type. Expected: an int, not float or str.
def test_fee_009_result_is_an_integer():
    assert type(calculate_parking_fee(60)) is int


# ---------- Invalid inputs (General Req 2, 3, 4) ----------

# Checks: negative minutes (right type, wrong range).
# Expected: ValueError. parametrize runs this test once per value.
@pytest.mark.parametrize("minutes", [-1, -60])
def test_fee_010_negative_minutes_raises_value_error(minutes):
    with pytest.raises(ValueError):
        calculate_parking_fee(minutes)


# Checks: floats (wrong type, even 60.0). Expected: TypeError.
@pytest.mark.parametrize("minutes", [1.5, 60.0])
def test_fee_011_float_minutes_raises_type_error(minutes):
    with pytest.raises(TypeError):
        calculate_parking_fee(minutes)


# Checks: a string and None (wrong type). Expected: TypeError.
@pytest.mark.parametrize("minutes", ["60", None])
def test_fee_012_non_numeric_minutes_raises_type_error(minutes):
    with pytest.raises(TypeError):
        calculate_parking_fee(minutes)


# Checks: booleans (not valid integers per the spec). Expected: TypeError.
@pytest.mark.parametrize("minutes", [True, False])
def test_fee_013_bool_minutes_raises_type_error(minutes):
    with pytest.raises(TypeError):
        calculate_parking_fee(minutes)
