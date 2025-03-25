import pytest
from appnew import Calculator


@pytest.fixture
def calc():
    """Фікстура для ініціалізації об'єкта Calculator перед кожним тестом."""
    return Calculator()


# Тести для основних операцій
def test_addition(calc: Calculator):
    result = calc.calculate(5, 3, '+')
    assert result == "Результат: 8"


def test_subtraction(calc: Calculator):
    result = calc.calculate(10, 4, '-')
    assert result == "Результат: 6"


def test_multiplication(calc: Calculator):
    result = calc.calculate(6, 7, '*')
    assert result == "Результат: 42"


def test_division(calc: Calculator):
    result = calc.calculate(20, 5, '/')
    assert result == "Результат: 4.0"


# Тест на ділення на нуль (тепер через pytest.raises)
def test_division_by_zero():
    calc = Calculator()
    result = calc.calculate(10, 0, '/')
    assert result == "Помилка: Ділення на нуль!"


# Тест на невідому операцію
def test_unknown_operation(calc: Calculator):
    result = calc.calculate(5, 5, '%')
    assert result == "Невідома операція!"


# Тести граничних випадків
def test_large_numbers(calc: Calculator):
    result = calc.calculate(1000, 1000, '+')
    assert result == "Результат: 2000"


def test_negative_numbers(calc: Calculator):
    result = calc.calculate(-10, -30, '+')
    assert result == "Результат: -40"


def test_float_numbers(calc: Calculator):
    result = calc.calculate(3.5, 2.5, '+')
    assert result == "Результат: 6.0"


# Тест для перевірки результату як об'єкта
def test_result_storage(calc: Calculator):
    calc.calculate(5, 5, '+')
    assert calc.result == 10

    # Перевірка збереження результату між операціями
    calc.calculate(calc.result, 5, '*')
    assert calc.result == 50


# Тест перевірки обробки граничних значень
def test_boundary_values(calc: Calculator):
    # Перевірка нуля
    result = calc.calculate(0, 0, '+')
    assert result == "Результат: 0"

    # Перевірка нескінченності
    result = calc.calculate(float('inf'), 5, '+')
    assert result == "Результат: inf"


# Тест для перевірки типу результату
def test_result_type(calc: Calculator):
    calc.calculate(10, 2, '/')
    assert isinstance(calc.result, float)

    calc.calculate(10, 2, '+')
    assert isinstance(calc.result, int) or isinstance(calc.result, float)


def test_reset_function():
    calc = Calculator()  # Створюємо об'єкт
    calc.calculate(10, 5, '*')  # Виконуємо операцію
    assert calc.result == 50  # Перевіряємо проміжний результат
    calc.reset()  # Викликаємо reset()
    assert calc.result == 0  # Очікуємо, що результат скинувся


def test_additional_functionality(calc, capsys):
    calc.calculate(10, 5, '+')
    captured = capsys.readouterr()
    assert "Додатковий функціонал для +: 25" in captured.out

    calc.calculate(20, 5, '-')
    captured = capsys.readouterr()
    assert "Додатковий функціонал для -: 10" in captured.out


# Тест для перевірки _check_result_thresholds при перевищенні верхньої межі
def test_upper_threshold_check(calc, capsys):
    calc.calculate(60, 50, '+')
    captured = capsys.readouterr()
    assert "Результат більший за 100!" in captured.out


# Тест для перевірки _check_result_thresholds при перевищенні нижньої межі
def test_lower_threshold_check(calc, capsys):
    calc.calculate(-30, 30, '-')
    captured = capsys.readouterr()
    assert "Результат менший за -50!" in captured.out


# Тест для перевірки обробки послідовних операцій
def test_sequential_operations(calc):
    calc.calculate(10, 5, '+')
    assert calc.result == 15

    result = calc.calculate(calc.result, 3, '*')
    assert "Результат: 45" in result

    result = calc.calculate(calc.result, 9, '/')
    assert "Результат: 5.0" in result


# Тест для перевірки обробки екстремально малих чисел
def test_very_small_numbers(calc):
    result = calc.calculate(1e-10, 2e-10, '+')
    assert "Результат: 3e-10" in result or "Результат: 3.0e-10" in result


# Тест для перевірки комутативності операцій
def test_operation_commutativity(calc):
    result1 = calc.calculate(5, 10, '+')
    calc.reset()
    result2 = calc.calculate(10, 5, '+')

    # Додавання має бути комутативним
    assert result1 == result2

    result1 = calc.calculate(5, 10, '*')
    calc.reset()
    result2 = calc.calculate(10, 5, '*')

    # Множення має бути комутативним
    assert result1 == result2

    # А віднімання і ділення - ні
    result1 = calc.calculate(10, 5, '-')
    calc.reset()
    result2 = calc.calculate(5, 10, '-')
    assert result1 != result2


# Тест для перевірки обробки спеціальних значень (NaN)
def test_nan_handling(calc):
    import math

    # Тестуємо обробку NaN
    result = calc.calculate(float('nan'), 5, '+')
    # NaN не дорівнює NaN, тому перевіряємо через isnan
    assert "Результат: " in result
    assert math.isnan(calc.result)
