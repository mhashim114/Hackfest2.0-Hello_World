from flask import Flask, request, render_template
from utils import *
app = Flask(__name__, template_folder='./template', static_folder='./static')
# app = Flask(__name__)


@app.route("/submit_diseases", methods=["POST"])
def post_form():
    received_symptoms = request.form
    symptoms = convert_symptoms_in_desired_format(received_symptoms)
    return symptoms


@app.route("/", methods=["GET"])
def home():
    return render_template('main.html')

@app.route("/form")
def form():
    return render_template('form.html')


if __name__ == '__main__':
    PORT = 5000
    print("Server up and running on port", PORT)
    app.run(debug=True, port=PORT)

