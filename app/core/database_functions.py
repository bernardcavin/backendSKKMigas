import os
from dotenv import load_dotenv
import contextlib
from sqlalchemy.orm import Session
from app.api.auth.models import User
from app.scripts.create_dummy_data import generate_dummy_data
from app.core.database import Base, SessionLocal, engine

def reset_database(engine):
    Base.metadata.drop_all(bind=engine)  # Drops all tables
    Base.metadata.create_all(bind=engine)  # Creates all tables
    
def data_exists(db: Session):
    return db.query(User).first() is not None
    
@contextlib.contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Main logic for generating dummy data if no data exists
# reset_database(engine)

def init_db():
    with get_db_context() as session:
        try:
            if data_exists(session):
                return
        except Exception as e:
            pass
        reset_database(engine)
        generate_dummy_data(session, n=500)