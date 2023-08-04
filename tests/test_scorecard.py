from models.boxer import Boxer
from models.round import Round
from models.scorecard import ScorecardBase


def test_complete_round(mock_scorecard):
    round = Round(round=1, b1_score=10, b2_score=9)
    mock_scorecard.complete_round(round)
    assert mock_scorecard.scores[0].round == 1
    assert mock_scorecard.scores[0].b1_score == 10
    assert mock_scorecard.scores[0].b2_score == 9


def test_get_winner(mock_scorecard):
    mock_scorecard.complete_round(Round(round=1, b1_score=10, b2_score=9))
    mock_scorecard.complete_round(Round(round=2, b1_score=10, b2_score=9))
    mock_scorecard.complete_round(Round(round=3, b1_score=10, b2_score=9))
    assert mock_scorecard.determine_winner()[0] == mock_scorecard.b1.name


def test_get_winner_b2(mock_scorecard):
    mock_scorecard.complete_round(Round(round=1, b1_score=9, b2_score=10))
    mock_scorecard.complete_round(Round(round=2, b1_score=9, b2_score=10))
    mock_scorecard.complete_round(Round(round=3, b1_score=9, b2_score=10))
    assert mock_scorecard.determine_winner()[0] == mock_scorecard.b2.name


def test_get_winner_draw(mock_scorecard):
    mock_scorecard.complete_round(Round(round=1, b1_score=10, b2_score=10))
    mock_scorecard.complete_round(Round(round=2, b1_score=10, b2_score=10))
    mock_scorecard.complete_round(Round(round=3, b1_score=10, b2_score=10))
    assert mock_scorecard.determine_winner()[0] == "N/A"


def test_str(mock_scorecard):
    assert str(mock_scorecard) == "Muhammad Ali vs. Joe Frazier, 12 rounds"


def test_invalid_fight_length():
    b1 = Boxer(name="Muhammad Ali")
    b2 = Boxer(name="Joe Frazier")
    try:
        ScorecardBase(b1=b1, b2=b2, rounds=1)
    except ValueError as e:
        assert str(e) == "rounds must be in range(3, 13)"


def test_reset_round(mock_scorecard):
    round = Round(round=1, b1_score=10, b2_score=9)
    mock_scorecard.complete_round(round)
    assert mock_scorecard.scores[0].b1_score == 10
    assert mock_scorecard.scores[0].b2_score == 9
    mock_scorecard.reset_round(1)
    assert mock_scorecard.scores[0].b1_score == 0
    assert mock_scorecard.scores[0].b2_score == 0


def test_reset_round_fail(mock_scorecard):
    round = Round(round=1, b1_score=10, b2_score=9)
    mock_scorecard.complete_round(round)
    assert mock_scorecard.scores[0].b1_score == 10
    assert mock_scorecard.scores[0].b2_score == 9
    mock_scorecard.reset_round(1)
    assert mock_scorecard.scores[0].b1_score == 0
    assert mock_scorecard.scores[0].b2_score == 0


def test_reset_card(mock_scorecard):
    mock_scorecard.complete_round(Round(round=1, b1_score=10, b2_score=9))
    mock_scorecard.complete_round(Round(round=2, b1_score=10, b2_score=9))
    mock_scorecard.complete_round(Round(round=3, b1_score=10, b2_score=9))
    assert mock_scorecard.scores[0].b1_score == 10
    assert mock_scorecard.scores[0].b2_score == 9
    assert mock_scorecard.scores[1].b1_score == 10
    assert mock_scorecard.scores[1].b2_score == 9
    assert mock_scorecard.scores[2].b1_score == 10
    assert mock_scorecard.scores[2].b2_score == 9
    mock_scorecard.reset_card()
    assert mock_scorecard.scores[0].b1_score == 0
    assert mock_scorecard.scores[0].b2_score == 0
    assert mock_scorecard.scores[1].b1_score == 0
    assert mock_scorecard.scores[1].b2_score == 0
    assert mock_scorecard.scores[2].b1_score == 0
    assert mock_scorecard.scores[2].b2_score == 0
