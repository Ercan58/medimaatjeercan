import logging
import azure.functions as func
import json

from .db_electronic_dossier import fetch_electronic_dossier_by_id, fetch_patient_by_id, update_electronic_dossier_by_id, AlchemyEncoder
from ..resources.authorization import check_authorization_by_scope
from ..resources.functions_shared import prepare_data

# Main function gets called when /api/electronic_dossier is accessed. This function calls and executes the corresponding get and put methods
# Responds with a JSON/text http response
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Electronic dossier endpoint triggered, checking request method...')
    try:
        token = req.headers.get("Authorization")
        if(req.method == "GET" and check_authorization_by_scope(token, 'read')):
            return get_electronic_dossier(req)
        elif(req.method == "PUT" and check_authorization_by_scope(token, 'write')):
            return update_electronic_dossier(req)
        else:
            return func.HttpResponse(f"You are not authorised to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(f"No valid token found", mimetype='text/plain', status_code=400)
    except ValueError:
        return func.HttpResponse(f"Token doesn't exist", mimetype='text/plain', status_code=400)

# GET electronic dossier by patient ID
def get_electronic_dossier(req):
    try:
        id = int(req.route_params.get('id'))
        if id:
            ed_patient = fetch_patient_by_id(id)
            if ed_patient:
                electronic_dossier = fetch_electronic_dossier_by_id(id)
            else:
                return func.HttpResponse(f"No patient with this ID", mimetype='text/plain', status_code=412)
        else:
            return func.HttpResponse(f"Empty input recieved", mimetype='text/plain', status_code=412)
    except ValueError:
         return func.HttpResponse(f"Invalid input, not an int", mimetype='text/plain', status_code=412)
    
    if electronic_dossier:
        return func.HttpResponse(json.dumps(prepare_data(electronic_dossier, [['ElectronicDossier']]), indent=4, sort_keys=True), mimetype='JSON', status_code=200)
    else:
        return func.HttpResponse(f"No electronic dossier found for this patient", mimetype='text/plain', status_code=404)

# Updates an existing electronic_dossier in the DB
def update_electronic_dossier(req):
    try:
        body = req.get_json()
        for item in body:
            electronic_dossier_id = int(item['electronic_dossier_id'])
            new_iq = int(item['iq'])
            new_summary = item['summary']
                
        # Check if supplied electronic_dossier ID exists
        electronic_dossier = fetch_electronic_dossier_by_id(electronic_dossier_id)
        if not electronic_dossier:
            return func.HttpResponse(f"No electronic_dossier with this id exists", mimetype='text/plain', status_code=412)

    except ValueError:
        return func.HttpResponse(f"This call needs an electronic_dossier_id, iq and summary in the json request body", mimetype='text/plain', status_code=412)
        
    try:
        update_electronic_dossier_by_id(electronic_dossier_id, new_iq, new_summary)
        return func.HttpResponse(f"Electronic dossier updated succesfully", mimetype='text/plain', status_code=200)
    except:
        return func.HttpResponse(f"Something went wrong, contact support", mimetype='text/plain', status_code=400)