from django.shortcuts import render

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q

from .decorators import (login_required, is_receptionist_required,
                         is_doctor_required, is_patient_required, 
                         is_pharmcist_required, is_lab_technician_required,
                         )
from accounts.utils import Helper, PayStackRequestHelper
from accounts.models import OTPCode, _generate_code
from .models import (Patient, Doctor, AdminReceptionist, Pharmacist, 
                     LabTechnician, BookAppointment, PENDING, ATTENDED, APPROVED,
                    PatientDiagnostic, Prescription, Transaction,
                     )

from accounts.models import User

def index(request):

    return render(request, "nipps-templates/index.html")

def login_view(request):
    
    if request.method == 'POST':
       
        password = request.POST.get("password")
        email = request.POST.get("email")
        
        user = authenticate(request, username=email, password=password)

        print("user====", user)
        
        if user and user.is_doctor:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('doctor_dashboard'))
        
        elif user and user.is_phamacist:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('pharmacy_dashboard'))
        
        elif user and user.is_lab_technician:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('lab_technician_dashboard'))
        
        elif user and user.is_receptionist:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('admin_receptionist'))
        
        elif user and user.is_patient:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('patient_dashboard'))
        else:
            messages.info(request, 'Failed to log in. Invalid email or password')
            return render(request, "nipps-templates/index.html")
            
    return render(request, "nipps-templates/index.html")

@is_receptionist_required
def register_patient_view(request):
   
    if request.method == 'POST':
        
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        if User.objects.filter(Q(email=email) | Q(phone_number=phone_number)).exists():
            messages.info(request, f"Patient with this email '{email}' or '{phone_number}' already existed")
            return HttpResponseRedirect(reverse('register_patient'))

        if phone_number[0] != "0":
            phone_number = "0" + phone_number
        print(phone_number)   
        prepend = email.split("@")[0]
        code = _generate_code()

        password = f"{prepend}-{code}"

        user = User.objects.create_user(
            password=password,
            email=email,
            phone_number=phone_number,
            country_code="234",
            is_patient=True
            )
        print("password patient", password)
        Helper.send_signup_email(email, password, user)
        return HttpResponseRedirect(reverse('verify_phone'))

    return render(request, "nipps-templates/register-patient.html",)

@is_receptionist_required
def verify_patient_phone_number(request):
   
    if request.method == 'POST':
        
        otp_code = request.POST.get("otp_code")
        
        try:
            otp_obj = OTPCode.objects.get(code=otp_code)
        except OTPCode.DoesNotExist:
            otp_obj = None

        if not otp_obj:
            messages.info(request,"OTP code not found")
            return HttpResponseRedirect(reverse('verify_phone'))
        
        if otp_obj.user.is_phone_verified:
            messages.info(request, "Phone number verified already")
            return HttpResponseRedirect(reverse('create_patient_file'))
        
        if otp_obj.is_used:
            messages.info(request, "OTP Code already used")
            return HttpResponseRedirect(reverse('verify_phone'))
        
        if otp_obj.expired():
            messages.info(request, "OTP Code expired")
            return HttpResponseRedirect(reverse('verify_phone'))
        
        otp_obj.otp_verified()
        otp_obj.user.phone_verified()

        return HttpResponseRedirect(reverse('create_patient_file'))

    return render(request, "nipps-templates/verify-patient-phne.html",)

@is_receptionist_required
def resend_otp_view(request):
   
    if request.method == 'POST':
        
        phone_number = request.POST.get("phone_number")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = None
        if not user:
            messages.info(request, f"User not found with this phone number {phone_number}")
            return HttpResponseRedirect(reverse('register_patient'))

        otp = OTPCode.objects.create(user=user)
        Helper.send_otp_sms(otp.code, user.country_code, 
                                user.phone_number)


        return HttpResponseRedirect(reverse('verify_phone'))

    return render(request, "nipps-templates/resend_code-phone.html",)

@is_receptionist_required
def create_patient_file_view(request):

    if request.method == 'POST':
        
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.info(request, f"User not found with this email {email}")
            return HttpResponseRedirect(reverse('create_patient_file'))
        
        if Patient.objects.filter(user=user).exists():
            messages.info(request, f"Patient already existed. Please ask for Patient file number and attend to Patient")
            return HttpResponseRedirect(reverse('create_patient_file'))

        if not user.is_patient:
            messages.info(request, f"User does not has a Patient account. Please contact Admin")
            return HttpResponseRedirect(reverse('register_patient'))

        from datetime import date, datetime
        date_object = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
        year = date_object.year

        age = date.today().year - year
        participant_age = age if age >= 1 else 1
        code_number = _generate_code()
        file_number = f"NIPSS-{code_number}"

        Patient.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            date_of_birth=date_of_birth,
            age=participant_age,
            address=address,
            city=city,
            state=state,
            country=country,
            user=user,
            file_number=file_number
        )
        country_code = user.country_code
        phone_number = user.phone_number
        
        Helper.send_patient_file_number_sms(file_number, country_code, phone_number)
        Helper.send_patient_file_number_email(email, file_number, last_name)
        
        messages.success(request, f"Patient file created successfully. File number has been sent to Patient Phone number and email")
        return HttpResponseRedirect(reverse('admin_receptionist'))
    
    return render(request, "nipps-templates/create-patient-file.html",)

@login_required
def logout_view(request):

    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def admin_receptionist(request):

    return render(request, "nipps-templates/admin-receptionist.html")

@login_required
def doctor_dashboard(request):

    return render(request, "nipps-templates/doctor-dashboard.html")

@login_required
def pharmacy_dashboard(request):

    return render(request, "nipps-templates/pharmacy-dashboard.html")

@login_required
def lab_technician_dashboard(request):

    return render(request, "nipps-templates/lab-technician-dashboard.html")

@login_required
def patient_dashboard(request):

    return render(request, "nipps-templates/patient-dashboard.html")

@is_receptionist_required
def get_patients_lists(request):

    patients = Patient.objects.all()
    ctx = {"patients": patients}

    return render(request, "nipps-templates/patient-list.html", ctx)
    

@is_receptionist_required
def get_patient(request, slug):


    try:
        patient = Patient.objects.get(slug=slug)
    except Patient.DoesNotExist:
        messages.info(request, f"Patient not found")
        return HttpResponseRedirect(reverse('admin_receptionist'))
    
    ctx = {"patient": patient}

    return render(request, "nipps-templates/get-patient.html", ctx)
    

@is_receptionist_required
def get_doctor_lists(request):   

    doctors = Doctor.objects.all()
    ctx = {"doctors": doctors}

    return render(request, "nipps-templates/doctor-list.html", ctx)
   

@is_receptionist_required
def get_doctor(request, slug):

    try:
        doctor = Doctor.objects.get(slug=slug)
    except Doctor.DoesNotExist:
        messages.info(request, f"Doctor not found")
        return HttpResponseRedirect(reverse('admin_receptionist'))
    
    ctx = {"doctor": doctor}

    return render(request, "nipps-templates/get-doctor.html", ctx)

@is_receptionist_required
def get_receptionist_profile(request):

    user = request.user

    try:
        receptionist = AdminReceptionist.objects.get(user=user)
    except Doctor.DoesNotExist:
        messages.info(request, f"Receptionist not found")
        return HttpResponseRedirect(reverse('admin_receptionist'))
    
    ctx = {"receptionist": receptionist}

    return render(request, "nipps-templates/receptionist-profile.html", ctx)

@is_doctor_required
def get_doctor_profile(request):

    user = request.user

    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        messages.info(request, f"Doctor not found")
        return HttpResponseRedirect(reverse('doctor_dashboard'))
    
    ctx = {"doctor": doctor}

    return render(request, "nipps-templates/doctor-profile.html", ctx)

@is_patient_required
def get_patient_profile(request):

    user = request.user

    try:
        patient = Patient.objects.get(user=user)
    except Patient.DoesNotExist:
        messages.info(request, f"Patient not found")
        return HttpResponseRedirect(reverse('patient_dashboard'))
    
    ctx = {"patient": patient}

    return render(request, "nipps-templates/patient-profile.html", ctx)

@is_pharmcist_required
def get_pharmacist_profile(request):

    user = request.user

    try:
        pharmacist = Pharmacist.objects.get(user=user)
    except Pharmacist.DoesNotExist:
        messages.info(request, f"Pharmacist not found")
        return HttpResponseRedirect(reverse('pharmacist_dashboard'))
    
    ctx = {"pharmacist": pharmacist}

    return render(request, "nipps-templates/pharmacist-profile.html", ctx)


@is_lab_technician_required
def get_lab_profile(request):

    user = request.user

    try:
        lab = LabTechnician.objects.get(user=user)
    except LabTechnician.DoesNotExist:
        messages.info(request, f"Lab technician not found")
        return HttpResponseRedirect(reverse('lab_dashboard'))
    
    ctx = {"lab": lab}

    return render(request, "nipps-templates/lab-profile.html", ctx)
    

@is_receptionist_required
def receptionist_complete_profile_view(request):

    if request.method == 'POST':
        
        user = request.user
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        if AdminReceptionist.objects.filter(user=user).exists():
            messages.info(request, f"Admin/Receptionist profile already completed.")
            return HttpResponseRedirect(reverse('admin_receptionist'))

        AdminReceptionist.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            address=address,
            city=city,
            state=state,
            country=country,
            user=user
        )
        
        messages.success(request, f"Profile completed successfully.")
        return HttpResponseRedirect(reverse('admin_receptionist'))
    
    return render(request, "nipps-templates/receptionist-complete-profile.html")


@is_doctor_required
def doctor_complete_profile_view(request):

    if request.method == 'POST':
        
        user = request.user
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        specialty = request.POST.get("specialty")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        if Doctor.objects.filter(user=user).exists():
            messages.info(request, f"Doctor profile already completed.")
            return HttpResponseRedirect(reverse('doctor_dashboard'))

        Doctor.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            address=address,
            city=city,
            state=state,
            country=country,
            specialty=specialty,
            user=user,
            is_available=True
        )
        
        messages.success(request, f"Profile completed successfully.")
        return HttpResponseRedirect(reverse('doctor_dashboard'))
    
    return render(request, "nipps-templates/doctor-complete-profile.html")


@is_pharmcist_required
def pharmacy_complete_profile_view(request):

    if request.method == 'POST':
        
        user = request.user
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        if Pharmacist.objects.filter(user=user).exists():
            messages.info(request, f"Pharmacist profile already completed.")
            return HttpResponseRedirect(reverse('pharmacy_dashboard'))

        Pharmacist.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            address=address,
            city=city,
            state=state,
            country=country,
            user=user
        )
        
        messages.success(request, f"Profile completed successfully.")
        return HttpResponseRedirect(reverse('pharmacy_dashboard'))
    
    return render(request, "nipps-templates/pharmacist-complete-profile.html")

@is_lab_technician_required
def lab_technician_complete_profile_view(request):

    if request.method == 'POST':
        
        user = request.user
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        if LabTechnician.objects.filter(user=user).exists():
            messages.info(request, f"Lab Technician profile already completed.")
            return HttpResponseRedirect(reverse('lab_technician_dashboard'))

        LabTechnician.objects.create(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            address=address,
            city=city,
            state=state,
            country=country,
            user=user
        )
        
        messages.success(request, f"Profile completed successfully.")
        return HttpResponseRedirect(reverse('lab_technician_dashboard'))
    
    return render(request, "nipps-templates/lab-complete-profile.html")

@is_patient_required
def patient_book_appointment_view(request, slug):

    if request.method == 'POST':
        
        user = request.user
        description = request.POST.get("description")
        appointment_date = request.POST.get("appointment_date")

        if BookAppointment.objects.filter(Q(status=PENDING) | Q(status=APPROVED), patient=user).exists():
            messages.info(request, f"You already have a pending appointment")
            return HttpResponseRedirect(reverse('patient_dashboard'))
        
        try:
            doctor = Doctor.objects.get(slug=slug)
        except Doctor.DoesNotExist:
            messages.info(request, f"Doctor not found")
            return HttpResponseRedirect(reverse('patient_appoint'))
        print("descr", description)
        print("descr", appointment_date)
        BookAppointment.objects.create(
            patient = user,
            doctor = doctor.user,
            appointment_date = appointment_date,
            description = description,
            is_booked = True
        )
        messages.success(request, f"Appointment booked successfully. Doctor has received and review your request")
        return HttpResponseRedirect(reverse('patient_dashboard'))
    
    return render(request, "nipps-templates/patient-book-appointment.html")

@is_patient_required
def patient_appoint_view(request):

    doctors = Doctor.objects.filter(is_available=True)
    ctx = {
        "doctors": doctors
     }
    
    return render(request, "nipps-templates/patient-appointment.html", ctx)


@is_patient_required
def get_patient_appointments_view(request):

    user = request.user
    appointments = BookAppointment.objects.filter(patient=user)
    ctx = {
        "appointments": appointments
     }
    
    return render(request, "nipps-templates/get-patient-appointment.html", ctx)

@is_receptionist_required
def appointments_receptionist_view(request):

    ctx = {}
    ctx_array = []
    appointments = BookAppointment.objects.all()
    for appoint in appointments:
        try:
            doctor = Doctor.objects.get(user=appoint.doctor)
        except Doctor.DoesNotExist:
            pass
        try:
            patient = Patient.objects.get(user=appoint.patient)
        except Patient.DoesNotExist:
            pass

        ctx["doctor_first_name"] = doctor.first_name
        ctx["doctor_last_name"] = doctor.first_name
        ctx["doctor_email"] = doctor.user.email
        ctx["patient_first_name"] = patient.first_name
        ctx["patient_last_name"] = patient.last_name
        ctx["patient_email"] = patient.user.email
        ctx["patient_file_number"] = patient.file_number
        ctx["appointment_date"] = appoint.appointment_date
        ctx["appointment_status"] = appoint.status
        ctx_array.append(ctx)
    
    response_ctx = {
        "appointments": ctx_array
    }
    return render(request, "nipps-templates/appointments-receptionist.html", response_ctx)

@is_doctor_required
def appointments_request_view(request):

    ctx = {}
    ctx_array = []
    user = request.user 
    appointments = BookAppointment.objects.filter(doctor=user, status=PENDING)
    for appoint in appointments:
        try:
            patient = Patient.objects.get(user=appoint.patient)
        except Patient.DoesNotExist:
            pass

        ctx["patient_first_name"] = patient.first_name
        ctx["patient_last_name"] = patient.last_name
        ctx["patient_email"] = patient.user.email
        ctx["patient_file_number"] = patient.file_number
        ctx["appointment_date"] = appoint.appointment_date
        ctx["appointment_status"] = appoint.status
        ctx["id"] = appoint.id # change later to slug
        ctx_array.append(ctx)
    
    response_ctx = {
        "appointments": ctx_array
    }
    return render(request, "nipps-templates/appointments-request.html", response_ctx)


@is_doctor_required
def appointments_approved_view(request):

    ctx = {}
    ctx_array = []
    user = request.user
    appointments = BookAppointment.objects.filter(doctor=user, status=APPROVED)
    for appoint in appointments:
        try:
            patient = Patient.objects.get(user=appoint.patient)
        except Patient.DoesNotExist:
            pass

        ctx["patient_first_name"] = patient.first_name
        ctx["patient_last_name"] = patient.last_name
        ctx["patient_email"] = patient.user.email
        ctx["patient_file_number"] = patient.file_number
        ctx["appointment_date"] = appoint.appointment_date
        ctx["appointment_status"] = appoint.status
        ctx_array.append(ctx)
    
    response_ctx = {
        "appointments": ctx_array
        
    }
    return render(request, "nipps-templates/appointments-approved.html", response_ctx)


@is_doctor_required
def doctor_approve_appointment_view(request, pk):

    try:
        appointment = BookAppointment.objects.get(id=pk)
    except BookAppointment.DoesNotExist:
        messages.info(request, f"Appointment not found")
        return HttpResponseRedirect(reverse('doctor_dashboard'))

    if appointment.status == APPROVED or appointment.status == ATTENDED:
        messages.info(request, f"Appointment already approved or attended")
        return HttpResponseRedirect(reverse('doctor_dashboard'))
    
    appointment.status = APPROVED
    appointment.save()
    
    messages.success(request, f"Appointment approved successfully")
    return HttpResponseRedirect(reverse('doctor_dashboard'))

@is_doctor_required
def doctor_attend_patient_view(request):
     
    if request.method == 'POST':
        
        file_number = request.POST.get("file_number")
        
        try:
            patient = Patient.objects.get(file_number=file_number)
        except Patient.DoesNotExist:
            messages.success(request, f"Patient not found")
            return HttpResponseRedirect(reverse('doctor_attend_patient'))
        messages.success(request, f"found")
        return HttpResponseRedirect(reverse('doctor_get_patient', kwargs={"slug": patient.slug }))
  
    return render(request, "nipps-templates/doctor-attend-patient.html")

@is_doctor_required
def doctor_get_patient_view(request, slug):
       
    try:
        patient = Patient.objects.get(slug=slug)
    except Patient.DoesNotExist:
        messages.success(request, f"Patient not found")
        return HttpResponseRedirect(reverse('doctor_attend_patient'))
    
    ctx = {
        "patient": patient
    }
    
    return render(request, "nipps-templates/doctor-get-patient.html", ctx)

@is_doctor_required
def doctor_request_patient_test_view(request, slug):

    
    if request.method == 'POST':
        user = request.user
        try:
            patient = Patient.objects.get(slug=slug)
        except Patient.DoesNotExist:
            messages.info(request, f"Patient not found")
            return HttpResponseRedirect(reverse('doctor_get_patient'))
        
        if PatientDiagnostic.objects.filter(patient=patient.user, lab_test_performed=False).exists():
            messages.info(request, f"Request to test this patient already existed")
            return HttpResponseRedirect(reverse('doctor_dashboard'))
        
        description = request.POST.get("description")
    
        PatientDiagnostic.objects.create(
            patient = patient.user,
            prescribed_by = user,
            description = description,
            lab_test_requested = True
        )
        messages.success(request, f"Request for test successfully send to Lab")
        return HttpResponseRedirect(reverse('doctor_dashboard'))
    
    return render(request, "nipps-templates/doctor-request-patient-test.html")


@is_doctor_required
def doctor_patient_prescription_view(request, slug):
    
    if request.method == 'POST':
        user = request.user
        try:
            patient = Patient.objects.get(slug=slug)
        except Patient.DoesNotExist:
            messages.info(request, f"Patient not found")
            return HttpResponseRedirect(reverse('doctor_get_patient'))
        
        if PatientDiagnostic.objects.filter(patient=patient.user, lab_test_requested=True, lab_test_performed=False).exists():
            messages.info(request, f"Result for this Patient test not yet out")
            return HttpResponseRedirect(reverse('doctor_patient_prescription', kwargs={"slug": patient.slug}))
        
        description = request.POST.get("description")
        
        patient_diag = PatientDiagnostic.objects.create(
            patient = patient.user,
            prescribed_by = user,
            description = description,
        )
        Prescription.objects.create(
            diagnostic_report = patient_diag,
            prescription = description,
            is_prescribed = True
        )
    
        messages.success(request, f"Prescription successfully sent to Pharmacy")
        return HttpResponseRedirect(reverse('doctor_dashboard'))
    
    return render(request, "nipps-templates/doctor-patient-prescription.html")

@is_doctor_required
def doctor_get_patient_results_view(request, slug):
    
    user = request.user
    try:
        patient = Patient.objects.get(slug=slug)
    except Patient.DoesNotExist:
        messages.info(request, f"Patient not found")
        return HttpResponseRedirect(reverse('doctor_get_patient'))
        
    patient_diagnostics = PatientDiagnostic.objects.filter(prescribed_by=user, patient=patient.user, lab_test_requested=True)
    ctx = {
        "patient_diagnostics": patient_diagnostics
    }
    return render(request, "nipps-templates/doctor_get_patient_results.html", ctx)


@is_doctor_required
def doctor_patient_test_prescription_view(request, pk):
    
    if request.method == 'POST':
       
        try:
            patient_diag = PatientDiagnostic.objects.get(id=pk)
        except PatientDiagnostic.DoesNotExist:
            messages.info(request, f"PatientDiagnostic not found")
            return HttpResponseRedirect(reverse('doctor_dashboard'))
        
        if not patient_diag.lab_test_result:
            messages.info(request, f"Patient has been requested for test and result not out yet")
            return HttpResponseRedirect(reverse('doctor_dashboard'))
        
        
        if Prescription.objects.filter(diagnostic_report=patient_diag,).exists():
            messages.info(request, f"Patient prescription already existed")
            return HttpResponseRedirect(reverse('doctor_dashboard'))
        
        description = request.POST.get("description")
        
        Prescription.objects.create(
            diagnostic_report = patient_diag,
            prescription = description,
            is_prescribed = True
        )
    
        messages.success(request, f"Prescription successfully sent to Pharmacy")
        return HttpResponseRedirect(reverse('doctor_dashboard'))
    
    return render(request, "nipps-templates/doctor-patient-test-prescription.html")


@is_doctor_required
def doctor_update_availabilty_view(request):
        
    user = request.user

    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        messages.info(request, f"Doctor not found")
        return HttpResponseRedirect(reverse('doctor_profile'))
    
    if doctor.is_available:
        doctor.is_available = False
    else:
        doctor.is_available = True

    doctor.save()
        
    messages.info(request, f"Availability updated successfully")
    return HttpResponseRedirect(reverse('doctor_profile'))


@is_lab_technician_required
def patient_to_be_tested_view(request):
        
    patient_diags = PatientDiagnostic.objects.filter(lab_test_requested=True)
    ctx = {
        "patient_diags": patient_diags
    }       
    
    return render(request, "nipps-templates/patient-to-be-tested.html", ctx)


@is_lab_technician_required
def patient_tested_upload_result_view(request, pk):

    if request.method == 'POST':    
        try:
            patient_diag = PatientDiagnostic.objects.get(id=pk)
        except PatientDiagnostic.DoesNotExist:
            messages.info(request, f"PatientDiagnostic not found")
            return HttpResponseRedirect(reverse('patient_to_be_tested'))
        
        description = request.POST.get("description")
        patient_diag.lab_test_result = description
        patient_diag.lab_test_performed = True
        patient_diag.save()

        messages.success(request, f"Test result updated successfully")
        return HttpResponseRedirect(reverse('lab_technician_dashboard'))
          
    return render(request, "nipps-templates/patient-tested-upload.html")


@is_lab_technician_required
def patients_tested_results_view(request):
        
    patient_diags = PatientDiagnostic.objects.filter(lab_test_performed=True)
    ctx = {
        "patient_diags": patient_diags
    }       
    
    return render(request, "nipps-templates/patient-tested-results.html", ctx)

@is_pharmcist_required
def pharmacist_search_patient_view(request):

    if request.method == 'POST':
        
        file_number = request.POST.get("file_number")
        
        try:
            patient = Patient.objects.get(file_number=file_number)
        except Patient.DoesNotExist:
            messages.success(request, f"Patient not found")
            return HttpResponseRedirect(reverse('pharmacy_dashboard'))
       
        return HttpResponseRedirect(reverse('pharmacist_get_patient', kwargs={"slug": patient.slug }))
  
        
    return render(request, "nipps-templates/pharmacist-search-patient.html")


@is_pharmcist_required
def pharmacist_get_patient_view(request, slug):
       
    try:
        patient = Patient.objects.get(slug=slug)
    except Patient.DoesNotExist:
        messages.success(request, f"Patient not found")
        return HttpResponseRedirect(reverse('pharmacy_dashboard'))
    patient_diags = PatientDiagnostic.objects.filter(patient=patient.user)

    prescription_object = {}
    for _ in patient_diags:
        prescriptions = Prescription.objects.filter(diagnostic_report__patient=patient.user)
        for i in prescriptions:
            prescription_object['prescription'] = i.prescription
            prescription_object["is_prescribed"] = i.is_prescribed
            prescription_object["prescription_date"] = i.prescription_date

    ctx = {
        "patient": patient,
        "prescription_data": prescription_object
    }
    
    return render(request, "nipps-templates/pharmacist-get-patient.html", ctx)

@is_pharmcist_required
def pharmacist_make_payment_view(request, slug):

    if request.method == 'POST':
       
        try:
            patient = Patient.objects.get(slug=slug)
        except Patient.DoesNotExist:
            messages.success(request, f"Patient not found")
            return HttpResponseRedirect(reverse('pharmacy_dashboard'))
        
        user_amount = int(request.POST.get("amount"))
        amount = user_amount * 100
        
        reference = Helper.reference_generator()
        email = patient.user.email 
        first_name = patient.first_name 
        last_name = patient.last_name
        country_code = patient.user.country_code
        phone_number = patient.user.phone_number
        patient_user = patient.user

        res = PayStackRequestHelper.send_payment(patient_user, request, reference, email, amount, first_name, last_name)
        if res is not None:
            payment_link = res["data"]["authorization_url"]
            print("pay linki   ", payment_link)
            Helper.send_patient_payment_link_email(
            email, user_amount, payment_link
            )
            Helper.send_patient_payment_link_sms(
                user_amount, payment_link, 
                country_code, phone_number)
            messages.success(request, f"Payment link succesfully sent to Patient phone number and email")
            return HttpResponseRedirect(reverse('pharmacy_dashboard'))
        messages.info(request, f"Something went wrong. Please contact support")
        return HttpResponseRedirect(reverse('pharmacy_dashboard'))
    return render(request, "nipps-templates/pharmacist-make-payment.html")

@is_pharmcist_required
def verify_payment_view(request, **kwargs):
    import requests
    from django.shortcuts import get_object_or_404

    transaction = get_object_or_404(Transaction, ref=kwargs["ref"])
    if transaction.verified:
        messages.info(request, f"Transaction already verified")
        return HttpResponseRedirect(reverse('pharmacy_dashboard'))
    res = requests.get(
        f"{PayStackRequestHelper.VERIFY_TRANSACTION_URL}{transaction.ref}",
        headers=PayStackRequestHelper.AUTHORIZED_HEADER
    ).json()
    if res["status"]:
        # Verify currency type, actual amount paid and status
        if res["data"]["status"] == "success" and res["data"]["currency"] == "NGN" \
            and res["data"]["amount"] >= transaction.amount:
            transaction.verified = True
            transaction.save()

            messages.info(request, f"Payment verified successfully")
            return HttpResponseRedirect(reverse('home'))

        messages.info(request, f"Somthin went wrong. Contact Admin")
        return HttpResponseRedirect(reverse('home'))
    messages.info(request, f"Somthin went wrong. Contact Admin")
    return HttpResponseRedirect(reverse('home'))

@is_pharmcist_required
def pharmacist_check_patient_payment_view(request):

    if request.method == 'POST':
        
        file_number = request.POST.get("file_number")
        
        try:
            patient = Patient.objects.get(file_number=file_number)
        except Patient.DoesNotExist:
            messages.success(request, f"Patient not found")
            return HttpResponseRedirect(reverse('pharmacy_dashboard'))
        
        try:
            transaction = Transaction.objects.get(user=patient.user)
        except Transaction.DoesNotExist:
            messages.success(request, f"Transaction not found")
            return HttpResponseRedirect(reverse('pharmacy_dashboard'))
       
        return HttpResponseRedirect(reverse('pharmacist_confirm_patient_payment', kwargs={"ref": transaction.ref}))
       
        
    return render(request, "nipps-templates/pharmacist-check-patient-payment.html")


@is_pharmcist_required
def pharmacist_confirm_patient_payment_view(request, ref):
        
    try:
        transaction = Transaction.objects.get(ref=ref)
    except Transaction.DoesNotExist:
        messages.success(request, f"Transaction not found")
        return HttpResponseRedirect(reverse('pharmacy_dashboard'))
    
    ctx = {
        "transaction": transaction,
        "amount": transaction.amount / 100
    }
    return render(request, "nipps-templates/pharmacist-confirm-patient-payment.html", ctx)
