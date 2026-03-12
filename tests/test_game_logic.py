import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

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
