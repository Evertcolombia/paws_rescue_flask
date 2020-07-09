from flask import Flask, render_template, abort, session, redirect, url_for
from app.forms import LoginForm, SignupForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'
# Initialize db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///paws.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#create db object
db = SQLAlchemy(app)


""" model for pet """
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    age = db.Column(db.String)
    bio = db.Column(db.String)
    posted_by = db.Column(db.String, db.ForeignKey('user.id'))


""" model for user """
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column( db.String)
    pets = db.relationship('Pet', backref='user')


db.create_all()

# Create "team" user and add it to session
team = User(full_name = "Pet Rescue Team", email = "team@petrescue.co", password = "adminpass")
db.session.add(team)

nelly = Pet(name = "Nelly", age = "5 weeks", bio = "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles.")
yuki = Pet(name = "Yuki", age = "8 months", bio = "I am a handsome gentle-cat. I like to dress up in bow ties.")
basker = Pet(name = "Basker", age =  "1 year", bio =  "I love barking. But, I love my friends more.")
mr_furrikis = Pet(name = "Mr. Furrkins", age = "5 years", bio =  "Probably napping.")

db.session.add(nelly)
db.session.add(yuki)
db.session.add(basker)
db.session.add(mr_furrikis)

try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
finally:
    db.session.close()

@app.route("/")
def home():
    pets = Pet.query.all()
    print(pets)
    return render_template("home.html", pets=pets)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/details/<int:pet_id>")
def details(pet_id):
    #pet = next((pet for pet in pets if pet["id"] == pet_id), None)
    pet = Pet.query.get(pet_id)
    if pet is None:
        print("none")
        abort(404, description="No Pet was Found with the given ID")
    return render_template("details.html", pet=pet)


@app.route("/signup", methods=["POST", "GET",])
def signup_render():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(full_name = form.full_name.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form=form, message="This email already exists in the system! Please log in instead")
        finally:
            db.session.close()
        return render_template("signup.html", message="Successfully Sign Up")
    return render_template("signup.html", form = form)


@app.route("/login", methods=["GET", "POST"])
def login_render():
    form = LoginForm()
    if form.validate_on_submit():
        #user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, message ="Wrong credentials. Please try again.")
        else:
            session['user'] = user.id
            return render_template("login.html", message = "Successfully Logged In!")
    return render_template("login.html", form = form)


@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('login_render', _external=True))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
