from flask import Flask, render_template
from flask_admin import Admin, BaseView, expose
from flask_mutatio import Mutatio, dashboard_template

app = Flask(__name__)


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render(app.config.get('MUTATIO_ADMIN', dashboard_template))


admin = Admin(app)
admin.add_view(MyView(name='Hello'))


app = Flask('test_dummy')

admin = Admin(app)

mutatio = Mutatio()
mutatio.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
