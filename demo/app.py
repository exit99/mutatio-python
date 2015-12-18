import os

from flask import Flask, render_template
from flask.ext import assets
from flask_mutatio import Mutatio

app = Flask(__name__)

app = Flask('test_dummy')
app.config['DEBUG'] = True
app.config['MUTATIO_PORT'] = 27018
app.config['MUTATIO_TEMPLATE_TAGS'] = ('{@', '@}')

env = assets.Environment(app)
env.load_path = [
    os.path.join(os.path.dirname(__file__), 'static'),
    os.path.join(os.path.dirname(__file__), 'node_modules'),
]
env.register(
    'js_all',
    assets.Bundle(
        'jquery/dist/jquery.min.js',
        'js/bootstrap.min.js',
        assets.Bundle(
            'coffee/dashboard.coffee',
            filters=['coffeescript']
         ),
         output='js_all.js'
    )
)
env.register(
    'css_all',
    assets.Bundle(
        'css/bootstrap.min.css',
        'css/font-awesome.min.css',
         output='css_all.css',
    )
)
mutatio = Mutatio()
mutatio.init_app(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
