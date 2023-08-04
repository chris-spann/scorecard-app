from models.boxer import Boxer


def test_str():
    boxer = Boxer(name="Muhammad Ali")
    assert str(boxer) == "Muhammad Ali"
