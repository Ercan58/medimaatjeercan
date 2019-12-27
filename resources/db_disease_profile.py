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


# get disease profile by id
def get_diseaseprofiles_by_id(id):
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(DiseaseProfile)
    query = query.filter(DiseaseProfile.disease_profile_id == id)

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


# update disease profile in db
def put_diseaseprofile(id, name, image_path, description):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()

        query = session.query(DiseaseProfile)
        disease = query.filter(DiseaseProfile.disease_profile_id == id).first()
        disease.name = name
        disease.image_path = image_path
        disease.description = description
        session.commit()
        return True
    except:
        return None


# delete disease profile from db
def delete_diseaseprofile(id):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(DiseaseProfile)
        query = query.filter(DiseaseProfile.disease_profile_id == id)
        query.delete()
        session.commit()
        return True
    except:
        return None
