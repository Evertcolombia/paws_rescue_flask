from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "hello world"

@app.route("/educative")
def learn():
    return "happy Learning at educative!"

@app.route("/<my_name>")
def greatings(my_name):
    return "Welcome " + my_name + "!"

@app.route('/square/<int:number>')
def show_square(number):
    square = str(number * number)
    return "Square of " + str(number) + " is: " + square + "!"

if __name__ == "__main__":
    # Onlyfor debuggin while developming
    app.run(host='0.0.0.0', debug=True, port="5000")
