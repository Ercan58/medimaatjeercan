# gets parameter from either the path or body in the request
def get_param(req, param, par_type):
    par = req.params.get(param)
    if not par:
        try:
            req_body = req.get_json()
        except ValueError:
            return None
        else:
            par = req_body.get(param)

    if(par_type == "int"):
        par = int(par)
    if(par_type == "string"):
        par = str(par)
    else:
        pass

    return par


# sqlalchemy response to list with dicts, and remove unwanted data
def prepare_data(db_data, var_list):
    return_list = []
    for rindex, item in enumerate(db_data):
        for iindex, var in enumerate(var_list):
            var_attr = getattr(item, var[0])
            obj_dict = var_attr.__dict__
            del obj_dict["_sa_instance_state"]
            try:
                return_list[rindex].append(obj_dict)
            except IndexError:
                return_list.append([obj_dict])
    return return_list