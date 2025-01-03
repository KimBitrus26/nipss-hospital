from django.urls import path
from .views import (
                    CreateAccountantProfileView,
                    CreateDoctorProfileView,
                    CreateNurseProfileView,
                    CreateLabTechnicianProfileView,
                    CreatePharmacistProfileView,
                    CreatePatientView,
                    ListPatientsView, GetPatientView, GetChildView, GetSpouseView,
                    SearchChildByFileNumberView, SearchPrincipalPatientByFileNumberView,
                    SearchPrincipalPatientByNHISView, SearchSpouseByFileNumberView,
                    GetChildContinuationSheetView, GetPrincipalContinuationSheetView,
                    GetSpouseContinuationSheetView,
                    UpdateChildContinuationSheetView, UpdatePrincipalContinuationSheetView,
                    UpdateSpouseContinuationSheetView,
                    GetAccountsDetailsView, GetDoctorDetailsView,
                    GetLabDetailsView, GetNurseDetailsView,
                    GetPharmacistDetailsView, CreateRequestChildTestView,
                    CreateRequestPrincipalPatientTestView,
                    CreateRequestSpouseTestView, ListRequestChildTestView,
                    ListRequestPrincipalPatientTestView,
                    ListRequestSpouseTestView, GetRequestChildTestView,
                    GetRequestPrincipalPatientTestView, GetRequestSpouseTestView,
                    UploadChildTestResultView, UploadPrincipalPatientTestResultView,
                    UploadSpouseTestResultView,
                    
                    )

urlpatterns = [
    
    path("create-patient/", CreatePatientView.as_view(), name="create_patient"),
    path("create-pharmacist-profile/", CreatePharmacistProfileView.as_view(), name="create_pharmacist_profile"),
    path("create-doctor-profile/", CreateDoctorProfileView.as_view(), name="create_doctor_profile"),
    path("create-nurse-profile/", CreateNurseProfileView.as_view(), name="create_nurse_profile"),
    path("create-accountant-profile/", CreateAccountantProfileView.as_view(), name="create_accountant_profile"),
    path("create-lab-technician-profile/", CreateLabTechnicianProfileView.as_view(), name="create_lab_technician_profile"),
    path("list-patients/", ListPatientsView.as_view(), name="list_patients"),
    
    path("get-patient/<str:file_number>/", GetPatientView.as_view(), name="get_patient"),
    path("get-spouse/<str:file_number>/", GetSpouseView.as_view(), name="get_spouse"),
    path("get-child/<str:file_number>/", GetChildView.as_view(), name="get_child"),

    # search endpoints
    path("search-patient-by-nhis-number/", SearchPrincipalPatientByNHISView.as_view(), name="search_patient_by_nhis_number"),
    path("search-patient-by-file-number/", SearchPrincipalPatientByFileNumberView.as_view(), name="search_patient_by_file_number"),
    path("search-spouse-by-file-number/", SearchSpouseByFileNumberView.as_view(), name="search_spouse_by_file_number"),
    path("search-child-by-file-number/", SearchChildByFileNumberView.as_view(), name="search_child_by_file_number"),

    # continuation sheet endpoints
    path("get-principal-continuation-sheet/<slug:slug>/", GetPrincipalContinuationSheetView.as_view(), name="get_principal_continuation_sheet"),
    path("get-spouse-continuation-sheet/<slug:slug>/", GetSpouseContinuationSheetView.as_view(), name="get_spouse_continuation_sheet"),
    path("get-child-continuation-sheet/<slug:slug>/", GetChildContinuationSheetView.as_view(), name="get_child_continuation_sheet"),

    path("update-principal-continuation-sheet/<slug:slug>/", UpdatePrincipalContinuationSheetView.as_view(), name="update_principal_continuation_sheet"),
    path("update-spouse-continuation-sheet/<slug:slug>/", UpdateSpouseContinuationSheetView.as_view(), name="update_spouse_continuation_sheet"),
    path("update-child-continuation-sheet/<slug:slug>/", UpdateChildContinuationSheetView.as_view(), name="update_child_continuation_sheet"),

    # profile endpoints
    path("get-doctor/", GetDoctorDetailsView.as_view(), name="get_doctor"),
    path("get-pharmacist/", GetPharmacistDetailsView.as_view(), name="get_pharmacist"),
    path("get-nurse/", GetNurseDetailsView.as_view(), name="get_nurse"),
    path("get-accounts/", GetAccountsDetailsView.as_view(), name="get_accounts"),
    path("get-lab/", GetLabDetailsView.as_view(), name="get_lab"),

    # request test endpoints
    path("create-patient-test-request/<str:patient_file_number>/", CreateRequestPrincipalPatientTestView.as_view(), name="create_patient_test_request"),
    path("create-spouse-test-request/<str:spouse_file_number>/", CreateRequestSpouseTestView.as_view(), name="create_spouse_test_request"),
    path("create-child-test-request/<str:child_file_number>/", CreateRequestChildTestView.as_view(), name="create_child_test_request"),

    path("list-patient-test-request/<str:patient_file_number>/", ListRequestPrincipalPatientTestView.as_view(), name="list_patient_test_request"),
    path("list-spouse-test-request/<str:spouse_file_number>/", ListRequestSpouseTestView.as_view(), name="list_spouse_test_request"),
    path("list-child-test-request/<str:child_file_number>/", ListRequestChildTestView.as_view(), name="list_child_test_request"),

    path("get-patient-test-request/<slug:slug>/", GetRequestPrincipalPatientTestView.as_view(), name="get_patient_test_request"),
    path("get-spouse-test-request/<slug:slug>/", GetRequestSpouseTestView.as_view(), name="get_spouse_test_request"),
    path("get-child-test-request/<slug:slug>/", GetRequestChildTestView.as_view(), name="get_child_test_request"),

    # upload results endpoints
    path("upload-patient-test-result/<slug:slug>/", UploadPrincipalPatientTestResultView.as_view(), name="upload_patient_test_result"),
    path("upload-spouse-test-result/<slug:slug>/", UploadSpouseTestResultView.as_view(), name="upload_spouse_test_result"),
    path("upload-child-test-result/<slug:slug>/", UploadChildTestResultView.as_view(), name="upload_child_test_result"),


]
