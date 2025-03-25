import pytest
from app import Calculator


# Тести для основних операцій
def test_addition():
    calc = Calculator()
    result = calc.calculate(5, 3, '+')
    assert "Результат: 8" in result


def test_subtraction():
    calc = Calculator()
    result = calc.calculate(10, 4, '-')
    assert "Результат: 6" in result


def test_multiplication():
    calc = Calculator()
    result = calc.calculate(6, 7, '*')
    assert "Результат: 42" in result


def test_division():
    calc = Calculator()
    result = calc.calculate(20, 5, '/')
    assert "Результат: 4.0" in result


# Тест на ділення на нуль
def test_division_by_zero():
    calc = Calculator()
    result = calc.calculate(10, 0, '/')
    assert "Помилка: Ділення на нуль!" in result


# Тест на невідому операцію
def test_unknown_operation():
    calc = Calculator()
    result = calc.calculate(5, 5, '%')
    assert "Невідома операція!" in result


# Тести граничних випадків
def test_large_numbers():
    calc = Calculator()
    result = calc.calculate(1000, 1000, '+')
    assert "Результат: 2000" in result


def test_negative_numbers():
    calc = Calculator()
    result = calc.calculate(-10, -30, '+')
    assert "Результат: -40" in result


def test_float_numbers():
    calc = Calculator()
    result = calc.calculate(3.5, 2.5, '+')
    assert "Результат: 6.0" in result


# Тест для перевірки результату як об'єкта
def test_result_storage():
    calc = Calculator()
    calc.calculate(5, 5, '+')
    assert calc.result == 10

    # Перевірка збереження результату між операціями
    calc.calculate(calc.result, 5, '*')
    assert calc.result == 50


# Тест перевірки обробки граничних значень
def test_boundary_values():
    calc = Calculator()
    # Перевірка нуля
    result = calc.calculate(0, 0, '+')
    assert "Результат: 0" in result

    # Перевірка нескінченності
    result = calc.calculate(float('inf'), 5, '+')
    assert "Результат: inf" in result


# Тест для перевірки типу результату
def test_result_type():
    calc = Calculator()
    calc.calculate(10, 2, '/')
    assert isinstance(calc.result, float)

    calc.calculate(10, 2, '+')
    assert isinstance(calc.result, int) or isinstance(calc.result, float)