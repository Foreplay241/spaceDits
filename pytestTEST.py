import pytest


class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_two(self, y):
        x = "that"
        assert y in x


def func(x):
    return x + 1


def test_answer(x):
    assert func(x) == 5


for i in range(10):
    print(func(i))
    assert func(i) < 11

tc = TestClass()
tc.test_two('t')

