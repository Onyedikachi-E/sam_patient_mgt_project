from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from .schemas import PatientARTResponse, PatientARTUpdate, PatientARTCreate
from .db_models import DatabaseManager
from .repo import PatientARTCRUD
from typing import List, Optional
db_manager = DatabaseManager()


# Create router
router = APIRouter(prefix="/patient_data")


# ============================================
# CREATE WAREHOUSE
# ============================================

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Import patient data using line list with predefined headers",
    description="Create initial data by importing a line list"
)
def import_patient_line_list(
    line_list_data_import: UploadFile,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_import = PatientARTCRUD(db_manager=db)
        patient_import = patient_import.create_patient_from_line_list(
            line_list_data=line_list_data_import
        )

        return patient_import
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Patient import failed -> {e}"
        )
    

@router.post(
    "/single",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new patient record",
    description="This route is used to create a single patient record in the system",
)
def create_patient(
    patient_payload: PatientARTCreate,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        new_patient = patient_manager.create_patient(patient_payload=patient_payload)
        return new_patient

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Patient creation failed -> {e}",
        )
    

@router.get(
    "/{patient_identifier}",
    response_model=Optional[PatientARTResponse],
    summary="Get complete patient information by patient identifier",
    description="This route is to be used to fetch all information about a patient"
)
def get_patient_by_identifier(
    patient_identifier: str,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        patient_record = patient_manager.get_patient_by_identifier(patient_identifier=patient_identifier)

        return patient_record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error -> {e}"
        )
    

# ============================================================
# 1. Get ALL patients
# ============================================================

@router.get(
    "/",
    response_model=List[PatientARTResponse],
    summary="Get all patient records",
    description="Fetch all patient records stored in the system",
)
def get_all_patients(
    db: Session = Depends(db_manager.get_session),
    skip:int = 0,
    limit:int = 100
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        patients = patient_manager.get_all_patients(skip, limit)
        return patients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch patients -> {e}"
        )


# ============================================================
# 2. Get patients by facility (datim_code)
# ============================================================

@router.get(
    "/facility/{datim_code}",
    response_model=List[PatientARTResponse],
    summary="Get all patients by facility",
    description="Fetch all patients linked to a specific facility using DATIM code",
)
def get_patients_by_facility(
    datim_code: str,
    skip:int = 0,
    limit:int = 100,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        patients = patient_manager.get_patients_by_datim_code(
            datim_code, skip, limit
        )
        return patients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch patients by facility -> {e}"
        )


# ============================================================
# 3. Get patients by state
# ============================================================

@router.get(
    "/state/{state}",
    response_model=List[PatientARTResponse],
    summary="Get all patients by state",
    description="Fetch all patients mapped to a specific state",
)
def get_patients_by_state(
    state: str,
    skip: int = 0,
    limit: int = 0,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        patients = patient_manager.get_patients_by_state(
            state, skip, limit
        )
        return patients
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to fetch patients by state -> {e}"
        )
    

# ============================================================
# 4. UPDATE patient
# ============================================================
@router.put(
    "/{patient_identifier}",
    response_model=PatientARTResponse,
    summary="Update a patient record",
    description="Update an existing patient record using patient identifier",
)
def update_patient(
    patient_identifier: str,
    payload: PatientARTUpdate,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        update_data = payload.dict(exclude_unset=True)

        updated_patient = patient_manager.update_patient(
            patient_identifier=patient_identifier,
            update_data=update_data,
        )

        if not updated_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with identifier {patient_identifier} not found",
            )

        return updated_patient

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update patient -> {e}"
        )


@router.delete(
    "/{patient_identifier}",
    summary="Soft delete (void) a patient record",
    description="Marks a patient record as voided instead of deleting it permanently",
)
def soft_delete_patient(
    patient_identifier: str,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        success = patient_manager.soft_delete_patient(
            patient_identifier=patient_identifier,
            voided_by="SUPER USER",
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with identifier {patient_identifier} not found or already voided",
            )

        return {
            "message": "Patient voided successfully",
            "patient_identifier": patient_identifier,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to void patient -> {e}"
        )


# ============================================================
# 6. RESTORE voided patient
# ============================================================

@router.post(
    "/{patient_identifier}/restore",
    summary="Restore a voided patient record",
    description="Unvoids a previously voided patient record",
)
def restore_patient(
    patient_identifier: str,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        success = patient_manager.restore_patient(
            patient_identifier=patient_identifier
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Patient with identifier {patient_identifier} not found",
            )

        return {
            "message": "Patient restored successfully",
            "patient_identifier": patient_identifier,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to restore patient -> {e}"
        )