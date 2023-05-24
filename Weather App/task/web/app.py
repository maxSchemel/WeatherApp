from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weather.db"
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    state = db.Column(db.String(40))
    temperature = db.Column(db.Integer)

    def __init__(self, name, state, temperature):
        self.name = name
        self.state = state
        self.temperature = temperature

#View Functions
@app.route('/')
def index():
    weathers = City.query.all()
    return render_template('index.html', City=weathers)

@app.route('/add', methods=['GET', 'POST'])
def load_city():
    if request.method == 'POST':
        if City.query.filter(City.name == request.form["city_name"]).first():
            print('already in database')
            return redirect(url_for('index'))
        city_weather = City(request.form["city_name"], "Warm", 25)
        db.session.add(city_weather)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == 'GET':
        return redirect(url_for('index'))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()


