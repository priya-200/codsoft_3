from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import requests
from dotenv import load_dotenv
import os

API = os.getenv('API')
URL = 'http://api.weatherapi.com/v1/current.json'


class Form(FlaskForm):
    pincode = StringField(label='Enter The Place Name', validators=[DataRequired()])
    submit = SubmitField(label='Get Data')


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)
load_dotenv()


@app.route("/", methods=['POST', 'GET'])
def home():
    form = Form()
    if form.validate_on_submit():
        city = form.pincode.data
        return redirect(url_for('details', city=city))
    return render_template("index.html", form=form)


@app.route('/details/<city>',methods=['POST','GET'])
def details(city):
    parameters = {
        'key': API,
        'q': city,
        'api': 'no'
    }
    respond = requests.get(url=URL, params=parameters)
    if respond.status_code == 200:
        return render_template('details.html', response=respond.json())
    else:
        flash(f'Check the city that you entered')
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)