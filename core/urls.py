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
                    GetPharmacistDetailsView,
                    
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

    path("search-patient-by-nhis-number/", SearchPrincipalPatientByNHISView.as_view(), name="search_patient_by_nhis_number"),
    path("search-patient-by-file-number/", SearchPrincipalPatientByFileNumberView.as_view(), name="search_patient_by_file_number"),
    path("search-spouse-by-file-number/", SearchSpouseByFileNumberView.as_view(), name="search_spouse_by_file_number"),
    path("search-child-by-file-number/", SearchChildByFileNumberView.as_view(), name="search_child_by_file_number"),

    path("get-principal-continuation-sheet/<slug:slug>/", GetPrincipalContinuationSheetView.as_view(), name="get_principal_continuation_sheet"),
    path("get-spouse-continuation-sheet/<slug:slug>/", GetSpouseContinuationSheetView.as_view(), name="get_spouse_continuation_sheet"),
    path("get-child-continuation-sheet/<slug:slug>/", GetChildContinuationSheetView.as_view(), name="get_child_continuation_sheet"),

    path("update-principal-continuation-sheet/<slug:slug>/", UpdatePrincipalContinuationSheetView.as_view(), name="update_principal_continuation_sheet"),
    path("update-spouse-continuation-sheet/<slug:slug>/", UpdateSpouseContinuationSheetView.as_view(), name="update_spouse_continuation_sheet"),
    path("update-child-continuation-sheet/<slug:slug>/", UpdateChildContinuationSheetView.as_view(), name="update_child_continuation_sheet"),

    path("get-doctor/", GetDoctorDetailsView.as_view(), name="get_doctor"),
    path("get-pharmacist/", GetPharmacistDetailsView.as_view(), name="get_pharmacist"),
    path("get-nurse/", GetNurseDetailsView.as_view(), name="get_nurse"),
    path("get-accounts/", GetAccountsDetailsView.as_view(), name="get_accounts"),
    path("get-lab/", GetLabDetailsView.as_view(), name="get_lab"),


]
