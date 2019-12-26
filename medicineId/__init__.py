import logging

import azure.functions as func
import json
from ..resources import authorization as auth, db_medicine


# main function handling request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('medicine triggered checking type.')
    try:
        token = req.headers.get("Authorization")
        if req.method == "GET":
            return get_medicine(req)
        elif req.method == 'PUT' and auth.check_authorization_by_scope(token, 'write'):
            return put_medicine(req)
        elif req.method == 'DELETE' and auth.check_authorization_by_scope(token, 'write'):
            return delete_medicine(req)
        else:
            return func.HttpResponse(f"You are not authorised to do this", mimetype='text/plain', status_code=401)
    except KeyError:
        return func.HttpResponse(
            'Not a valid token found',
            status_code=400
        )
    except ValueError:
        return func.HttpResponse(
            "Token doesn't exist",
            status_code=400
        )


def get_medicine(req):
    logging.info('medicine handeling get request.')
    id = req.route_params.get("medicineid")
    try:
        int(id)
    except ValueError:
        return func.HttpResponse(
            'Route parameter not a valid input.',
            status_code=400
        )
    c = db_medicine.get_medicine_by_id(id)

    return func.HttpResponse(
        json.dumps(c, cls=db.AlchemyEncoder, indent=4, sort_keys=True),
        mimetype='JSON',
        status_code=200
    )


def put_medicine(req):
    logging.info('medicine handeling put request.')
    try:
        message = req.get_json()
        id = req.route_params.get("medicineid")
        int(id)
        name = message['name']
        description = message['intakeInstructions']
        imagepath = message['imagePath']
        if db_medicine.put_medicine(id, name, imagepath, description) is not None:
            return func.HttpResponse(
                'Updated entry to database.',
                status_code=200
            )
    except KeyError:
        return func.HttpResponse(
            'Body is not valid.',
            status_code=400
        )
    except ValueError:
        return func.HttpResponse(
            'No json found in the body',
            status_code=400
        )
    return func.HttpResponse(
        'Request not accepted',
        status_code=400
    )


def delete_medicine(req):
    logging.info('medicine handeling delete request.')
    try:
        id = req.route_params.get("medicineid")
        int(id)
        db_medicine.delete_medicine(id)
        return func.HttpResponse(
            'Succesfully removed entry from database',
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            'Route parameter not a valid input.',
            status_code=400
        )

