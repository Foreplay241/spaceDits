import mathlib


# def test_calc_addition():
#     output = mathlib.calc_addition(2, 4)
#     assert output == 6
#
#
# def test_calc_multiply():
#     output = mathlib.calc_multiply(2, 4)
#     assert output == 8
#
#
# def test_calc_subtraction():
#     output = mathlib.calc_subtraction(2, 4)
#     assert output == -2
#
#
# def test_area():
#     output = mathlib.area_of_rectangle(2, 5)
#     assert output == 10
#
#
# def test_perimeter():
#     output = mathlib.perimeter_of_rectangle(2, 5)
#     assert output == 14


def test_total_divisible_by_6(input_total):
    assert input_total % 5 == 0


def test_total_divisible_by_15(input_total):
    assert input_total % 5 == 0


def test_total_divisible_by_9(input_total):
    assert input_total % 5 == 0
