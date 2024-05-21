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
                    UploadSpouseTestResultView, PayRequestPrincipalPatientTestView,
                    PayRequestChildTestView, PayRequestSpouseTestView,
                    CreatePrincipalPatientPrescriptionView,
                    CreateChildPrescriptionView, CreateSpousePrescriptionView,
                    ListChildPrescriptionView, ListSpousePrescriptionView,
                    ListPrincipalPatientPrescriptionView,
                    GetPrincipalPatientPrescriptionView, GetChildPrescriptionView,
                    GetSpousePrescriptionView, PayChildPrescriptionView,
                    PayPrincipalPatientPrescriptionView, PaySpousePrescriptionView,
                    BillChildPrescriptionView, BillSpousePrescriptionView,
                    BillPrincipalPatientPrescriptionView, ListDoctorsView,
                    BookAppointmentView, ListAppointmentsView, GetPatientAppointmentsView,
                    CompletePatientAppointmentsView, ListDoctorAppointmentsView,
                    
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

    path("pay-child-test-result/<slug:slug>/", PayRequestChildTestView.as_view(), name="pay_child_test_result"),
    path("pay-spouse-test-result/<slug:slug>/", PayRequestSpouseTestView.as_view(), name="pay_spouse_test_result"),
    path("pay-principal-test-result/<slug:slug>/", PayRequestPrincipalPatientTestView.as_view(), name="pay_principal_test_result"),

    path("create-patient-prescription/<str:patient_file_number>/", CreatePrincipalPatientPrescriptionView.as_view(), name="create_patient_prescription"),
    path("create-spouse-prescription/<str:spouse_file_number>/", CreateSpousePrescriptionView.as_view(), name="create_spouse_prescription"),
    path("create-child-prescription/<str:child_file_number>/", CreateChildPrescriptionView.as_view(), name="create_child_prescription"),


    path("list-patient-prescription/<str:patient_file_number>/", ListPrincipalPatientPrescriptionView.as_view(), name="create_patient_prescription"),
    path("list-spouse-prescription/<str:spouse_file_number>/", ListSpousePrescriptionView.as_view(), name="list_spouse_prescription"),
    path("list-child-prescription/<str:child_file_number>/", ListChildPrescriptionView.as_view(), name="list_child_prescription"),

    path("get-patient-prescription/<slug:slug>/", GetPrincipalPatientPrescriptionView.as_view(), name="get_patient_prescription"),
    path("get-spouse-prescription/<slug:slug>/", GetSpousePrescriptionView.as_view(), name="get_spouse_prescription"),
    path("get-child-prescription/<slug:slug>/", GetChildPrescriptionView.as_view(), name="get_child_prescription"),

    path("pay-patient-prescription/<slug:slug>/", PayPrincipalPatientPrescriptionView.as_view(), name="pay_patient_prescription"),
    path("pay-spouse-prescription/<slug:slug>/", PaySpousePrescriptionView.as_view(), name="pay_spouse_prescription"),
    path("pay-child-prescription/<slug:slug>/", PayChildPrescriptionView.as_view(), name="pay_child_prescription"),

    path("bill-patient-prescription/<slug:slug>/", BillPrincipalPatientPrescriptionView.as_view(), name="bill_patient_prescription"),
    path("bill-spouse-prescription/<slug:slug>/", BillSpousePrescriptionView.as_view(), name="bill_spouse_prescription"),
    path("bill-child-prescription/<slug:slug>/", BillChildPrescriptionView.as_view(), name="bill_child_prescription"),

    path("list-doctors/", ListDoctorsView.as_view(), name="list_doctors"),


    path("book-appointment/", BookAppointmentView.as_view(), name="book_appointment"),
    path("list-appointments/", ListAppointmentsView.as_view(), name="list_appointment"),
    path("get-appointment/<slug:slug>/", GetPatientAppointmentsView.as_view(), name="get_appointment"),
    path("complete-appointment/<slug:slug>/", CompletePatientAppointmentsView.as_view(), name="complete_appointment"),
    path("list-appointments/", ListAppointmentsView.as_view(), name="list_appointment"),
    path("doctors-appointments/", ListDoctorAppointmentsView.as_view(), name="doctor_appointments"),
    
]
