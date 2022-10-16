from keras.models import model_from_json
from unittest import result
from flask import Flask, request, render_template
from utils import *
app = Flask(__name__, template_folder='./templates', static_folder='./static')


diseases = {'0.1': "Dengue",
            '0.2': 'Malaria',
            '0.3': 'Typhoid',
            '0.4': 'Jaundice',
            '0.5': 'Covid',
            }

hospitals = {'Dengue': "Hashmanis Hospital, South City Hospital, Altamash General Hospital, Medicare Cardiac & General Hospital, Dr. Ziauddin Hospital (North Nazimabad), National Medical Centre (NMC), Darul Sehat Hospital, Patel Hospital, Saifee Hospital, Aga Khan University Hospital, Life Care International Hospital",
            'Malaria': "Zobia Hospital (G-9), MaxHealth Hospital, Shifa International Hospital Ltd, Ali Medical Center (Islamabad), Quaid-e-Azam International Hospital, Islamabad Specialist Clinic (F-8 Markaz), Kulsum International Hospital",
             'Typhoid' : "Hashmanis Hospital, South City Hospital, Altamash General Hospital, Medicare Cardiac & General Hospital, Dr. Ziauddin Hospital (North Nazimabad), National Medical Centre (NMC), Darul Sehat Hospital, Patel Hospital, Saifee Hospital, Aga Khan University Hospital, Life Care International Hospital",
            'Jaundice' : "Hashmanis Hospital, South City Hospital, Altamash General Hospital, Medicare Cardiac & General Hospital, Dr. Ziauddin Hospital (North Nazimabad), National Medical Centre (NMC), Darul Sehat Hospital, Patel Hospital, Saifee Hospital, Aga Khan University Hospital, Life Care International Hospital",
            'Covid': "Civil Hospital, Jinnah Postgraduate Medical Centre (JPMC), Karachi, Dow Hospital, Sheikh Zayed Hospital, Pakistan Institute of Medical Sciences (PIMS), Hayatabad Medical Complex, Allied Teaching Hospital, Bacha Khan Medical Complex, Shiekh Khalifa Bin Zaid (SKBZ) Hospital",  
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
    
    print(conse)
    try:
        disease = diseases[str(round(conse[0][0], 1))]
        hospitalss = hospitals[disease].replace(',','\n\n')
        message = f'''You may have {disease}.\n You can visit hospitals below:\n\n {hospitalss}'''
    except Exception as e:
        message = "Your Disease can't be identified"+str(e)
    return render_template('form.html', result=f"{message}")


if __name__ == '__main__':
    PORT = 5000
    print("Server up and running on port", PORT)
    app.run(debug=True, port=PORT)
