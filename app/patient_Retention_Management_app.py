







# # =============================================
# # EXAMPLE USAGE
# # =============================================
# if __name__ == "__main__":
#     # Initialize database
#     db_manager = DatabaseManager('sqlite:///patient_art_data.db')
#     crud = PatientARTCRUD(db_manager)
    
#     # 1. CREATE - Add new patient
#     print("\n=== CREATING NEW PATIENT ===")
#     patient_data = {
#         'state': 'Rivers',
#         'lga': 'Port Harcourt',
#         'facility_name_all': 'University of Port Harcourt Teaching Hospital',
#         'datim_code': 'DATIM001',
#         'sex': 'Male',
#         'hospital_number': 'HN123456',
#         'patient_identifier': 'PID789012',
#         'current_age': 35,
#         'clients_current_art_status': 'Active',
#         'educational_status': 'Secondary',
#         'residential_address': '123 Main Street, Port Harcourt',
#         'marital_status': 'Married',
#         'employment_status': 'Employed'
#     }
    
#     new_patient = crud.create_patient(patient_data)
    
#     # 2. READ - View all columns for a patient
#     print("\n=== VIEWING ALL COLUMNS ===")
#     patient_details = crud.view_all_columns('PID789012')
#     if patient_details:
#         for key, value in patient_details.items():
#             print(f"{key}: {value}")
    
#     # 3. UPDATE - Modify patient record
#     print("\n=== UPDATING PATIENT ===")
#     update_data = {
#         'clients_current_art_status': 'Active',
#         'current_art_regimen': 'TDF/3TC/DTG',
#         'last_viral_load_result': 'Undetectable',
#         'comment': 'Patient adherence is excellent'
#     }
#     crud.update_patient('PID789012', update_data)
    
#     # 4. VIEW ALL PATIENTS
#     print("\n=== VIEWING ALL PATIENTS ===")
#     all_patients = crud.view_all_patients_all_columns()
#     print(f"Total active patients: {len(all_patients)}")
    
#     # 5. SOFT DELETE - Void a patient
#     print("\n=== VOIDING PATIENT ===")
#     crud.soft_delete_patient('PID789012', 'admin_user')
    
#     # 6. VIEW VOIDED PATIENTS
#     print("\n=== VIEWING VOIDED PATIENTS ===")
#     all_patients_with_voided = crud.view_all_patients_all_columns(include_voided=True)
#     voided_count = sum(1 for p in all_patients_with_voided if p['voided'] == 1)
#     print(f"Total voided patients: {voided_count}")
    
#     # 7. RESTORE - Unvoid a patient
#     print("\n=== RESTORING PATIENT ===")
#     crud.restore_patient('PID789012')
