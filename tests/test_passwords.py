from passwords import Passwords

alphabet_0_9 = "0123456789"


class TestPasswords:

    def test1(self):
        p = Passwords(start="00", end="11", alphabet="01")
        assert p.total == 4
        assert list(p.generator()) == ["00", "01", "10", "11"]

    def test2(self):
        p = Passwords(start="01", end="11", alphabet="01")
        assert p.total == 3
        assert list(p.generator()) == ["01", "10", "11"]

    def test3(self):
        p = Passwords(start="00", end="01", alphabet="01")
        assert p.total == 2
        assert list(p.generator()) == ["00", "01"]



