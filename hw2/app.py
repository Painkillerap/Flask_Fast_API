from flask import Flask, make_response, redirect, request, session, url_for
from flask import render_template

app = Flask(__name__)

app.secret_key = '5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


# -----------------------
# Задание №1

# Создать страницу, на которой будет кнопка "Нажми меня", при
# нажатии на которую будет переход на другую страницу с
# приветствием пользователя по имени.

@app.route("/")
@app.route('/page-main/')
def page_main():
    context = {'title': 'Главная страница'}
    return render_template('page-main.html', **context)


@app.route('/page-2/')
def page_2():
    context = {'title': 'Страница 2'}
    return render_template('page-2.html', **context)


# -----------------------
# Задание №2

# Создать страницу, на которой будет изображение и ссылка на другую страницу,
# на которой будет отображаться форма для загрузки изображений.

@app.get('/page-3/')
def load_image():
    context = {'title': 'Загрузка изображения'}
    return render_template('page-3.html', **context)


@app.post('/page-3/')
def upload():
    if request.method == "POST":
        f = request.files["file"]
        print(f)
    return 'Изображение загружено!'


# -----------------------
# Задание №3

# Создать страницу, на которой будет форма для ввода логина и пароля.
# При нажатии на кнопку "Отправить" будет произведена проверка соответствия логина
# и пароля и переход на страницу приветствия пользователя или страницу с ошибкой.

@app.route('/login/', methods=["POST", "GET"])
def auth():
    if request.method == "POST":
        user_name = request.form.get("login")
        user_pass = request.form.get("password")
        if user_name == "admin" and user_pass == "qwerty":
            context = {'title': 'Успешная авторизация'}
            return render_template('page-4-succ.html', **context)
        context = {'title': 'Нет авторизации!!!'}
        return render_template('page-4-error.html', **context)
    context = {'title': 'Авторизация'}
    return render_template('page-4.html', **context)


# -----------------------
# Задание №4

# Создать страницу, на которой будет форма для ввода текста и кнопка "Отправить"
# При нажатии кнопки будет произведен подсчет количества слов в тексте и переход на страницу с результатом.

@app.route('/send_text/', methods=["POST", "GET"])
def send_text():
    if request.method == "POST":
        text = request.form.get("text")
        print(text)
        word_list = text.split()
        world_len = len(word_list)
        print(world_len)
        context = {'title': 'Подсчитываю...', 'world_len': world_len}
        return render_template('page-5-len.html', **context)
    context = {'title': 'Отправка текста'}
    return render_template('page-5.html', **context)


# -----------------------
# Задание №5

# Создать страницу, на которой будет форма для ввода двух чисел и выбор операции
# (сложение, вычитание, умножение или деление) и кнопка "Вычислить"
# При нажатии на кнопку будет произведено вычисление результата выбранной операции
# и переход на страницу с результатом.

@app.route('/calc/', methods=["POST", "GET"])
def calc():
    if request.method == "POST":
        num_1 = int(request.form.get("num_1"))
        num_2 = int(request.form.get("num_2"))
        operation = request.form.get("operation")
        if operation == "Сложение":
            result = num_1 + num_2
            operation_text = "сложения"
        elif operation == "Вычитание":
            result = num_1 - num_2
            operation_text = "вычитания"
        elif operation == "Умножение":
            result = num_1 * num_2
            operation_text = "умножения"
        elif operation == "Деление":
            if num_2 != 0:
                result = num_1 / num_2
            else:
                result = "нет решения! деление на ноль!!"
            operation_text = "деления"
        else:
            result = None

        context = {'title': 'Подсчитываю...', 'result': result, "operation_text": operation_text, "num_1": str(num_1), "num_2": str(num_2)}
        return render_template('page-6-result.html', **context)

    context = {'title': 'Калькулятор текста'}
    return render_template('page-6.html', **context)


# -----------------------
# Задание №6

# Создать страницу, на которой будет форма для ввода имени и возраста пользователя и кнопка "Отправить"
# При нажатии на кнопку будет произведена проверка возраста и переход на страницу с результатом или на
# страницу с ошибкой в случае некорректного возраста.

@app.route('/name_age/', methods=["POST", "GET"])
def name_age():
    if request.method == "POST":
        name = request.form.get("name")
        age = int(request.form.get("age"))
        context = {'title': 'Доступ...', 'name': name, 'age': age}
        if 18 <= age <= 60:
            return render_template('page-7-access.html', **context)
        else:
            return render_template('page-7-no-access.html', **context)

    context = {'title': 'Знакомство с пользователем'}
    return render_template('page-7.html', **context)


# -----------------------
# Задание №9

# Создать страницу, на которой будет форма для ввода имени и электронной почты
# При отправке которой будет создан cookie файл с данными пользователя
# Также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
# На странице приветствия должна быть кнопка "Выйти"
# При нажатии на кнопку будет удален cookie файл с данными пользователя и произведено
# перенаправление на страницу ввода имени и электронной почты.


@app.route('/name_email/', methods=["POST", "GET"])
def name_email():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        session['name'] = name
        session['email'] = email
        context = {'title': 'Доступ...', 'name': name, 'email': email}
        response = make_response(render_template('page-8-hello.html', **context))
        print(f'Session: name = {session.get("name")}, email = {session.get("email")}')
        return response
    context = {'title': 'Знакомство с пользователем'}
    return render_template('page-8.html', **context)


@app.route('/logout/')
def logout():
    print(" --- Сессия ---")
    print(f'Session: name = {session.get("name")}, email = {session.get("email")}')
    session.pop('name', None)
    session.pop('email', None)
    print(" --- Сессия завершена ! ---")
    print(f'Session: name = {session.get("name")}, email = {session.get("email")}')
    return redirect(url_for('name_email'))


# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
