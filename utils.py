def convert_symptoms_in_desired_format(received_symptoms):
    symptoms = {}
    for symptom in received_symptoms:
        symptoms[symptom] = 1 if received_symptoms[symptom].lower() == 'yes' else 0

    return symptoms