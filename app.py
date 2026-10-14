from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    titulo = "PWA"
    lista = ["Pedro", "Luis", "Paco"]
    return render_template("index.html", titulo = titulo, lista = lista)


@app.route("/Hola")
def func():
    return "Hola Tonotos"


@app.route("/user/<string:user>")
def user(user):
    return f"Holaaa {user}"


@app.route("/numero/<int:n>")
def numero(n):
    return f"Número: {n}"


@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return f"ID: {id} nombre: {username}"


@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return f"La suma es: {n1 + n2}"


if __name__ == "__main__":
    app.run(debug=True)