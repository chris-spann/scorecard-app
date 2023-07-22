import pytest
from models.round import Round


def test_round_valid_input():
    round = Round(round=1, b1_score=10, b2_score=9)
    assert round.b1_score == 10


def test_round_invalid_score():
    with pytest.raises(ValueError):
        Round(b1_score=11, b2_score=9, round=2)


def test_round_invalid_round():
    with pytest.raises(ValueError):
        Round(b1_score=12, b2_score=9, round=65)
