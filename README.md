# 🥗 Calorie Tracker

**Calorie Tracker** — це веб-застосунок, створений на Django, який дозволяє користувачам відслідковувати споживання калорій, білків, жирів та вуглеводів.  
Він включає інтерфейс додавання продуктів, графік співвідношення нутрієнтів та прогресбар з денною нормою калорій.

---

## ✨ Основний функціонал

- 🔐 Аутентифікація користувачів
- ➕ Додавання продуктів харчування з макроелементами
- 📊 Автоматичний розрахунок сумарних значень
- 📉 Графік співвідношення білків/жирів/вуглеводів (Chart.js)
- 📈 Прогресбар до 2000 калорій
- ❌ Видалення окремих продуктів
- ✅ Повна підтримка бази даних (SQLite) і збереження спожитого

---

## 🛠️ Стек технологій

- Django 5.1.5 (Python 3.12)
- HTML5 + Bootstrap 4
- Chart.js (v2.9.3)
- JavaScript (інлайн для обчислень)
- SQLite (вбудовано)

---

## 📁 Структура проєкту

<pre>
├── mysite/
│   ├── myapp/
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── myapp/
│   │   │       ├── index.html
│   │   │       └── delete.html
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── tests.py
│   │   └── ...
│   ├── mysite/
│   │   └── urls.py, settings.py, ...
│   └── manage.py
</pre>

---

## 🧪 Тестування

У проєкті реалізовано **20 модульних тестів** з покриттям:
- моделей `Food` та `Consume`
- представлень `index` і `delete`
- логіки додавання/видалення
- CSRF, форм, шаблонів, кнопок
- негативних кейсів

---

## ✅ Застосовані методи рефакторингу з прикладами

| №  | Метод                         | Файл         | Рядки (приблизно) | Пояснення                                                                 |
|----|-------------------------------|--------------|--------------------|---------------------------------------------------------------------------|
| 1  | Rename Variable               | `views.py`   | ~23               | `def delete_consume(request, consume_id)` — зміна `id` на `consume_id`   |
| 2  | Reorder Imports               | `views.py`   | 1–5               | Django-імпорти (`login_required`) переміщено над локальними (`.models`)  |
| 3  | Remove Unused Variable        | `tests.py`   | ~50               | Видалено `response = ...`, яке не використовувалось                      |
| 4  | Replace `.format()` → f-string| `tests.py`, `views.py` | ~65, ~24 | Заміна `format()` на f-string у `reverse('delete', args=[...])`         |
| 5  | Add Docstrings                | `tests.py`, `views.py`, `models.py` | по всьому файлу | Додані описи `"""Test that ..."""` у кожному класі та методі             |
| 6  | Improve Naming                | `tests.py`   | ~10–110           | `test_logged_in_delete_food`, `test_add_nonexistent_food` тощо           |
| 7  | Refactor Inline JS           | `index.html` | `<script>` внизу | Винесено змінні `carbs`, `calories`, `carbsP`, `fatsP` тощо в окремі блоки |
| 8  | Refactor Layout (frontend)   | `index.html` | вся структура     | Використано `container`, `row`, `col-12`, `col-lg-5` для адаптивності    |
| 9  | Split Responsibilities        | `views.py`   | 7–25              | У `index()` чітко розділено логіку `POST` і `GET`                        |
| 10 | Positioning CSS out of HTML  | `index.html` | `<style>` у `<head>` | `#progress-text` перенесено зі `style="..."` у CSS                       |

---

## 💡 Обґрунтування методів рефакторингу

Кожна техніка була обрана відповідно до проблем у вихідному коді.  
Наведемо приклади:

- **Rename Variable**: зміна `id` на `consume_id` усунула неявний конфлікт з вбудованими іменами.
- **Split Responsibilities**: розділення логіки GET/POST покращило модульність і дозволило простіше тестувати.
- **Docstrings**: тепер кожен тест має опис, що полегшує підтримку.
- **F-string замість .format()**: сучасніша синтаксична конструкція, що спрощує вирази.

> Повний список див. у таблиці вище.

---

## 📏 Результати рефакторингу

| Метрика                         | До  | Після |
|--------------------------------|-----|-------|
| `pylint` оцінка якості         | 0.43/10 | 9.46/10 |
| Модульні тести                 | 0   | 20     |
| Видалено зайвий JS код         | ❌  | ✅     |
| CSS інлайновий → структурований| ❌  | ✅     |
| Docstrings                     | ❌  | ✅     |
| Адаптивність фронтенду        | ❌  | ✅     |
| Іменування змінних             | неосмислене | зрозуміле |

---

## 📌 Діаграма

![image](https://github.com/user-attachments/assets/b8ce1009-6c25-4e3e-bab1-e1e6628ea94f)

---

## Зображення додатку

Було:
![image](https://github.com/user-attachments/assets/afd04731-b4b8-4eb9-bf04-ed31d6cb6218)
![image](https://github.com/user-attachments/assets/d3b3850e-59a7-4c6d-9455-b240cc18e563)

Стало:
![image](https://github.com/user-attachments/assets/0a1c6227-4ff2-4e07-8304-7bb6b0513aea)
![image](https://github.com/user-attachments/assets/6f2b423c-bcf7-407e-b003-09aad825b8cc)

---

## 📌 Висновки

Завдяки застосуванню технік рефакторингу, проєкт став:

- легшим для підтримки
- кращим у тестуванні
- зручнішим для масштабування
- з високим рівнем автоматичної перевірки (pylint)

Всі цілі проекту досягнуті, функціональність не порушена.

---

