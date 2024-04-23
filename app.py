from flask import Flask, render_template
app = Flask("__name__")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quemsomos")
def quem_somos():
    return render_template("quemsomos.html")

@app.route("/cadastro")
def contatos():
    return render_template("cadastro.html")