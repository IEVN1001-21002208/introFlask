from flask import Flask, render_template, request
 
app = Flask(__name__)
 
@app.route('/')
def index():
    titulo = "PWA"
    lista = ["pedro", "luis", "pablo"]
    return render_template("index.html", titulo=titulo, lista=lista)
 
@app.route("/hola")
def func():
    return " Hola ..."
 
@app.route("/user/<string:user>")
def user(user):
    return " Hola: " + user
 
@app.route("/numero/<int:n>")
def numero(n):
    return " Numero: {}".format(n)
 
@app.route("/user/<int:id>/<string:username>")
def username(id, username):
    return "ID: {} nombre: {}".format(id, username)
 
@app.route("/suma/<float:n1>/<float:n2>")
def suma(n1, n2):
    return "la suma es: {}".format(n1 + n2)
 
@app.route("/distancia")
def distancia():
    return render_template("distancia.html")
 
@app.route("/operasBas", methods=["GET", "POST"])
def operaBas():
    n1 = 0
    n2 = 0
    res = 0
   
    if request.method == 'POST':
        n1 = float(request.form.get('n1', 0))
        n2 = float(request.form.get('n2', 0))
        operacion = request.form.get('operacion')
       
        if operacion == 'sumar':
            res = n1 + n2
        elif operacion == 'restar':
            res = n1 - n2
        elif operacion == 'multiplicar':
            res = n1 * n2
 
    return render_template("operasBas.html", n1=n1, n2=n2, res=res)
 
if __name__ == "__main__":
    app.run(debug=True)