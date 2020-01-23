from flask import Flask, request, render_template
app = Flask(__name__)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        vardas = request.form['vardas']
        return render_template("greetings.html", vardas=vardas)
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)