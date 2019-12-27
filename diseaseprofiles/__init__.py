import logging

import azure.functions as func
import json
from ..resources import authorization as auth, db_disease_profile


# main function handling request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('diseaseprofiles triggered checking type.')
    try:
        token = req.headers.get("Authorization")
        if req.method == "GET":
            return get_profiles(req)
        elif req.method == 'POST' and auth.check_authorization_by_scope(token, 'write'):
            return post_profile(req)
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
def get_profiles(req) -> func.HttpResponse:
    logging.info('diseaseprofiles handeling get request.')
    c = db_disease_profile.get_all_diseaseprofiles()

    return func.HttpResponse(
        json.dumps(c, cls=db.AlchemyEncoder, indent=4, sort_keys=True),
        mimetype='JSON',
        status_code=200
    )


# Handle post request
def post_profile(req) -> func.HttpResponse:
    logging.info('diseaseprofiles handeling post request')
    try:
        message = req.get_json()
        try:
            name = message['name']
            description = message['description']
            imagepath = message['imagePath']
            db_disease_profile.post_diseaseprofile(name, imagepath, description)
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
