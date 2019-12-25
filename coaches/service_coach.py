from ..resources.functions_shared import get_param
from . import db_coaches as db

# Get coaches with the following parameters:
# No parameters = all the coaches
# id = specific coach
# number and start_index is a specific amount of coaches
def get_coach_logic(req):
    id = get_param(req, 'id', 'int')
    number_of_coaches = get_param(req, 'number', 'int')
    start_index = get_param(req, 'start_index', 'int')

    if id:
        data = db.get_coach(id)
        if(data[0] is None):
            return None
        else:
            return data
    elif number_of_coaches and start_index:
        return db.get_multiple_coaches(start_index, number_of_coaches)
    else:
        return db.get_all_coaches()


def post_coach_logic(req):
    id = get_param(req, 'id', 'int')
    workplace = get_param(req, 'workplace', 'string')

    db.create_coach(id, workplace)
    return db.get_coach(id)


# This method removes a single coach (and user & details)
def delete_coach_logic(req):
    id = get_param(req, 'id', 'int')
    db.remove_coach(id)


# Updates a existing coach in the DB
# User_id and the workplace is required
def put_coach_logic(req):
    id = get_param(req, 'id', 'int')
    workplace = get_param(req, 'workplace', 'string')
    db.update_coach(id, workplace)
    return db.get_coach(id)

