from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import sessionmaker
from resources.db_connection import Base, db_connect
from resources.models import DiseaseProfile


# Get all the disease profiles in the db with sqlalchemy
def get_all_diseaseprofiles():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DiseaseProfile)

    return query.all()


# post disease profile to db
def post_diseaseprofile(name, image_path, description):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        disease = DiseaseProfile(name=name, image_path=image_path, description=description)
        session.add(disease)
        session.commit()
        return True
    except:
        return None
