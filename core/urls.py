
from django.urls import path, include
from .views import (index, admin_receptionist, doctor_dashboard,
                    pharmacy_dashboard, lab_technician_dashboard,
                    patient_dashboard, login_view, logout_view,
                    register_patient_view, verify_patient_phone_number,
                    create_patient_file_view, resend_otp_view, get_patients_lists,
                    get_patient, get_doctor_lists, get_doctor,
                    receptionist_complete_profile_view,
                    lab_technician_complete_profile_view,
                    doctor_complete_profile_view,
                    pharmacy_complete_profile_view, get_doctor_profile,
                    get_patient_profile, get_pharmacist_profile, get_receptionist_profile,
                    get_lab_profile, patient_appoint_view,
                    patient_book_appointment_view, get_patient_appointments_view,
                    appointments_receptionist_view, appointments_approved_view,
                    appointments_request_view, doctor_approve_appointment_view,
                    doctor_attend_patient_view, doctor_get_patient_view,
                    doctor_request_patient_test_view,
                    doctor_patient_prescription_view, doctor_get_patient_results_view,
                    doctor_patient_test_prescription_view, doctor_update_availabilty_view,
                    patient_to_be_tested_view, patient_tested_upload_result_view,
                    patients_tested_results_view, pharmacist_search_patient_view,
                    pharmacist_get_patient_view, pharmacist_make_payment_view,
                    verify_payment_view, pharmacist_check_patient_payment_view,
                    pharmacist_confirm_patient_payment_view,



                    )

urlpatterns = [
    
    path('', index, name="home"),
    path('login', login_view, name="login"),
    path('logout', logout_view, name="logout"),

    path('register-patient', register_patient_view, name="register_patient"),
    path('verify-phone', verify_patient_phone_number, name="verify_phone"),
    path('resend-otp', resend_otp_view, name="resend_otp"),

    path('admin-receptionist', admin_receptionist, name="admin_receptionist"),
    path('doctor-dashboard', doctor_dashboard, name="doctor_dashboard"),
    path('pharmacy-dashboard', pharmacy_dashboard, name="pharmacy_dashboard"),
    path('lab-technician-dashboard', lab_technician_dashboard, name="lab_technician_dashboard"),
    path('patient-dashboard', patient_dashboard, name="patient_dashboard"),

    path('create-patient-file', create_patient_file_view, name="create_patient_file"),
    path('get-patients-list', get_patients_lists, name="get_patients_lists"),
    path('get-patient/<slug:slug>', get_patient, name="get_patient"),

    path('get-doctors-list', get_doctor_lists, name="get_doctor_lists"),
    path('get-doctor/<slug:slug>', get_doctor, name="get_doctor"),


    path('receptionist-complete-prifile', receptionist_complete_profile_view, name="receptionist_complete_prifile"),
    path('doctor-complete-prifile', doctor_complete_profile_view, name="doctor_complete_prifile"),
    path('pharmacist-complete-prifile', pharmacy_complete_profile_view, name="pharmicist_complete_prifile"),
    path('lab-complete-prifile', lab_technician_complete_profile_view, name="lab_complete_prifile"),

    path('lab-profile', get_lab_profile, name="lab_profile"),
    path('receptionist-profile', get_receptionist_profile, name="receptionist_profile"),
    path('doctor-profile', get_doctor_profile, name="doctor_profile"),
    path('patient-profile', get_patient_profile, name="patient_profile"),
    path('pharmacist-profile', get_pharmacist_profile, name="pharmacist_profile"),

    path('patient-appoint', patient_appoint_view, name="patient_appoint"),
    path('patient-book-appoint/<slug:slug>', patient_book_appointment_view, name="patient_book_appoint"),

    path('get-patient-appointments', get_patient_appointments_view, name="get_patient_appointments"),
    path('appointments-receptionist', appointments_receptionist_view, name="appointments_receptionist"),
    path('appointments-request', appointments_request_view, name="appointments_request"),
    path('appointments-approved', appointments_approved_view, name="appointments_approved"),
    path('doctor-approve-appointment/<int:pk>', doctor_approve_appointment_view, name="doctor_approve_appointment"),

    path('doctor-attend-patient', doctor_attend_patient_view, name="doctor_attend_patient"),
    path('doctor-get-patient/<slug:slug>', doctor_get_patient_view, name="doctor_get_patient"),
    path('doctor-request-test-patient/<slug:slug>', doctor_request_patient_test_view, name="doctor_request_test_patient"),
    path('doctor-patient-prescription/<slug:slug>', doctor_patient_prescription_view, name="doctor_patient_prescription"),
    path('doctor-get-patient-results/<slug:slug>', doctor_get_patient_results_view, name="doctor_get_patient_results"),
    path('doctor-patient-test-prescription/<int:pk>', doctor_patient_test_prescription_view, name="doctor_patient_test_prescription"),
    path('doctor-update-availabilty', doctor_update_availabilty_view, name="doctor_update_availabilty"),

    path('patients-to-be-tested', patient_to_be_tested_view, name="patients_to_be_tested"),
    path('patient-tested-upload-result/<int:pk>', patient_tested_upload_result_view, name="patient_tested_upload_result"),
    path('patient-tested-results', patients_tested_results_view, name="patient_tested_results"),

    path('pharmacist-search-patient', pharmacist_search_patient_view, name="pharmacist_search_patient"),
    path('pharmacist-get-patient/<slug:slug>', pharmacist_get_patient_view, name="pharmacist_get_patient"),
    path('pharmacist-make-payment/<slug:slug>', pharmacist_make_payment_view, name="pharmacist_make_payment"),
    
    path("verify-transaction/<str:ref>/", verify_payment_view, name="verify_transaction"),
    path("pharmacist-check-patient-payment", pharmacist_check_patient_payment_view, name="pharmacist_check_patient_payment"),
    path("pharmacist-confirm-patient-payment/<str:ref>", pharmacist_confirm_patient_payment_view, name="pharmacist_confirm_patient_payment"),


]
