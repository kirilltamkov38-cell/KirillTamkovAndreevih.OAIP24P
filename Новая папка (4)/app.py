from flask import Flask, session, request, flash, redirect, url_for, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "arbuz52"

VALID_USER = 'student'
VALID_PASS = 'cerber666'
UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'ico', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

images_data = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html', images = images_data)

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('Файл не загружен', 'danger')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == "":
            flash("Файл не выбран", 'warning')
            return redirect(request.url)

        caption = request.form.get('caption', 'Без подписи')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            images_data.append({
                'filename': filename,
                'caption': caption
            })

            flash('Файл успешно загружен', 'success')
            return redirect(url_for('index'))
        else:
            flash("Недопустимый тип файла", "danger")
            return redirect(request.url)
    return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<int:index>')
def delete_file(index):
    if 0 <= index < len(images_data):
        removed = images_data.pop(index)
        flash('Фото удалено', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')

        if user == VALID_USER and password == VALID_PASS:
            session['username'] = user
            flash("Вы успешно вошли!", 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверный логин или пароль', 'danger')

    return  render_template("login.html")

@app.route("/profile")
def profile():
    if "username" not in session:
        flash("Сначала войдите в систему!", 'warning')
        return redirect(url_for('login'))

    return render_template("profile.html", name=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)