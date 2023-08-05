from unittest.mock import patch

from cli import get_boxer_info
from models import ScorecardCli


@patch("cli.click.prompt", side_effect=["Muhammad Ali", "Mike Tyson", 12])
def test_get_boxer_info(mock_prompt):
    scorecard = get_boxer_info()
    assert isinstance(scorecard, ScorecardCli)
    assert scorecard.b1.name == "Muhammad Ali"
    assert scorecard.b2.name == "Mike Tyson"
    assert scorecard.rounds == 12
