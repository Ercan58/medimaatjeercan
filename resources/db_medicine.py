from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import sessionmaker
from resources.db_connection import Base, db_connect
from resources.models import Medicine


# Get all the medicine in the db with sqlalchemy
def get_all_medicines():
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Medicine)

    return query.all()


# update medicine in db
def put_medicine(id, name, image_path, intake_instruction):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Medicine)
        medicine = query.filter(Medicine.medicine_id == id).first()
        medicine.name = name
        medicine.image_path = image_path
        medicine.description = intake_instruction
        session.commit()
        return True
    except:
        return None


# Get medicine by id
def get_medicine_by_id(id):
    engine = db_connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Medicine)
    query = query.filter(Medicine.medicine_id == id)

    return query.all()


# post medicine to db
def post_medicine(name, image_path, intake_instruction):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        medicine = Medicine(name=name, image_path=image_path, description=intake_instruction)
        session.add(medicine)
        session.commit()
        return True
    except:
        return None


# delete medicine from db
def delete_medicine(id):
    try:
        engine = db_connect()
        Session = sessionmaker(bind=engine)
        session = Session()
        query = session.query(Medicine)
        query = query.filter(Medicine.medicine_id == id)
        query.delete()
        session.commit()
        return True
    except:
        return None