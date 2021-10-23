import pytest


# def calc_addition(a, b):
#     return a + b
#
#
# def calc_multiply(a, b):
#     return a * b
#
#
# def calc_subtraction(a, b):
#     return a - b
#
#
# def area_of_rectangle(width, height):
#     area = width * height
#     return area
#
#
# def perimeter_of_rectangle(width, height):
#     perimeter = 2 * (width + height)
#     return perimeter


def test_total_divisible_by_5(input_total):
    assert input_total % 5 == 0


def test_total_divisible_by_10(input_total):
    assert input_total % 10 == 0


def test_total_divisible_by_20(input_total):
    assert input_total % 20 == 0


def test_total_divisible_by_50(input_total):
    assert input_total % 50 == 0
