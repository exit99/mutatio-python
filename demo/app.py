from flask_mutatio import Mutatio
from flask import Flask, render_template


app = Flask('test_dummy')

mutatio = Mutatio()
mutatio.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
