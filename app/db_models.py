"""
Patient ART Data Management System using SQLAlchemy
Complete CRUD operations with soft delete functionality
"""

from sqlalchemy import create_engine, Column, Integer, String, Date, Text, DateTime, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from datetime import datetime
from typing import List, Optional, Dict, Any
import pymysql, os
from dotenv import load_dotenv
load_dotenv()

# Database setup
Base = declarative_base()

# =============================================
# DATABASE MODEL
# =============================================
class PatientARTData(Base):
    __tablename__ = 'patient_art_data'
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Required Fields (NOT NULL)
    state = Column(String(100))
    lga = Column(String(100))
    facility_name_all = Column(String(255), nullable=False)
    datim_code = Column(String(50), nullable=False)
    sex = Column(String(10))
    hospital_number = Column(String(50))
    patient_identifier = Column(String(50), nullable=False, unique=True)
    current_age = Column(Integer)
    
    # Optional Fields
    date_of_birth = Column(Date)
    care_entry_point = Column(String(100))
    art_start_date = Column(Date)
    age_at_art_initiation = Column(Integer, nullable=True)
    clients_current_art_status = Column(String(50))
    educational_status = Column(String(100))
    residential_address = Column(String(255))
    last_drug_pick_up_date = Column(Date)
    last_viral_load_result = Column(String(50))
    cd4_test_cd4_result = Column(String(50))
    adherence_outcome_classification = Column(String(50))
    marital_status = Column(String(50))
    employment_status = Column(String(100))
    no_of_days_of_refills = Column(Integer)
    who_stage_at_art_start = Column(String(50))
    last_drug_art_pick_up_date = Column(Date)
    duration_on_art_months = Column(Integer)
    previous_art_regimen = Column(String(255))
    current_art_regimen = Column(String(255))
    current_art_regimen_line = Column(String(50))
    last_viral_load_sample_collection_date = Column(Date)
    last_viral_load_result_date = Column(Date)
    cd4_test_sample_collection_date = Column(Date)
    cd4_test_result_date = Column(Date)
    signature = Column(String(255))
    comment = Column(Text)
    suggestion = Column(Text)
    
    # Soft Delete Fields
    voided = Column(Integer, default=0)
    voided_by = Column(String(255))
    voided_date = Column(DateTime)
    
    # Timestamps
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'state': self.state,
            'lga': self.lga,
            'facility_name_all': self.facility_name_all,
            'datim_code': self.datim_code,
            'sex': self.sex,
            'hospital_number': self.hospital_number,
            'patient_identifier': self.patient_identifier,
            'current_age': self.current_age,
            'clients_current_art_status': self.clients_current_art_status,
            'educational_status': self.educational_status,
            'residential_address': self.residential_address,
            'last_drug_pick_up_date': self.last_drug_pick_up_date,
            'last_viral_load_result': self.last_viral_load_result,
            'cd4_test_cd4_result': self.cd4_test_cd4_result,
            'adherence_outcome_classification': self.adherence_outcome_classification,
            'date_of_birth': self.date_of_birth,
            'care_entry_point': self.care_entry_point,
            'marital_status': self.marital_status,
            'employment_status': self.employment_status,
            'art_start_date': self.art_start_date,
            'no_of_days_of_refills': self.no_of_days_of_refills,
            'who_stage_at_art_start': self.who_stage_at_art_start,
            'last_drug_art_pick_up_date': self.last_drug_art_pick_up_date,
            'duration_on_art_months': self.duration_on_art_months,
            'previous_art_regimen': self.previous_art_regimen,
            'current_art_regimen': self.current_art_regimen,
            'current_art_regimen_line': self.current_art_regimen_line,
            'last_viral_load_sample_collection_date': self.last_viral_load_sample_collection_date,
            'last_viral_load_result_date': self.last_viral_load_result_date,
            'cd4_test_sample_collection_date': self.cd4_test_sample_collection_date,
            'cd4_test_result_date': self.cd4_test_result_date,
            'name': self.name,
            'date': self.date,
            'signature': self.signature,
            'comment': self.comment,
            'suggestion': self.suggestion,
            'voided': self.voided,
            'voided_by': self.voided_by,
            'voided_date': self.voided_date,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    


# =============================================
# DATABASE CONNECTION SETUP
# =============================================
class DatabaseManager:
    def __init__(
        self,
        database_url: str = os.getenv("DATABASE_URL"),  
        db_name: str = os.getenv("DATABASE_NAME"),
    ):
        self.database_url = database_url
        self.db_name = db_name
        self.engine = create_engine(
            self.database_url, 
            echo=False, 
            future=True, 
            poolclass=NullPool,
            connect_args={"ssl": {"ssl-mode": "REQUIRED"}, "connect_timeout": 10}
        )

    def create_databse(self):
        server_url = self.database_url.rsplit("/", 1)[0]
        server_engine = create_engine(server_url, echo=False, future=True)

        # 2) Create database if it does not exist
        with server_engine.connect() as connection:
            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS {self.db_name} "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            )
        
        # 4) Create tables
        Base.metadata.create_all(self.engine)
        print("DATABASE CREATION IS COMPLETE!!!")
        

    def get_session(self):
        """Get a new database session"""
        self.Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )
        return self.Session()


if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_databse()
    

