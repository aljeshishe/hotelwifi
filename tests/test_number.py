
from number import Number

alphabet_2 = "01"
alphabet_10 = "0123456789"


class TestNumber:
    def test_from_base_10(self):
        n = Number.from_base_10(value=267077, base=16)
        assert n.base == 16
        assert n.data == [5, 4, 3, 1, 4]

    def test_to_base_10(self):
        n = Number(data=[5, 4, 3, 1, 4], base=16)
        assert n.to_base_10() == 267077

    def test2(self):
        n = Number.from_str(value="00", alphabet="01")
        assert n.base == 2
        assert n.data == [0, 0]

    def test_from_str(self):
        result = Number.from_str(value="00", alphabet=alphabet_2).to_str(alphabet_2)
        assert result == "00"

    def test_add(self):
        result = Number.from_str(value="00", alphabet=alphabet_2)
        result += 2
        assert result.to_str(alphabet_2) == "10"

    def test_add_with_overflow(self):
        result = Number.from_str(value="01", alphabet=alphabet_2)
        result += 1
        assert result.to_str(alphabet_2) == "10"

    def test_add_with_overflow_add_extra_digit(self):
        result = Number.from_str(value="11", alphabet=alphabet_2)
        result += 1
        assert result.to_str(alphabet_2) == "100"

    def test_sub(self):
        result = Number.from_str(value="01", alphabet=alphabet_2)
        result -= 1
        assert result.to_str(alphabet_2) == "00"

    def test_sub_with_overflow(self):
        result = Number.from_str(value="10", alphabet=alphabet_2)
        result -= 1
        assert result.to_str(alphabet_2) == "01"

    def test_sub_with_overflow1(self):
        result = Number.from_str(value="00", alphabet=alphabet_2)
        result -= 1
        assert result.to_str(alphabet_2) == "111"

    def test6(self):
        start = Number.from_str("11", alphabet=alphabet_10)
        end = Number.from_str("99", alphabet=alphabet_10)
        while start != end + 1:
            print(start.to_str(alphabet=alphabet_10))
            start += 1

