from flask import Flask, render_template, request
import re
from ml_logic import predict
app = Flask(__name__)

# Nuorodos į gėlyčių nuotraukas

virginica_url = \
    'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Iris_virginica_2.jpg/220px-Iris_virginica_2.jpg'
setosa_url = \
    'https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kosaciec_szczecinkowaty_Iris_setosa.jpg/220px-Kosaciec_szczecinkowaty_Iris_setosa.jpg'
versicolor_url = \
    'https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Blue_Flag%2C_Ottawa.jpg/220px-Blue_Flag%2C_Ottawa.jpg'

# regex validacija

def validate_inputs(*args):
    valid_form = re.compile(r'\b[0-9]\.[0-9]\b')
    res = valid_form.findall(' '.join(args))
    print(res)
    if len(res) == 4:
        return True
    return False

# Pagr. Flasko funkcija. Išgaudome kintamuosius iš web-formos. Praleidžiame per regexo funkciją,
# Jeigu nepraeina validacijos, vietoj prediction dedame klaidą. Jeigu praeina, naudojame iš kito failo
# importuotą funkciją predict. Priklausomai nuo jos atsakymo, parenkame paveikslėlio nuorodą. Perduodame
# rezultatus į template'ą.

@app.route('/', methods=['POST', 'GET'])
def index():
    picture = False
    pred = False
    if request.method == 'POST':
        sl = request.form['sepalL']
        sw = request.form['sepalW']
        pl = request.form['petalL']
        pw = request.form['petalW']
        if not validate_inputs(sl, sw, pl, pw):
            pred = 'Please provide values in float format, ex. "0.5", "5.0", etc.'
            picture = ''
        else:
            pred = predict(sl, sw, pl, pw)
            if pred == 'virginica':
                picture = virginica_url
            elif pred == 'versicolor':
                picture = versicolor_url
            else:
                picture = setosa_url
    return render_template('predictor.html', pred=pred, picture=picture)


if __name__ == "main":
    app.run(debug=True)