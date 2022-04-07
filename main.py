from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired, url
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CafeForm(FlaskForm):
    id_field = HiddenField()
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Map URL')
    img_url = StringField('Image Url')
    location = StringField('Location', validators=[DataRequired()])
    sockets = BooleanField('Has sockets')
    toilet = BooleanField('Has a public restroom')
    wifi = BooleanField('Has public wifi')
    calls = BooleanField('Can make calls')
    seats = StringField('How many seats does this cafe have?')
    coffee_price = StringField('How much is a cup of coffee?')
    submit = SubmitField('Submit')
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=True)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=False)

db.create_all()


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_cafe = Cafe(
            name=request.form.get('name'),
            map_url=request.form.get('map_url'),
            img_url=request.form.get('img_url'),
            location=request.form.get('location'),
            has_sockets=bool(request.form.get('sockets')),
            has_toilet=bool(request.form.get('toilet')),
            has_wifi=bool(request.form.get('wifi')),
            can_take_calls=bool(request.form.get('calls')),
            seats=request.form.get('seats'),
            coffee_price=request.form.get('coffee_price'),
        )
        db.session.add(new_cafe)
        db.session.commit()

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    cafe_places = db.session.query(Cafe).all()
    return render_template('cafes.html', cafes=cafe_places)


if __name__ == '__main__':
    app.run(debug=True)
