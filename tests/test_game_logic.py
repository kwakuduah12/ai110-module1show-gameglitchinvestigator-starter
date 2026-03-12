import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from logic_utils import check_guess, parse_guess


# --- Existing tests (fixed: check_guess returns a tuple, not a plain string) ---

def test_winning_guess():
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug fix: hint messages were swapped ---
# Before the fix, "Too High" returned "Go HIGHER!" and "Too Low" returned "Go LOWER!",
# sending the player in the wrong direction.

def test_too_high_hint_directs_player_lower():
    # Guess is above secret — player should be told to go lower
    _, message = check_guess(80, 50)
    assert "LOWER" in message, f"Expected 'LOWER' in hint for too-high guess, got: {message}"

def test_too_low_hint_directs_player_higher():
    # Guess is below secret — player should be told to go higher
    _, message = check_guess(20, 50)
    assert "HIGHER" in message, f"Expected 'HIGHER' in hint for too-low guess, got: {message}"

def test_swapped_hints_not_present():
    # Explicitly confirm the old wrong behavior no longer occurs
    _, high_message = check_guess(80, 50)
    assert "HIGHER" not in high_message, "Too-high guess should NOT say HIGHER"

    _, low_message = check_guess(20, 50)
    assert "LOWER" not in low_message, "Too-low guess should NOT say LOWER"


# --- Bug fix: decimal inputs were silently truncated instead of rejected ---
# Before the fix, "7.9" would be accepted and processed as 7 with no feedback to the player.

def test_decimal_input_is_rejected():
    ok, value, error = parse_guess("7.9")
    assert ok is False, "Decimal input should be rejected"
    assert value is None
    assert error is not None

def test_decimal_rejection_has_clear_message():
    _, _, error = parse_guess("7.9")
    assert "whole number" in error.lower() or "decimal" in error.lower(), (
        f"Error message should mention whole numbers or decimals, got: {error}"
    )

def test_decimal_zero_is_rejected():
    # Even "5.0" should be rejected — player must type whole numbers
    ok, _, _ = parse_guess("5.0")
    assert ok is False

def test_whole_number_is_accepted():
    # Confirm valid whole number input still works after the decimal fix
    ok, value, error = parse_guess("42")
    assert ok is True
    assert value == 42
    assert error is None

def test_empty_input_is_rejected():
    ok, _, error = parse_guess("")
    assert ok is False
    assert error is not None

def test_non_numeric_input_is_rejected():
    ok, _, error = parse_guess("abc")
    assert ok is False
    assert error is not None


# --- Edge case: negative numbers should be rejected ---
# parse_guess currently accepts negative integers because they pass the decimal
# and int() checks. The game range starts at 1, so negatives are never valid.

@pytest.mark.xfail(reason="parse_guess does not yet reject negative numbers")
def test_negative_number_is_rejected():
    ok, value, error = parse_guess("-1")
    assert ok is False, "Negative input should be rejected"
    assert value is None
    assert error is not None

@pytest.mark.xfail(reason="parse_guess does not yet reject negative numbers")
def test_negative_number_has_clear_message():
    _, _, error = parse_guess("-1")
    assert error is not None, "Error message should explain why the input is invalid"

@pytest.mark.xfail(reason="parse_guess does not yet reject negative numbers")
def test_large_negative_is_rejected():
    ok, _, _ = parse_guess("-999")
    assert ok is False, "Large negative input should also be rejected"


# --- Edge case: out-of-range large numbers should be rejected ---
# parse_guess currently accepts integers above 100 with no upper-bound check.
# Guessing 200 in a 1-100 game should return an error, not silently proceed.

@pytest.mark.xfail(reason="parse_guess does not yet reject out-of-range numbers")
def test_number_above_range_is_rejected():
    ok, value, error = parse_guess("200")
    assert ok is False, "Numbers above the valid range should be rejected"
    assert value is None
    assert error is not None

@pytest.mark.xfail(reason="parse_guess does not yet reject out-of-range numbers")
def test_number_above_range_has_clear_message():
    _, _, error = parse_guess("200")
    assert error is not None, "Error message should explain the valid range"

def test_boundary_value_100_is_accepted():
    # 100 is the top of the Normal range — it should still be valid
    ok, value, error = parse_guess("100")
    assert ok is True
    assert value == 100
    assert error is None

def test_boundary_value_1_is_accepted():
    # 1 is the bottom of the range — it should still be valid
    ok, value, error = parse_guess("1")
    assert ok is True
    assert value == 1
    assert error is None


# --- Edge case: string secret causes wrong hint on even-numbered attempts ---
# In app.py, secret is cast to str on even attempts before being passed to
# check_guess. String comparison is lexicographic: "9" > "50" is True because
# "9" > "5", so a guess of 9 against secret "50" incorrectly returns "Too High".

@pytest.mark.xfail(reason="check_guess uses lexicographic comparison when secret is a string")
def test_string_secret_low_guess_returns_too_low():
    # 9 < 50 — outcome must be "Too Low" regardless of secret type
    outcome, _ = check_guess(9, "50")
    assert outcome == "Too Low", (
        f"check_guess(9, '50') should return 'Too Low' but got '{outcome}'. "
        "This fails due to lexicographic string comparison: '9' > '5'."
    )

@pytest.mark.xfail(reason="check_guess uses lexicographic comparison when secret is a string")
def test_string_secret_low_guess_hint_directs_higher():
    # Player guessed too low — hint must say go HIGHER
    _, message = check_guess(9, "50")
    assert "HIGHER" in message, (
        f"Hint for guess 9 vs secret '50' should say HIGHER, got: {message}"
    )

def test_string_secret_high_guess_returns_too_high():
    # 80 > 50 — outcome must be "Too High" regardless of secret type
    outcome, _ = check_guess(80, "50")
    assert outcome == "Too High", (
        f"check_guess(80, '50') should return 'Too High' but got '{outcome}'."
    )
