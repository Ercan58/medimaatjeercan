import logging

import azure.functions as func
import json
from ..resources import connection as db, authorization as auth, db_disease_profile


# main function handling request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('diseaseprofiles triggered checking type.')
    try:
        token = req.headers.get("Authorization")
        if req.method == "GET":
            return get_profile(req)
        elif req.method == 'PUT' and auth.check_authorization_by_scope(token, 'write'):
            return put_profile(req)
        elif req.method == 'DELETE' and auth.check_authorization_by_scope(token, 'write'):
            return delete_profile(req)
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


def get_profile(req):
    logging.info('diseaseprofiles handeling get request.')
    id = req.route_params.get("diseaseid")
    try:
        int(id)
    except ValueError:
        return func.HttpResponse(
            'Route parameter not a valid input.',
            status_code=400
        )
    c = db_disease_profile.get_diseaseprofiles_by_id(id)

    return func.HttpResponse(
        json.dumps(c, cls=db.AlchemyEncoder, indent=4, sort_keys=True),
        mimetype='JSON',
        status_code=200
    )


def put_profile(req):
    logging.info('diseaseprofiles handeling put request.')
    try:
        message = req.get_json()
        id = req.route_params.get("diseaseid")
        int(id)
        name = message['name']
        description = message['description']
        imagepath = message['image_path']
        if db_disease_profile.put_diseaseprofile(id, name, imagepath, description) is not None:
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


def delete_profile(req):
    logging.info('diseaseprofiles handeling delete request.')
    id = req.route_params.get("diseaseid")
    try:
        int(id)
        db_disease_profile.delete_diseaseprofile(id)
        return func.HttpResponse(
            'Succesfully removed entry',
            status_code=200
        )
    except ValueError:
        return func.HttpResponse(
            'Route parameter not a valid input.',
            status_code=400
        )
