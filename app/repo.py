from db_models import DatabaseManager, PatientARTData
from typing import Any, Dict, Optional, List
from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from io import BytesIO
import pandas as pd
from schemas import PatientARTCreate, PatientARTUpdate



# =============================================
# CRUD OPERATIONS
# =============================================
class PatientARTCRUD:
    def __init__(self, db_manager: Session):
        self.db_manager = db_manager

    def parse_date(self, value):
        """
        Convert various Excel/date/string formats to a Python date object.
        Returns None if parsing fails.
        """
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return None

        # Already a date/datetime
        if isinstance(value, (date, datetime)):
            return value.date() if isinstance(value, datetime) else value

        # Try as string
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return None

            # 1. Try your specific known format first: DD/MM/YYYY
            try:
                return datetime.strptime(value, "%d/%m/%Y").date()
            except ValueError:
                pass

            # 2. Other common formats if needed
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue

            # 3. Try pandas as a last resort (but don't fall back to 1970):
            try:
                dt = pd.to_datetime(value, errors="coerce", dayfirst=True)
                if pd.isna(dt):
                    return None
                return dt.date()
            except Exception:
                return None

        # Excel numeric (serial date)
        # If your Excel stores dates as numbers (e.g. 31607), handle here:
        if isinstance(value, (int, float)) and not pd.isna(value):
            try:
                dt = pd.to_datetime(value, origin="1899-12-30", unit="D")
                return dt.date()
            except Exception:
                return None

        # Anything else: give up gracefully
        return None
    
    def create_patient_from_line_list(self, line_list_data: UploadFile):
        """
        Create patient records from uploaded patient line list
        Required fields: state, lga, facility_name_all, datim_code, 
                        sex, hospital_number, patient_identifier, current_age
        """
        try:
            # Implement the logic
            file_bytes = line_list_data.file.read()
            if not file_bytes:
                raise ValueError("Uploaded file is empty.")
            
            # Here, let's assume the first sheet only; change if needed.
            excel_file = BytesIO(file_bytes)
            dataframe = pd.read_excel(excel_file)

            created_count = 0
            # Helper to read safely from a row
            def get_val(row, col):
                return None if (col not in row or pd.isna(row[col])) else row[col]
            for _, row in dataframe.iterrows():
                # Basic safety: skip if essential identifier missing
                if pd.isna(row["hospital_number"]) and pd.isna(row["patient_identifier"]):
                    continue

                patient = PatientARTData(
                    state=str(get_val(row, "state")).strip() if get_val(row, "state") is not None else None,
                    lga=str(get_val(row, "lga")).strip() if get_val(row, "lga") is not None else None,
                    facility_name_all=str(get_val(row, "facility_name_all")).strip() if get_val(row, "facility_name_all") is not None else None,
                    datim_code=str(get_val(row, "datim_code")).strip() if get_val(row, "datim_code") is not None else None,
                    sex=str(get_val(row, "sex")).strip() if get_val(row, "sex") is not None else None,
                    hospital_number=str(get_val(row, "hospital_number")).strip() if get_val(row, "hospital_number") is not None else None,
                    patient_identifier=str(get_val(row, "patient_identifier")).strip() if get_val(row, "patient_identifier") is not None else None,
                    current_age=int(get_val(row, "current_age")) if get_val(row, "current_age") is not None else None,

                    date_of_birth=self.parse_date(get_val(row, "date_of_birth")),
                    care_entry_point=str(get_val(row, "care_entry_point")).strip() if get_val(row, "care_entry_point") is not None else None,
                    art_start_date=self.parse_date(get_val(row, "art_start_date")),
                    age_at_art_initiation=int(get_val(row, "age_at_art_initiation")) if get_val(row, "age_at_art_initiation") is not None else None,
                    clients_current_art_status=str(get_val(row, "clients_current_art_status")).strip() if get_val(row, "clients_current_art_status") is not None else None,
                    educational_status=str(get_val(row, "educational_status")).strip() if get_val(row, "educational_status") is not None else None,
                    residential_address=str(get_val(row, "residential_address")).strip() if get_val(row, "residential_address") is not None else None,
                    last_drug_pick_up_date=self.parse_date(get_val(row, "last_drug_pick_up_date")),
                    last_viral_load_result=str(get_val(row, "last_viral_load_result")).strip() if get_val(row, "last_viral_load_result") is not None else None,
                    cd4_test_cd4_result=str(get_val(row, "cd4_test_cd4_result")).strip() if get_val(row, "cd4_test_cd4_result") is not None else None,
                    adherence_outcome_classification=str(get_val(row, "adherence_outcome_classification")).strip() if get_val(row, "adherence_outcome_classification") is not None else None,
                    marital_status=str(get_val(row, "marital_status")).strip() if get_val(row, "marital_status") is not None else None,
                    employment_status=str(get_val(row, "employment_status")).strip() if get_val(row, "employment_status") is not None else None,
                    no_of_days_of_refills=int(get_val(row, "no_of_days_of_refills")) if get_val(row, "no_of_days_of_refills") is not None else None,
                    who_stage_at_art_start=str(get_val(row, "who_stage_at_art_start")).strip() if get_val(row, "who_stage_at_art_start") is not None else None,
                    last_drug_art_pick_up_date=self.parse_date(get_val(row, "last_drug_art_pick_up_date")),
                    duration_on_art_months=int(get_val(row, "duration_on_art_months")) if get_val(row, "duration_on_art_months") is not None else None,
                    previous_art_regimen=str(get_val(row, "previous_art_regimen")).strip() if get_val(row, "previous_art_regimen") is not None else None,
                    current_art_regimen=str(get_val(row, "current_art_regimen")).strip() if get_val(row, "current_art_regimen") is not None else None,
                    current_art_regimen_line=str(get_val(row, "current_art_regimen_line")).strip() if get_val(row, "current_art_regimen_line") is not None else None,
                    last_viral_load_sample_collection_date=self.parse_date(get_val(row, "last_viral_load_sample_collection_date")),
                    last_viral_load_result_date=self.parse_date(get_val(row, "last_viral_load_result_date")),
                    cd4_test_sample_collection_date=self.parse_date(get_val(row, "cd4_test_sample_collection_date")),
                    cd4_test_result_date=self.parse_date(get_val(row, "cd4_test_result_date"))
                )

                self.db_manager.add(patient)
                created_count += 1
            
            self.db_manager.commit()
            return {
                "patient_data": {
                    "message": "Line list import completed",
                    "total_patient_inserted": created_count
                }
            }
        except Exception as e:
            self.db_manager.rollback()
            print(f"✗ Error creating patient records: {str(e)}")
            raise

    # 1. CREATE - Single patient
    def create_patient(self, patient_payload: PatientARTCreate):
        """Create a single patient record"""
        try:
            # Verify patient with identifer doesnt exist
            patient_exist = self.db_manager.query(PatientARTData).filter(PatientARTData.patient_identifier==patient_payload.patient_identifier).first()
            if patient_exist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"A patient with same patient identifier already exist"
                )
            # Convert Pydantic model to plain dict (only provided fields)
            patient_data = patient_payload.model_dump(exclude_unset=True)

            patient = PatientARTData(**patient_data)
            self.db_manager.add(patient)
            self.db_manager.commit()
            self.db_manager.refresh(patient)
            return {
                "message": "Patient created successfully"
            }
        except Exception as e:
            self.db_manager.rollback()
            print(f"✗ Error creating patient: {str(e)}")
            raise

    
    # 2. READ - Get patient records
    def get_patient_by_identifier(self, patient_identifier: str) -> Optional[PatientARTData]:
        """Get a single patient by patient_identifier"""
        try:
            query = self.db_manager.query(PatientARTData).filter(
                PatientARTData.patient_identifier == patient_identifier,
                PatientARTData.voided==False
            )
            patient = query.first()
            if not patient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Specified Patient Identifier not found"
                )

            return patient
        except:
            raise
    

    def get_all_patients(self, skip, limit) -> List[PatientARTData]:
        """Get all patient records"""
        try:
            query = self.db_manager.query(PatientARTData).offset(skip).limit(limit)
            
            patients = query.all()
            return patients
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error fetching all patients records -> {str(e)})"
            )
    

    def get_patients_by_datim_code(self, datim_code: str, skip, limit) -> List[PatientARTData]:
        """Get all patients from a specific facility using datim code"""
        try:
            query = self.db_manager.query(PatientARTData).filter(
                PatientARTData.datim_code == datim_code
            ).offset(skip).limit(limit)
            
            patients = query.all()
            return patients
        finally:
            self.db_manager.close()
    

    def get_patients_by_state(self, state: str, skip, limit) -> List[PatientARTData]:
        """Get all patients from a specific state"""
        try:
            query = self.db_manager.query(PatientARTData).filter(
                PatientARTData.state == state
            ).offset(skip).limit(limit)
            
            patients = query.all()
            return patients
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error fetching all patients records -> {str(e)})"
            )
    

    # 3. UPDATE - Modify existing patient record
    def update_patient(self, patient_identifier: str, update_data: Dict[str, Any]) -> Optional[PatientARTData]:
        """Update an existing patient record"""
        try:
            patient = self.db_manager.query(PatientARTData).filter(
                PatientARTData.patient_identifier == patient_identifier,
                PatientARTData.voided == 0
            ).first()
            
            if not patient:
                print(f"✗ Patient not found: {patient_identifier}")
                return None
            
            # Update fields
            for key, value in update_data.items():
                if hasattr(patient, key):
                    setattr(patient, key, value)
            
            self.db_manager.commit()
            self.db_manager.refresh(patient)
            
            print(f"✓ Patient updated successfully: {patient_identifier}")
            return patient
        
        except Exception as e:
            self.db_manager.rollback()
            print(f"✗ Error updating patient: {str(e)}")
            raise
    

    # 4. SOFT DELETE - Void a patient record
    def soft_delete_patient(self, patient_identifier: str, voided_by: str) -> bool:
        """Soft delete a patient record by setting voided = 1"""
        try:
            patient = self.db_manager.query(PatientARTData).filter(
                PatientARTData.patient_identifier == patient_identifier,
                PatientARTData.voided == 0
            ).first()
            
            if not patient:
                print(f"✗ Patient not found or already voided: {patient_identifier}")
                return False
            
            patient.voided = 1
            patient.voided_by = voided_by
            patient.voided_date = datetime.now()
            
            self.db_manager.commit()
            
            print(f"✓ Patient voided successfully: {patient_identifier}")
            return True
        
        except Exception as e:
            self.db_manager.rollback()
            print(f"✗ Error voiding patient: {str(e)}")
            raise
    

    # 5. RESTORE - Unvoid a patient record
    def restore_patient(self, patient_identifier: str) -> bool:
        """Restore a voided patient record"""
        try:
            patient = self.db_manager.query(PatientARTData).filter(
                PatientARTData.patient_identifier == patient_identifier,
            ).first()
            
            if not patient:
                print(f"✗ Patient not found: {patient_identifier}")
                return False
            
            if patient.voided==False:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Patient is not voided"
                )
            
            
            patient.voided = 0
            patient.voided_by = None
            patient.voided_date = None
            
            self.db_manager.commit()
            
            print(f"✓ Patient restored successfully: {patient_identifier}")
            return True
        
        except Exception as e:
            self.db_manager.rollback()
            print(f"✗ Error restoring patient: {str(e)}")
            raise
    
    