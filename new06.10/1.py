from flask import Flask, render_template

app = Flask(__name__)

movies = [
    {
        "id": 1,
        "title": "Пила",
        "year": 2004,
        "rating": 7.6,
        "genre": "Хоррор",
        "description": "Двое незнакомцев просыпаются в запертой комнате и узнают, что стали участниками смертельной игры Конструктора."
    },
    {
        "id": 2,
        "title": "Крик",
        "year": 1996,
        "rating": 7.4,
        "genre": "Хоррор",
        "description": "Серийный убийца в маске Призрачного лица терроризирует подростков городка Вудсборо, знающих правила фильмов ужасов."
    },
    {
        "id": 3,
        "title": "Хэллоуин",
        "year": 1978,
        "rating": 7.7,
        "genre": "Хоррор",
        "description": "Маньяк Майкл Майерс сбегает из психиатрической лечебницы и возвращается в родной город, чтобы продолжить кровавую расправу."
    },
    {
        "id": 4,
        "title": "Кошмар на улице Вязов",
        "year": 1984,
        "rating": 7.5,
        "genre": "Хоррор",
        "description": "Фредди Крюгер — маньяк, убивающий подростков в их снах, где жертвы не могут найти спасения."
    },
    {
        "id": 5,
        "title": "Оно",
        "year": 2017,
        "rating": 7.3,
        "genre": "Хоррор",
        "description": "Группа детей из городка Дерри сталкивается с древним злом, принимающим облик клоуна Пеннивайза."
    }
]

@app.route("/")
def index():
    return render_template("index.html", movies=movies)

@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    for movie in movies:
        if movie["id"] == movie_id:
            return render_template("movie.html", movie=movie)
    return "Фильм не найден", 404

if __name__ == "__main__":
    app.run(debug=True)
