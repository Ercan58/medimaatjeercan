import sqlalchemy
from sqlalchemy.orm import defer
from ..resources.models import MedicinePerPatient, Medicine, Patient
from ..resources.db_connection import request_session

def fetch_medicine_list(id):
    try:
        session = request_session()
        query = session.query(MedicinePerPatient).filter(Patient.patient_user_id==MedicinePerPatient.patient_user_id).filter(Medicine.medicine_id==MedicinePerPatient.medicine_id)
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

def insert_medicine_per_patient(mpp):
    try:
        session = request_session()
        session.add(mpp)
        session.commit()
    except:
        return None

# Remove coach from db
def delete_medicine_per_patient(mpp):
    try:
        session = request_session()

        mpp_id = mpp.id
        p_id = mpp.patient_user_id
        
        query = session.query(MedicinePerPatient).filter(MedicinePerPatient.id==mpp_id).filter(MedicinePerPatient.patient_user_id==p_id)
        query.delete()
        session.commit()
    except:
        return None