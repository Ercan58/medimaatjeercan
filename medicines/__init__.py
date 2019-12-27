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
            return get_medicines(req)
        elif req.method == "POST" and auth.check_authorization_by_scope(token, 'write'):
            return post_medicine(req)
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


# Handle get request
def get_medicines(req) -> func.HttpResponse:
    logging.info('medicine handeling get request.')
    c = db_medicine.get_all_medicines()

    return func.HttpResponse(
        json.dumps(c, cls=db.AlchemyEncoder, indent=4, sort_keys=True),
        mimetype='JSON',
        status_code=200
    )


# Handle post request
def post_medicine(req) -> func.HttpResponse:
    logging.info('Medicines handeling post request')
    try:
        message = req.get_json()
        name = message['name']
        intakeInstructions = message['intakeInstructions']
        imagepath = message['imagePath']
        db_medicine.post_medicine(name, imagepath, intakeInstructions)
        return func.HttpResponse(
            'Added entry to database.',
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
