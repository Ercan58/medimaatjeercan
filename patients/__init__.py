import logging
import azure.functions as func
import json

from .db_patients import fetch_all_patients, fetch_multiple_patients, fetch_patient_by_id, insert_patient, insert_electronic_dossier, delete_patient_by_id, update_patient, check_if_coach_exists
from ..resources.authorization import check_authorization_by_scope
from ..resources.functions_shared import prepare_data, get_param

# Main function gets called when /api/patients is accesed. This function calls and executes the coresponding post/get/update/delete method
# Responds with a JSON/text http response
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Patients endpoint triggered, checking request method...')
    try:
        token = req.headers.get("Authorization")
        if(req.method == "GET" and check_authorization_by_scope(token, 'read')):
            return get_patients(req)
        elif(req.method == "POST" and check_authorization_by_scope(token, 'write')):
            return post_patient(req)
        elif(req.method == "DELETE" and check_authorization_by_scope(token, 'write')):
            return delete_patient(req)
        elif(req.method == "PUT" and check_authorization_by_scope(token, 'write')):
            return put_patient(req)
        else:
            return func.HttpResponse(f"You are not authorised to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(f"No valid token found", mimetype='text/plain', status_code=400)
    except ValueError:
        return func.HttpResponse(f"Token doesn't exist", mimetype='text/plain', status_code=400)

# GET a list of patients. Either a single patient by id, a specific number of patients or all the patients
def get_patients(req) -> func.HttpResponse:
    try:
        id = get_param(req, 'id')
        number_of_patients = get_param(req, 'number')
        if id:
            id = int(id)
            db_data = fetch_patient_by_id(id)
        elif number_of_patients:
            number_of_patients = int(number_of_patients)
            db_data = fetch_multiple_patients(number_of_patients)
        else:
            db_data = fetch_all_patients()
    except:
        return func.HttpResponse(f"Invalid parameter, not an int", mimetype='text/plain', status_code=412)
    
    if db_data:
        return func.HttpResponse(json.dumps(prepare_data(db_data, [['User'], ['Patient']]), indent=4, sort_keys=True, default=str), mimetype='JSON', status_code=200)
    else:
        return func.HttpResponse(f"No patients found", mimetype='text/plain', status_code=404)

# This method gets the post data (JSON) and inputs it into the db
def post_patient(req) -> func.HttpResponse:
    try:
        body = req.get_json()
        patient_user_id = body['patient_user_id']
        coach_user_id = body['coach_user_id']
        summary = body['electronic_dossier']['summary']
        iq = body['electronic_dossier']['iq']
        
        coach = check_if_coach_exists(coach_user_id)

        if coach:
            electronic_dossier_id = insert_electronic_dossier(summary, iq)
            insert_patient(patient_user_id, coach_user_id, electronic_dossier_id)
            return func.HttpResponse('Added entry to database.', status_code=200)
        else:
            return func.HttpResponse(f"No coach with this id exists", mimetype='text/plain', status_code=412)
    except ValueError:
        return func.HttpResponse(f"This call needs valid user data to post, please refer to the API documentation", mimetype='text/plain', status_code=412)

# This method removes a single patient along with its user and user_details records
def delete_patient(req) -> func.HttpResponse:
    try:
        id = get_param(req, 'id')
        id = int(id)
        delete_patient(id)
        return func.HttpResponse(f"Patient succesfully removed", mimetype='text/plain', status_code=200)
    except:
        return func.HttpResponse(f"Failed to remove", mimetype='text/plain', status_code=412)

# Updates an existing patient in the DB
# User_id and all the user info is required, detail_id is optional
def put_patient(req) -> func.HttpResponse:
    try:
        body = req.get_json()
        for item in body:
            patient_user_id = int(item['patient_user_id'])
            new_coach_user_id = int(item['new_coach_user_id'])
                
        # Check if supplied coach ID is an actual coach
        coach = check_if_coach_exists(new_coach_user_id)
        if not coach:
            return func.HttpResponse(f"No coach with this id exists", mimetype='text/plain', status_code=412)

    except ValueError:
        return func.HttpResponse(f"This call needs a patient_user_id and new_coach_user_id in the json request body", mimetype='text/plain', status_code=412)
        
    try:
        update_patient(patient_user_id, new_coach_user_id)
        return func.HttpResponse(f"New coach assigned succesfully", mimetype='text/plain', status_code=200)
    except:
        return func.HttpResponse(f"No patient with this ID has been found", mimetype='text/plain', status_code=404)