from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


class CityWeather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), unique=True)
    state = db.Column(db.String(40))
    temperature = db.Column(db.Integer)

    def __init__(self, city_name, state, temperature):
        self.city_name = city_name
        self.state = state
        self.temperature = temperature

#View Functions
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def load_city():
    if request.method == 'POST':
        if db.session.query(db.exists().where(CityWeather.city_name==request.form["city_name"])):
            return render_template('index.html')
        city_weather = CityWeather(request.form["city_name"], "Warm", 25)
        db.session.add(city_weather)
        db.session.commit()
        return render_template('index.html')
    if request.method == 'GET':
        return render_template('index.html')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()


