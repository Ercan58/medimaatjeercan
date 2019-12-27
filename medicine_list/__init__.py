import logging
import azure.functions as func
import json

from .db_medicine_list import fetch_medicine_list, fetch_patient_by_id, insert_medicine_per_patient, delete_medicine_per_patient
from ..resources.models import MedicinePerPatient
from ..resources.authorization import check_authorization_by_scope
from ..resources.functions_shared import prepare_data

# Main function gets called when /api/patients is accesed. This function calls and executes the coresponding post/get/update/delete method
# Responds with a JSON/text http response
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Medicine list endpoint triggered, checking request method...')
    try:
        token = req.headers.get("Authorization")
        if(req.method == "GET" and check_authorization_by_scope(token, 'read')):
            return get_medicine_list(req)
        elif(req.method == "POST" and check_authorization_by_scope(token, 'write')):
            return post_medicine_list(req)
        elif(req.method == "DELETE" and check_authorization_by_scope(token, 'write')):
            return delete_medicine_list(req)
        else:
            return func.HttpResponse(f"You are not authorised to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(f"No valid token found", mimetype='text/plain', status_code=400)
    except ValueError:
        return func.HttpResponse(f"Token doesn't exist", mimetype='text/plain', status_code=400)


# GET a list of patients. Either a single patient by id, a specific number of patients or all the patients
def get_medicine_list(req):
    try:
        id = int(req.route_params.get('id'))
        if id:
            ml_patient = fetch_patient_by_id(id)
            if ml_patient:
                medicine_list = fetch_medicine_list(id)
            else:
                return func.HttpResponse(f"No patient with this ID", mimetype='text/plain', status_code=412)
        else:
            return func.HttpResponse(f"Empty input recieved", mimetype='text/plain', status_code=412)
    except ValueError:
         return func.HttpResponse(f"Invalid input, not an int", mimetype='text/plain', status_code=412)
    
    if medicine_list:
        return func.HttpResponse(json.dumps(prepare_data(medicine_list, [['MedicinePerPatient']]), indent=4, sort_keys=True), mimetype='JSON', status_code=200)
    else:
        return func.HttpResponse(f"No medicine found for this patient", mimetype='text/plain', status_code=404)

# Handles the creation of one or more medicine_per_patient in the DB
# Expects a request body in the shape of a list of medicine_per_patient objects
def post_medicine_list(req):
    meds_to_add = []
    body = req.get_json()
    
    try:
        id = int(req.route_params.get('id'))
        for item in body:
            mpp = MedicinePerPatient(
                patient_user_id=id,
                medicine_id=item['medicine_id'],
                intake_time=item['intake_time'],
                intake_state=item['intake_state'],
                dose=item['dose']
            )
            meds_to_add.append(mpp)
    except:
        return func.HttpResponse(f"Invalid input, list of medicine_per_patient objects expected", mimetype='text/plain', status_code=412)

    try:
        for mpp in meds_to_add:
            insert_medicine_per_patient(mpp)
        return func.HttpResponse(f"Medicine list entries successfully inserted", mimetype='text/plain', status_code=200)
    except:
        return func.HttpResponse(f"Failed to insert medicine list entries", mimetype='text/plain', status_code=412)

# This method removes a single patient along with its user and user_details records
def delete_medicine_list(req):
    meds_to_delete = []
    body = req.get_json()

    # Try to loop through multiple medicine_per_patient objects in request body
    try:
        p_id = int(req.route_params.get('id'))
        for item in body:
            mpp = MedicinePerPatient(
                patient_user_id=p_id,
                id=item['id']
            )
            meds_to_delete.append(mpp)
    except:
        return func.HttpResponse(f"Invalid input, list of medicine per patient objects expected", mimetype='text/plain', status_code=412)

    try:
        for mpp in meds_to_delete:
            delete_medicine_per_patient(mpp)
        return func.HttpResponse(f"Medicine list entries successfully removed", mimetype='text/plain', status_code=200)
    except:
        return func.HttpResponse(f"Failed to remove medicine list entries", mimetype='text/plain', status_code=412)