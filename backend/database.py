from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

file_path = os.path.abspath(os.getcwd())+"/test.db"
SQLALCHEMY_DATABASE_URL = 'sqlite:///'+file_path

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#testtt

Base = declarative_base()
