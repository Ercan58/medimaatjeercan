import sqlalchemy
from sqlalchemy.orm import defer
from ..resources.models import ElectronicDossier, Patient, User
from ..resources.db_connection import request_session

def fetch_electronic_dossier_by_id(id):
    try:
        session = request_session()
        query = session.query(ElectronicDossier).filter(ElectronicDossier.electronic_dossier_id==Patient.electronic_dossier_id).filter(Patient.electronic_dossier_id==id)
        return query.all()
    except:
        return None

def fetch_patient_by_id(id):
    try:
        session = request_session()
        query = session.query(Patient, User).filter(Patient.patient_user_id==id).filter(Patient.patient_user_id==User.id).options(defer(User.password))
        return query.all()
    except:
        return None

def update_electronic_dossier_by_id(ed_id, new_iq, new_summary):
    try:
        session = request_session()
        query = session.query(ElectronicDossier).filter(ElectronicDossier.electronic_dossier_id==ed_id).first()
        query.iq = new_iq
        query.summary = new_summary
        session.commit()
    except:
        return None