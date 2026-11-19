"""Unit tests for parking_permit.is_permit_valid (Spec 3.2).

Each test maps to a test case ID in the Test Case Specification (PM-TCS).
Rule under test: valid only if permit_active is True AND parked_minutes <= 120.
Return value must be the real bool True/False, not 1/0.
"""
import pytest

from parking_permit import is_permit_valid


# ---------- Valid inputs (Req 3.2.1, 3.2.2) ----------
# "is True" / "is False" is used on purpose: "== True" would also accept 1.

# Checks: active permit, 0 minutes (zero is allowed). Expected: True.
def test_permit_001_active_zero_minutes_is_valid():
    assert is_permit_valid(True, 0) is True


# Checks: active permit, well within the limit. Expected: True.
def test_permit_002_active_within_limit_is_valid():
    assert is_permit_valid(True, 60) is True


# Checks: boundary, exactly 120 minutes is still allowed. Expected: True.
def test_permit_003_active_exactly_120_minutes_is_valid():
    assert is_permit_valid(True, 120) is True


# Checks: just over the boundary. Expected: False.
def test_permit_004_active_121_minutes_is_not_valid():
    assert is_permit_valid(True, 121) is False


# Checks: inactive permit, 0 minutes. Expected: False.
def test_permit_005_inactive_zero_minutes_is_not_valid():
    assert is_permit_valid(False, 0) is False


# Checks: inactive permit, even within the limit. Expected: False.
def test_permit_006_inactive_within_limit_is_not_valid():
    assert is_permit_valid(False, 120) is False


# Checks: inactive permit and over the limit. Expected: False.
def test_permit_007_inactive_over_limit_is_not_valid():
    assert is_permit_valid(False, 121) is False


# Checks: the return type is a real bool (not 1 or 0) for True and False.
# Expected: type is bool. parametrize runs this once per input pair.
@pytest.mark.parametrize("active, minutes", [(True, 60), (False, 60)])
def test_permit_008_result_is_a_real_bool(active, minutes):
    assert type(is_permit_valid(active, minutes)) is bool


# ---------- Invalid inputs (General Req 2, 3, 4) ----------

# Checks: negative minutes (right type, wrong range). Expected: ValueError.
@pytest.mark.parametrize("active", [True, False])
def test_permit_009_negative_minutes_raises_value_error(active):
    with pytest.raises(ValueError):
        is_permit_valid(active, -1)


# Checks: permit_active is not a bool (1, 0, string, None). Expected: TypeError.
@pytest.mark.parametrize("active", [1, 0, "True", None])
def test_permit_010_non_bool_permit_raises_type_error(active):
    with pytest.raises(TypeError):
        is_permit_valid(active, 60)


# Checks: parked_minutes is not an int (float, string, None, bool).
# Expected: TypeError.
@pytest.mark.parametrize("minutes", [60.5, "60", None, True, False])
def test_permit_011_non_int_minutes_raises_type_error(minutes):
    with pytest.raises(TypeError):
        is_permit_valid(True, minutes)


# Checks: bad type AND out-of-range value together (1 is not a bool, -5 < 0).
# Expected: TypeError, because the type check comes first.
def test_permit_012_type_error_takes_priority_over_value_error():
    # permit_active has a bad type AND minutes is out of range
    with pytest.raises(TypeError):
        is_permit_valid(1, -5)
