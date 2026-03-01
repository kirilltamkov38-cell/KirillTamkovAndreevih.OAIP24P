from flask import Flask, render_template

app = Flask(__name__)

@app.route('/<float:num1>/<op>/<float:num2>/')
def calculator(num1, op, num2):
    return render_template('index.html', num1=num1, num2=num2, operation=op)

if __name__ == '__main__':
    app.run(debug=True)