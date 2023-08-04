from models.boxer import Boxer
from models.scorecard import Scorecard
from pytest import fixture


@fixture()
def mock_scorecard():
    b1 = Boxer(name="Muhammad Ali")
    b2 = Boxer(name="Joe Frazier")
    card = Scorecard(b1=b1, b2=b2, rounds=12)
    yield card
