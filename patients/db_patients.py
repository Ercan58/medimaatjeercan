import sqlalchemy
from sqlalchemy.orm import defer
from ..resources.models import Patient, User, ElectronicDossier, Coach
from ..resources.db_connection import request_session

# Function to fetch all patient records, joins Patient.patient_user_id on User.id and Patient.electronic_dossier_id on ElectronicDossier.electronic_dossier_id
def fetch_all_patients():
    session = request_session()
    query = session.query(Patient, User, ElectronicDossier).filter(Patient.patient_user_id==User.id).filter(Patient.electronic_dossier_id==ElectronicDossier.electronic_dossier_id).options(defer(User.password))
    return query.all()

def fetch_multiple_patients(number):
    session = request_session()
    query = session.query(Patient, User).filter(Patient.patient_user_id==User.id).filter(Patient.electronic_dossier_id==ElectronicDossier.electronic_dossier_id).limit(number).options(defer(User.password))
    return query.all()

def fetch_patient_by_id(id):
    session = request_session()
    query = session.query(Patient, User).filter(Patient.patient_user_id==id).filter(Patient.patient_user_id==User.id).options(defer(User.password))
    return query.all()

# Create patient in db
def insert_patient(p_id, c_id, ed_id):
    session = request_session()
    patient = Patient(patient_user_id=p_id, coach_user_id=c_id, electronic_dossier_id=ed_id)
    session.add(patient)
    session.commit()

# Remove coach from db
def delete_patient_by_id(id):
    session = request_session()
    query = session.query(Patient, User).get(id)
    query.delete()
    query.commit()

# Update patient
def update_patient(p_id, new_c_id):
    session = request_session()
    query = session.query(Patient).filter(Patient.patient_user_id==p_id).first()
    query.coach_user_id = new_c_id
    session.commit()

# Create electronic dossier in db
def insert_electronic_dossier(summ, ed_iq):
    session = request_session()
    electronic_dossier = ElectronicDossier(summary=summ, iq=ed_iq)
    session.add(electronic_dossier)
    session.flush()
    ed_id = electronic_dossier.electronic_dossier_id
    session.commit()
    return ed_id

# Check if supplied user id belongs to a coach
def check_if_coach_exists(id):
    session = request_session()
    query = session.query(Coach).filter(Coach.id==id)
    return query.all()

# # Function with connection string to create the db engine connection and to establish a connection with the database
# # Returns the db connection session
# def db_connect():
#     engine = sqlalchemy.engine.create_engine('postgresql+psycopg2://medimaatjeadmin@medimaatje-auth:9050a3a086206329784301b99f410b03!@medimaatje-auth.postgres.database.azure.com:5432/medimaatje-auth?sslmode=require')
#     session = sessionmaker(bind=engine)
#     return session()