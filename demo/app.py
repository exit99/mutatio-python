from flask import Flask, render_template
from flask_mutatio import Mutatio

app = Flask(__name__)

app = Flask('test_dummy')
app.config['DEBUG'] = True

mutatio = Mutatio()
mutatio.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
