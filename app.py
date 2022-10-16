from unittest import result
from flask import Flask, request, render_template
from utils import *
app = Flask(__name__, template_folder='./templates', static_folder='./static')
from keras.models import model_from_json


diseases = {0.1:	"Dengue",
0.2	:'Malaria',
0.3	:'Typhoid',
0.4	:'Jaundice',
0.5	:'Covid',
}

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model.h5")

@app.route("/", methods=["GET"])
def home():
    return render_template('main.html')

@app.route("/form")
def form():
    return render_template('form.html')

@app.route("/submit_diseases", methods=["POST"])
def post_form():
    received_symptoms = request.form
    symptoms = convert_symptoms_in_desired_format(received_symptoms)
    conse = loaded_model.predict([list(symptoms.values())])
    try:
        conse = diseases[round(conse[0][0],1)]
    except:
        conse = "Your Disease can't be identified"
    return render_template('form.html',result=f"{conse}")


if __name__ == '__main__':
    PORT = 5000
    print("Server up and running on port", PORT)
    app.run(debug=True, port=PORT)
