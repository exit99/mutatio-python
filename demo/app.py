import os
from flask_mutatio import MutatioEnvironment, TagGenerator
from flask import Flask, render_template


app = Flask('test_dummy')


TEMPLATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

taggen = TagGenerator()
taggen.create_tags(TEMPLATE_PATH)


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
