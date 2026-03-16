from flask import Flask, session, request, flash, redirect, url_for, render_template
import os

app = Flask(__name__)
app.secret_key = "books_secret_key_2024"

VALID_USER = 'admin'
VALID_PASS = 'admin'

books = [
    {
        "id": 1,
        "title": "Война и мир",
        "category": "Роман",
        "author": "Лев Толстой",
        "description": "Эпическое произведение о жизни русского общества в эпоху наполеоновских войн."
    },
    {
        "id": 2,
        "title": "Преступление и наказание",
        "category": "Роман",
        "author": "Федор Достоевский",
        "description": "Философско-психологический роман о студенте, совершившем убийство."
    },
    {
        "id": 3,
        "title": "Мастер и Маргарита",
        "category": "Роман",
        "author": "Михаил Булгаков",
        "description": "Мистический роман о визите дьявола в советскую Москву."
    },
    {
        "id": 4,
        "title": "Евгений Онегин",
        "category": "Поэма",
        "author": "Александр Пушкин",
        "description": "Роман в стихах о жизни молодого дворянина."
    },
    {
        "id": 5,
        "title": "Мертвые души",
        "category": "Поэма",
        "author": "Николай Гоголь",
        "description": "Произведение о похождениях Чичикова, скупающего мертвые души крепостных."
    }
]

def get_next_id():
    if books:
        return max(book['id'] for book in books) + 1
    return 1


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books_list():
    return render_template('books_list.html', books=books)

@app.route('/books/<int:book_id>')
def book_detail(book_id):
    # Ищем книгу по ID
    book = None
    for item in books:
        if item['id'] == book_id:
            book = item
            break

    if book is None:
        flash('Книга не найдена', 'danger')
        return redirect(url_for('books_list'))

    return render_template('book_detail', book=book)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    # Проверка авторизации
    if 'username' not in session:
        flash('Сначала войдите в систему!', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        author = request.form.get('author', '').strip()
        description = request.form.get('description', '').strip()

        if not title or not category or not author or not description:
            flash('Все поля должны быть заполнены!', 'warning')
            return redirect(request.url)

        new_book = {
            'id': get_next_id(),
            'title': title,
            'category': category,
            'author': author,
            'description': description
        }

        books.append(new_book)
        flash('Книга успешно добавлена!', 'success')
        return redirect(url_for('books_list'))

    return render_template('add_book.html')

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    if 'username' not in session:
        flash('Сначала войдите в систему!', 'warning')
        return redirect(url_for('login'))

    for i, book in enumerate(books):
        if book['id'] == book_id:
            deleted_book = books.pop(i)
            flash(f'Книга "{deleted_book["title"]}" удалена', 'success')
            break

    return redirect(url_for('books_list'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == VALID_USER and password == VALID_PASS:
            session['username'] = username
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('add_book'))
        else:
            flash('Неверный логин или пароль!', 'danger')

    return render_template('login')

@app.route('/profile')
def profile():
    if 'username' not in session:
        flash('Сначала войдите в систему!', 'warning')
        return redirect(url_for('login'))

    total_books = len(books)

    return render_template('profile',
                           username=session['username'],
                           total_books=total_books)

@app.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)