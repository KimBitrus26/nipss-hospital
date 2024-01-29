from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from nipps_hms.utils import generate_slug_code
from nipps_hms.utils import validate_file
User = get_user_model()

PENDING = "Pending"
APPROVED = "Approved"
DENIED = "Denied"
INSUFFICIENT = "Insufficient"
ACTIVE = "Active"
SUSPENDED = "Suspended"
EXPIRED = "Expired"
CLAIMED = "Claimed"
REFUNDED = "Refunded"
ACCEPTED = "Accepted"
COMPLETED = "Completed"
DISPUTED = "Disputed"
VERIFIED = "Verified"
ATTENDED = "Attended"
MALE = "Male"
FEMALE = "Female"
OTHER = "Other"

STATUS_CHOICES = ((PENDING, "Pending"), (APPROVED, "Approved"),
                      (DENIED, "Denied"), (INSUFFICIENT, "Insufficient"),)

LICENCE_STATUS_CHOICES = ((ACTIVE, "Active"), (SUSPENDED, "Suspended"),
                      (EXPIRED, "Expired"),)

REQUEST_STATUS = ((PENDING, "Pending"), (ACCEPTED, "Accepted"),
                    (COMPLETED, "Completed"), (DISPUTED, "Disputed"),)

ACCEPT_REQUEST_STATUS = ((ACCEPTED, "Accepted"),
                      (COMPLETED, "Completed"),)

PAYMENT_STATUS_CHOICES = ((PENDING, "Pending"), (VERIFIED, "Verified"), (CLAIMED, "Claimed"), (REFUNDED, "Refunded"))

GENDER_CHOICES = ((MALE, "Male"), (FEMALE, "Female"),
                      (OTHER, "Other"),)
BOOKING_STATUS_CHOICES = ((PENDING, "Pending"), (APPROVED, "Approved"),
                      (ATTENDED, "Attended"),)



class Doctor(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_doctor")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256, default="Nigeria")
    specialty = models.CharField(max_length=256)
   
    is_available = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"Agent Application for Agent {self.first_name}"


class Pharmacist(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_pharmacist")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256, default="Nigeria")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"Agent Application for Agent {self.first_name}"


class LabTechnician(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_lab")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256, default="Nigeria")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"Agent Application for Agent {self.first_name}"


class Patient(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    age = models.CharField(
        max_length=10)
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="patient_user")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256, default="Nigeria")

    file_number = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f" {self.first_name}"


class AdminReceptionist(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
   
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_admin")
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    country = models.CharField(max_length=256, default="Nigeria")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", )

    def __str__(self):
        return f"Agent Application for Agent {self.first_name}"


class BookAppointment(models.Model):
    # slug = models.SlugField(editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_patient_booking")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_doctor_booking")
    appointment_date = models.DateField(auto_now=True)
    description = models.TextField(max_length=500)
    is_booked = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default=PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment for {self.patient.first_name} with {self.doctor.first_name} on {self.appointment_date}"
    

class PatientDiagnostic(models.Model):

    # slug = models.SlugField(editable=False)

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_patient_diagnostic")
    prescribed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    lab_test_requested = models.BooleanField(default=False)
    lab_test_performed = models.BooleanField(default=False)
    lab_test_result = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Diagnostic"


class LabTestResult(models.Model):
    # slug = models.SlugField(editable=False)
    diagnostic_report = models.ForeignKey(PatientDiagnostic, on_delete=models.CASCADE, related_name="lab_test_result_diagnotic")
    lab_technician = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_lab_test_result")
    test_date = models.DateField(auto_now=True)
    result = models.TextField()
    is_result_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Lab Test"


class Prescription(models.Model):
    # slug = models.SlugField(editable=False)
    diagnostic_report = models.ForeignKey(PatientDiagnostic, on_delete=models.CASCADE, related_name="prescription_diagnostic_report")
    
    prescription = models.TextField()
    is_prescribed = models.BooleanField(default=False)
    prescription_date = models.DateField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    ref = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prescription"
    
class Pharmacy(models.Model):
    # slug = models.SlugField(editable=False)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="pharmacy_prescription")  
    medications = models.TextField()
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pharmacy"
    
class Transaction(models.Model):
    """Model to represent Transaction."""

    ref = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transaction_user", null=True, blank=True)  
    email = models.CharField(max_length=355)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    verified = models.BooleanField(default=False)

    def verify(self):
        self.verified = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.ref)