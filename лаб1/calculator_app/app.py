from flask import Flask, render_template, request

app = Flask(__name__)

class Calculator:
    def __init__(self):
        self.result = 0

    def calculate(self, num1, num2, operation):
        if operation == '+':
            self.result = num1 + num2
        elif operation == '-':
            self.result = num1 - num2
        elif operation == '*':
            self.result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                return "Помилка: Ділення на нуль!"
            self.result = num1 / num2
        else:
            return "Невідома операція!"

        # Дублювання коду для "додаткового функціоналу"
        if operation == '+':
            print("Додатковий функціонал для додавання: результат + 10 =", self.result + 10)
        elif operation == '-':
            print("Додатковий функціонал для віднімання: результат - 5 =", self.result - 5)
        elif operation == '*':
            print("Додатковий функціонал для множення: результат * 2 =", self.result * 2)
        elif operation == '/':
            print("Додатковий функціонал для ділення: результат / 2 =", self.result / 2)

        # Магічні числа
        if self.result > 100:
            print("Результат більший за 100!")
        elif self.result < -50:
            print("Результат менший за -50!")

        # Надмірна складність: непотрібні вкладені умови
        if operation == '+':
            if num1 > 10:
                if num2 > 10:
                    print("Обидва числа більші за 10!")
                else:
                    print("Перше число більше за 10, а друге ні!")
            else:
                if num2 > 10:
                    print("Друге число більше за 10, а перше ні!")
                else:
                    print("Обидва числа менші або рівні 10!")

        return f"Результат: {self.result}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        calc = Calculator()
        result = calc.calculate(num1, num2, operation)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)