"""
Flask-додаток для калькулятора.
Містить клас Calculator з базовими операціями \(^3^)/.
"""

from flask import Flask, render_template, request

app = Flask(__name__)

class Calculator:
    """Калькулятор, що підтримує базові арифметичні операції."""

    def __init__(self):
        """Ініціалізація калькулятора з початковим значенням результату."""
        self.result = 0

    def calculate(self, num1: float, num2: float, operation: str) -> str:
        """
        Виконує арифметичну операцію між двома числами.

        Args:
            num1 (float): Перше число.
            num2 (float): Друге число.
            operation (str): Операція ('+', '-', '*', '/').

        Returns:
            str: Результат операції або повідомлення про помилку.
        """
        operations = {
            '+': self._add,
            '-': self._subtract,
            '*': self._multiply,
            '/': self._divide
        }

        if operation not in operations:
            return "Невідома операція!"

        try:
            self.result = operations[operation](num1, num2)
            self._additional_functionality(operation)
            self._check_result_thresholds()
            return f"Результат: {self.result}"
        except ValueError as error:
            return str(error)

    def _add(self, num1: float, num2: float) -> float:
        """Додавання двох чисел."""
        return num1 + num2

    def _subtract(self, num1: float, num2: float) -> float:
        """Віднімання другого числа від першого."""
        return num1 - num2

    def _multiply(self, num1: float, num2: float) -> float:
        """Множення двох чисел."""
        return num1 * num2

    def _divide(self, num1: float, num2: float) -> float:
        """Ділення першого числа на друге. Викликає помилку при діленні на нуль."""
        if num2 == 0:
            raise ValueError("Помилка: Ділення на нуль!")
        return num1 / num2

    def _additional_functionality(self, operation: str):
        """Додаткові обчислення для кожної операції."""
        additional_operations = {
            '+': lambda: self.result + 10,
            '-': lambda: self.result - 5,
            '*': lambda: self.result * 2,
            '/': lambda: self.result / 2
        }
        additional_result = additional_operations.get(operation, lambda: None)()
        if additional_result is not None:
            print(f"Додатковий функціонал для {operation}: {additional_result}")

    def _check_result_thresholds(self):
        """Перевіряє, чи виходить результат за визначені межі."""
        if self.result > 100:
            print("Результат більший за 100!")
        elif self.result < -50:
            print("Результат менший за -50!")

    def reset(self):
        """Скидає результат у 0."""
        self.result = 0


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Головна сторінка калькулятора.

    Returns:
        str: Рендеринг HTML-шаблону з результатом обчислення.
    """
    result = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operation = request.form["operation"]

            calc = Calculator()
            result = calc.calculate(num1, num2, operation)
        except (ValueError, KeyError):
            result = "Помилка у введених даних!"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
