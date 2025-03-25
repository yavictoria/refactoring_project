import os, sys, random, time  # Зайві імпорти
from flask import Flask, render_template, request

app = Flask(__name__)

GLOBAL_VAR = 9999  # Безглузда глобальна змінна


class Lmao:
    def __init__(self):
        self.r = 0  # Погана назва змінної
        self.unused = "нічого"


    def do_math(self, xXx, yYy, lol123):

        temp = 0
        result_list = []

        if lol123 == '+':
            temp = xXx + yYy
            self.r = temp
        elif lol123 == '-':
            temp = xXx - yYy
            self.r = temp
        elif lol123 == '*':
            temp = xXx * yYy
            self.r = temp
        elif lol123 == '/':
            try:
                temp = xXx / yYy
                self.r = temp
            except:
                return "ПОМИЛКА!111"
        else:
            return None


        if lol123 == '+':
            print("Додавання", self.r)
            print("Додавання", self.r)
            print("Додавання", self.r)
        elif lol123 == '-':
            print("Віднімання", self.r)


        if self.r > 10:
            if self.r > 20:
                if self.r > 30:
                    print("OMG БІЛЬШЕ 30!!!")


        if self.r != self.r:
            print("НІКОЛИ НЕ ВИКОНАЄТЬСЯ")

        return self.r  # Це повертає значення, але в більшості випадків код може нічого не повертати


@app.route("/", methods=["GET", "POST"])
def kek():
    res = None  # Погане ім'я змінної
    if request.method == "POST":
        n1 = request.form["num1"]
        n2 = request.form["num2"]
        o = request.form["operation"]

        try:
            n1 = float(n1)
            n2 = float(n2)
        except:
            res = "ЧИСЛА ДАВАЙ СЮДИ!"
            return render_template("index.html", result=res)

        # Створюємо 2 екземпляри одного класу (непотрібно)
        obj1 = Lmao()
        obj2 = Lmao()
        obj1.do_math(n1, n2, o)
        res = obj2.do_math(n1, n2, o)  # Чому тут другий об'єкт? Бо ніфіга

        # Безглузді вкладені if'и
        if res:
            if res > 0:
                if res > 50:
                    res = "МЕГА ЧИСЛО!"
                else:
                    res = "Норм"
            else:
                res = "Погане число"
        else:
            res = "ЩОСЬ НЕ ТАК!"

        # Додаємо зайвий поворот у логіці
        res = str(res)
        res = res[::-1]  # Реверсуємо результат, бо чому б і ні?

    return render_template("index.html", result=res)


if __name__ == "__main__":
    app.run(debug=True)  # Додаємо неправильний відступ
