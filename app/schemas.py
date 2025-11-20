from datetime import date
from typing import Optional
from pydantic import BaseModel

class PatientARTCreate(BaseModel):
    # Required-ish identifiers
    state: Optional[str] = None
    lga: Optional[str] = None
    facility_name_all: str
    datim_code: str
    sex: Optional[str] = None
    hospital_number: Optional[str] = None
    patient_identifier: str
    current_age: Optional[int] = None

    date_of_birth: Optional[date] = None
    care_entry_point: Optional[str] = None
    art_start_date: Optional[date] = None
    age_at_art_initiation: Optional[int] = None
    clients_current_art_status: Optional[str] = None
    educational_status: Optional[str] = None
    residential_address: Optional[str] = None
    last_drug_pick_up_date: Optional[date] = None
    last_viral_load_result: Optional[str] = None
    cd4_test_cd4_result: Optional[str] = None
    adherence_outcome_classification: Optional[str] = None
    marital_status: Optional[str] = None
    employment_status: Optional[str] = None
    no_of_days_of_refills: Optional[int] = None
    who_stage_at_art_start: Optional[str] = None
    last_drug_art_pick_up_date: Optional[date] = None
    duration_on_art_months: Optional[int] = None
    previous_art_regimen: Optional[str] = None
    current_art_regimen: Optional[str] = None
    current_art_regimen_line: Optional[str] = None
    last_viral_load_sample_collection_date: Optional[date] = None
    last_viral_load_result_date: Optional[date] = None
    cd4_test_sample_collection_date: Optional[date] = None
    cd4_test_result_date: Optional[date] = None

    class Config:
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "state": "Abia",
                "lga": "Umuahia North",
                "facility_name_all": "St. Joseph Catholic Hospital- Ohabia",
                "datim_code": "NBpPdHsoZge",
                "sex": "Female",
                "hospital_number": "HOSP-2025-00123",
                "patient_identifier": "PAT-0001-ABIA-2025",
                "current_age": 39,
                "date_of_birth": "1986-01-01",
                "care_entry_point": "OPD",
                "art_start_date": "2015-06-15",
                "age_at_art_initiation": 30,
                "clients_current_art_status": "Active",
                "educational_status": "Tertiary",
                "residential_address": "No 10 Aba Road, Umuahia",
                "last_drug_pick_up_date": "2025-01-10",
                "last_viral_load_result": "550",
                "cd4_test_cd4_result": "450",
                "adherence_outcome_classification": "Good",
                "marital_status": "Married",
                "employment_status": "Employed",
                "no_of_days_of_refills": 30,
                "who_stage_at_art_start": "Stage II",
                "last_drug_art_pick_up_date": "2025-01-10",
                "duration_on_art_months": 115,
                "previous_art_regimen": "TDF/3TC/NVP",
                "current_art_regimen": "TDF/3TC/DTG",
                "current_art_regimen_line": "First Line",
                "last_viral_load_sample_collection_date": "2024-12-20",
                "last_viral_load_result_date": "2025-01-05",
                "cd4_test_sample_collection_date": "2024-11-15",
                "cd4_test_result_date": "2024-11-20"
            }
        }

class PatientARTResponse(BaseModel):
    id: int
    state: Optional[str]
    lga: Optional[str]
    facility_name_all: Optional[str]
    datim_code: str
    sex: Optional[str]
    hospital_number: Optional[str]
    patient_identifier: str
    current_age: Optional[int]

    # Optional fields
    date_of_birth: Optional[date] = None
    care_entry_point: Optional[str] = None
    art_start_date: Optional[date] = None
    age_at_art_initiation: Optional[int] = None
    clients_current_art_status: Optional[str] = None
    educational_status: Optional[str] = None
    residential_address: Optional[str] = None
    last_drug_pick_up_date: Optional[date] = None
    last_viral_load_result: Optional[str] = None
    cd4_test_cd4_result: Optional[str] = None
    adherence_outcome_classification: Optional[str] = None
    marital_status: Optional[str] = None
    employment_status: Optional[str] = None
    no_of_days_of_refills: Optional[int] = None
    who_stage_at_art_start: Optional[str] = None
    last_drug_art_pick_up_date: Optional[date] = None
    duration_on_art_months: Optional[int] = None
    previous_art_regimen: Optional[str] = None
    current_art_regimen: Optional[str] = None
    current_art_regimen_line: Optional[str] = None
    last_viral_load_sample_collection_date: Optional[date] = None
    last_viral_load_result_date: Optional[date] = None
    cd4_test_sample_collection_date: Optional[date] = None
    cd4_test_result_date: Optional[date] = None
    signature: Optional[str] = None
    comment: Optional[str] = None
    suggestion: Optional[str] = None
    
    class Config:
        orm_mode = True


class PatientARTUpdate(BaseModel):
    # all fields optional for partial update
    state: Optional[str] = None
    lga: Optional[str] = None
    facility_name_all: Optional[str] = None
    datim_code: Optional[str] = None
    sex: Optional[str] = None
    hospital_number: Optional[str] = None
    current_age: Optional[int] = None

    date_of_birth: Optional[date] = None
    care_entry_point: Optional[str] = None
    art_start_date: Optional[date] = None
    age_at_art_initiation: Optional[int] = None
    clients_current_art_status: Optional[str] = None
    educational_status: Optional[str] = None
    residential_address: Optional[str] = None
    last_drug_pick_up_date: Optional[date] = None
    last_viral_load_result: Optional[str] = None
    cd4_test_cd4_result: Optional[str] = None
    adherence_outcome_classification: Optional[str] = None
    marital_status: Optional[str] = None
    employment_status: Optional[str] = None
    no_of_days_of_refills: Optional[int] = None
    who_stage_at_art_start: Optional[str] = None
    last_drug_art_pick_up_date: Optional[date] = None
    duration_on_art_months: Optional[int] = None
    previous_art_regimen: Optional[str] = None
    current_art_regimen: Optional[str] = None
    current_art_regimen_line: Optional[str] = None
    last_viral_load_sample_collection_date: Optional[date] = None
    last_viral_load_result_date: Optional[date] = None
    cd4_test_sample_collection_date: Optional[date] = None
    cd4_test_result_date: Optional[date] = None

    class Config:
        extra = "forbid"