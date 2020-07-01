from flask import Flask, render_template, abort, request
from .forms import LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfewfew123213rwdsgert34tgfd1234trgf'

pets = [
    {"id": 1, "name": "Nelly", "age": "5 weeks", "bio": "I am a tiny kitten rescued by the good people at Paws Rescue Center. I love squeaky toys and cuddles."},
    {"id": 2, "name": "Yuki", "age": "8 months", "bio": "I am a handsome gentle-cat. I like to dress up in bow ties."},
    {"id": 3, "name": "Basker", "age": "1 year", "bio": "I love barking. But, I love my friends more."},
    {"id": 4, "name": "Mr. Furrkins", "age": "5 years", "bio": "Probably napping."},
]

users = {
    "archie.andrews@email.com": "football4life",
    "veronica.lodge@email.com": "fashiondiva"
}

@app.route("/")
def home():
    return render_template("home.html", pets=pets)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/details/<int:pet_id>")
def details(pet_id):
    pet = next((pet for pet in pets if pet["id"] == pet_id), None)
    if pet is None:
        print("none")
        abort(404, description="Custom Error Message")
    return render_template("details.html", pet=pet)

@app.route("/login", methods=["GET", "POST"])
def login_render():
    """
    if request.method == "POST":
        print(request)
        email = request.form["email"]
        password = request.form.get("password")
        print(email + ' ' + password)

        if (users[email] == password):
            return render_template("login.html", message ="Successfully Logged In")
        return render_template("login.html", message ="Incorrect Email or Password")
    return render_template("login.html")"""

    form = LoginForm ()
    """
    if form.is_submitted():
        print("submitted")
    if form.validate():
        print("valid")"""
    if form.validate_on_submit():
        for u_email, u_password in users.items():
            if (u_email == form.email.data and u_password == form.password.data):
                return render_template("login.html", message ="Successfully Logged In")
        return render_template("login.html", form = form, message ="Incorrect Email or Password")
    elif form.errors:
        print(form.errors.items())
    return render_template("login.html", form = form)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
