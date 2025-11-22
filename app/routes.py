from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, BackgroundTasks, Query
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from .schemas import PatientARTResponse, PatientARTUpdate, PatientARTCreate, LineListRequestResponse
from .db_models import DatabaseManager, LineListRequest
from .repo import PatientARTCRUD
from typing import List, Optional
from datetime import datetime
import uuid, os
from io import BytesIO
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
    "/patient_identifier",
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
    "/identifiers/all",
    summary="Get all patient identifiers",
    description="Fetch paginated list of all patients' DATIM codes and identifiers",
)
def get_all_patient_identifiers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        identifiers = patient_manager.get_all_patient_identifiers(skip=skip, limit=limit)
        return [
            {"datim_code": d, "patient_identifier": pid}
            for d, pid in identifiers
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error fetching all patient identifiers -> {e}",
        )

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
    "/facility/datim_code",
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
    "/state/state_name",
    response_model=List[PatientARTResponse],
    summary="Get all patients by state",
    description="Fetch all patients mapped to a specific state",
)
def get_patients_by_state(
    state_name: str,
    skip: int = 0,
    limit: int = 0,
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        patients = patient_manager.get_patients_by_state(
            state_name, skip, limit
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
    "/patient_identifier",
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
    "/patient_identifier",
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
    "/patient_identifier/restore",
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
    

@router.delete(
    "/delete/all",
    summary="Delete ALL patient records",
    description="⚠️ Irreversibly deletes all patient records from the patient_art_data table",
)
def drop_all_patients(
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        deleted = patient_manager.drop_all_patients()
        return {
            "message": "All patient records deleted successfully",
            "total_deleted": deleted,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting all patient records -> {e}",
        )
    

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)
def _background_generate_line_list(
    db_session_factory,
    request_id: str,
    datim_code: str | None,
):
    # Create a new session inside background task
    db: Session = db_session_factory()
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        excel_bytes = patient_manager.generate_patient_line_list(datim_code=datim_code)
        
        # fetch the request record
        request_record = db.query(LineListRequest).filter(LineListRequest.request_id==request_id).first()

        file_content = excel_bytes.getvalue()
        request_record.file_data=file_content
        request_record.file_size = len(file_content)
        request_record.request_status="Completed"
        db.commit()
        print(f"✓ Export stored in database for request {request_id}")
    finally:
        db.close()


@router.post(
    "/line-list/export",
    summary="Request patient line list export",
    description="Triggers background generation of the patient line list. Returns a job id.",
)
def request_line_list_export(
    background_tasks: BackgroundTasks,
    datim_code: str | None = Query(default=None),
    db: Session = Depends(db_manager.get_session),
):
    # Generate a job ID
    request_id = str(uuid.uuid4())

    # schedule background work
    background_tasks.add_task(
        _background_generate_line_list,
        db_manager.get_session, 
        request_id,
        datim_code,
    )

    new_request = LineListRequest(
        request_id=request_id,
        requested_by_id="SUPER USER",
        request_date=datetime.now(),
        request_status="Processing"
    )
    db.add(new_request)
    db.commit()

    return {
        "message": "Export started",
        "request_id": request_id,
    }


@router.get(
    "/line-list/requests/all",
    response_model=List[LineListRequestResponse],
    summary="Fetch all the request records for line lists generation"
)
def get_line_list_requests(
    db: Session = Depends(db_manager.get_session),
):
    try:
        patient_manager = PatientARTCRUD(db_manager=db)
        line_list_requests = patient_manager.get_line_list_requests()

        return line_list_requests
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error: -> {str(e)}"
        )



@router.get(
    "/line-list/download/request_id",
    summary="Download generated patient line list",
)
def download_line_list(request_id: str, db: Session = Depends(db_manager.get_session),):
    request_record = db.query(LineListRequest).filter(
        LineListRequest.request_id == request_id
    ).first()

    if request_record.request_status != "Completed":
        raise HTTPException(status_code=400, detail="Export not ready yet")

    # Create a file-like object from the binary data
    file_stream = BytesIO(request_record.file_data)
    file_stream.seek(0)

    return StreamingResponse(
        content=file_stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=patient_line_list.xlsx"}
    )


@router.get(
    "/line-list/template",
    summary="Download empty patient line list template for import",
    description="Generate and download an empty Excel template for patient line list upload",
)
def download_line_list_template(
    db: Session = Depends(db_manager.get_session),
):
    patient_manager = PatientARTCRUD(db_manager=db)
    excel_file = patient_manager.generate_empty_line_list_template()

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": 'attachment; filename="patient_line_list_template.xlsx"'
        },
    )
