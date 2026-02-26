from flask import Flask, render_template, request

app = Flask(__name__)

# Учётные данные для входа (можно изменить)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

@app.route("/", methods=["GET", "POST"])
def login():
    """Страница с формой входа."""
    error = None
    show_link = False
    if request.method == "POST":
        # Получаем данные из формы
        username = request.form.get("username")
        password = request.form.get("password")
        # Проверяем правильность
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            show_link = True   # показываем ссылку на /me
        else:
            error = "Неверный логин или пароль"
    return render_template("login.html", error=error, show_link=show_link)

@app.route("/me")
def me():
    """Личная страница с приветствием."""
    # Замените "Анна" на своё имя
    name = "Анна"
    return render_template("index.html", name=name)

@app.route("/about")
def about():
    """Страница с тремя фактами."""
    facts = [
        "Я обожаю решать задачи на Python.",
        "Моё хобби – фотографировать природу.",
        "Мечтаю побывать в Японии."
    ]
    return render_template("about.html", facts=facts)

if __name__ == "__main__":
    app.run(debug=True)