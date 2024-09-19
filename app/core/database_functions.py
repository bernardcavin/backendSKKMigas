import contextlib
from sqlalchemy.orm import Session
from app.api.auth.models import User
from app.scripts.create_dummy_data import generate_dummy_data
from app.core.database import Base, SessionLocal, engine
from sqlalchemy import text
from app.core.config import settings
   
def data_exists(db: Session):
    return db.query(User).first() is not None
    
@contextlib.contextmanager
def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    
    try:
        with get_db_context() as session:
            if data_exists(session):
                return
    except Exception as e:
        pass
    with get_db_context() as session:
        
        if settings.ENVIRONMENT == "local":
            Base.metadata.drop_all(bind=engine)  # Creates all tables
        elif settings.ENVIRONMENT == "staging":
            drop_schema_query = text("DROP SCHEMA IF EXISTS public CASCADE;")
            create_schema_query = text("CREATE SCHEMA public;")

            session.execute(drop_schema_query)
            session.execute(create_schema_query)
            session.commit()
        Base.metadata.create_all(bind=engine)  # Creates all tables
        generate_dummy_data(session, n=500)