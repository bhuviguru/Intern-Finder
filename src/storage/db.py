from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, Job, SentNotification
import os
from dotenv import load_dotenv

load_dotenv()

# Ensure the database is created in the project root
DB_NAME = os.getenv('DB_NAME', 'internships.db')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_job(session, job_data):
    """
    Saves a job if it doesn't already exist (based on link).
    Returns the Job object if saved, None if duplicate.
    """
    existing_job = session.query(Job).filter_by(link=job_data['link']).first()
    if existing_job:
        return None
    
    new_job = Job(**job_data)
    session.add(new_job)
    session.commit()
    session.refresh(new_job)
    return new_job

def get_unnotified_jobs(session, limit=None):
    query = session.query(Job).filter_by(is_sent=False).order_by(Job.score.desc())
    if limit:
        return query.limit(limit).all()
    return query.all()

def mark_jobs_as_sent(session, job_ids):
    session.query(Job).filter(Job.id.in_(job_ids)).update({Job.is_sent: True}, synchronize_session=False)
    session.commit()
