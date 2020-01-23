# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:46:27 2019

@author: Donoras
"""

# 1 Paprasčiausias variantas:

# from flask import Flask
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#    return "Čia mano naujas puslapis <h1></h1>"
#
# if __name__ == "__main__":
#    app.run()

# http://127.0.0.1:5000/


# 2 su kintamojo aptaizdavimu:

# from flask import Flask
# app = Flask(__name__)
#
#
# @app.route("/")
# def home():
#    return "Čia mano naujas puslapis <h1>LABAS</h1>"
#
#
# @app.route("/<name>")
# def user(name):
#    return f"Labas, {name}"
#
# if __name__ == "__main__":
#    app.run()

# http://127.0.0.1:5000/Donatas


# template naudojimas

# from flask import Flask, render_template
#
# app = Flask(__name__)


# @app.route("/")
# def home():
#     return render_template("home.html")


# @app.route("/<name>")
# def hello(name):
#     return render_template("hello.html", vardas=name)
#
#
# if __name__ == "__main__":
#     app.run()

# http://127.0.0.1:5000/Donatas


# 4 gražinimas į puslapį

# from flask import Flask, request, render_template
# app = Flask(__name__)
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#    if request.method == "POST":
#        vardas = request.form['vardas']
#        return render_template("greetings.html", vardas=vardas)
#        # return redirect(url_for("greetings", vardas=vardas))
#    else:
#        return render_template("login.html")
#
# if __name__ == "__main__":
#    app.run()

# Slačiavimai šablone:

# from flask import Flask, render_template
# app = Flask(__name__)
#
# @app.route("/")
# def home():
#    return render_template("skaiciavimai.html")
#
# if __name__ == "__main__":
#    app.run()


# Sarašas šablone:

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
   return render_template("sarasas.html", sarasas = ["Tomas", "Jonas", "Domas"])

if __name__ == "__main__":
   app.run()