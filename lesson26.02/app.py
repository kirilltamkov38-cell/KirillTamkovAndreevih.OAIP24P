from flask import Flask
app = Flask(__name__)

@app.route('/<float:r>')
def index(r):
    pi = 3.14
    return render_template('index.html', r=r, pi=pi)

if __name__ == '__main__':
    app.run(debug=True)