from datetime import datetime
import pytz

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from nipps_hms.utils import generate_slug_code
from accounts.models import _generate_code

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
PARTICIPANT = "Participant"
ENROLLEE = "Enrollee"

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

PATIENT_TYPE_CHOICES = ((PARTICIPANT, "Participant"), (ENROLLEE, "Enrollee"),)


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
        return f"Doctor {self.first_name}"


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
        return f"Pharmacist {self.first_name}"
    

class AccountsRecords(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_accountant")
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
        return f"Accountant {self.first_name}"


class LabTechnician(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_lab_technician")
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
        return f"Lab Technician {self.first_name}"

class Spouse(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    
    file_number = models.CharField(max_length=15, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
           
        super().save(*args, **kwargs)


class PatientPrincipal(models.Model):
    
    slug = models.SlugField(editable=False)
    patient_type = models.CharField(
        max_length=20, choices=PATIENT_TYPE_CHOICES)
    nhis_number = models.CharField(max_length=10)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    file_number = models.CharField(max_length=15, null=True, blank=True)

    spouse = models.OneToOneField(Spouse, on_delete=models.CASCADE, related_name="spouse_patient", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
            
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("-created_at", )

    @property
    def children(self):
        children = self.patient_principal_children.all()
        return children if children else None

    def __str__(self):
        return f" {self.first_name}"


class Children(models.Model):
    
    slug = models.SlugField(editable=False)

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    
    file_number = models.CharField(max_length=15, null=True, blank=True)

    patient_principal = models.ForeignKey(PatientPrincipal, on_delete=models.CASCADE, related_name="patient_principal_children")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
    
        super().save(*args, **kwargs)


class Nurse(models.Model):
    
    slug = models.SlugField(editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES)
   
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name="user_nurse")
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
        return f"Nurse {self.first_name}"


class BookAppointment(models.Model):
    
    slug = models.SlugField(editable=False)
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

    slug = models.SlugField(editable=False)
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
    
    slug = models.SlugField(editable=False)
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
    
    slug = models.SlugField(editable=False)
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

    slug = models.SlugField(editable=False)
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
    

class DeathReport(models.Model):

    slug = models.SlugField(editable=False)
    patient_name = models.CharField(max_length=100)
    date_of_death = models.DateField()
    cause_of_death = models.TextField()
    attending_physician = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Death Report for {self.patient_name}"


class BirthReport(models.Model):

    slug = models.SlugField(editable=False)
    baby_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=255)
    parent_names = models.CharField(max_length=255)
    attending_physician = models.CharField(max_length=255)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Birth Report")
        verbose_name_plural = _("Birth Reports")

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.baby_name
    

class BloodBankReport(models.Model):
    blood_group_choices = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    slug = models.SlugField(editable=False)
    donor_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=blood_group_choices)
    donation_date = models.DateField()
    quantity_ml = models.PositiveIntegerField()
    donor_contact = models.CharField(max_length=15)
    notes = models.TextField(blank=True, null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Blood Bank Report")
        verbose_name_plural = _("Blood Bank Reports")

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Blood Bank Report for {self.donor_name}"


class Ward(models.Model):

    slug = models.SlugField(editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    capacity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Bed(models.Model):

    slug = models.SlugField(editable=False)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=20)
    is_occupied = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bed_number} - {self.ward}"

class Cabin(models.Model):

    slug = models.SlugField(editable=False)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    cabin_number = models.CharField(max_length=20)
    is_occupied = models.BooleanField(default=False)
    capacity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cabin_number} - {self.ward}"

class Admission(models.Model):

    slug = models.SlugField(editable=False)
    patient = models.ForeignKey(PatientPrincipal, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, blank=True, null=True)
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE, blank=True, null=True)
    admitted_at = models.DateTimeField(auto_now_add=True)
    discharged = models.BooleanField(default=False)
    discharged_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Admission for {self.patient.name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):

        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        
            self.bed.is_occupied = True
            self.bed.save()
           
            self.cabin.is_occupied = True
            self.cabin.save()

        super().save(*args, **kwargs)

    def discharge(self):
        # Mark the bed or cabin as available when discharging the patient
        if self.bed:
            self.bed.is_occupied = False
            self.bed.save()
        if self.cabin:
            self.cabin.is_occupied = False
            self.cabin.save()

        self.discharged = True
        self.discharged_at = datetime.now(pytz.utc)
        self.save()


class Medicine(models.Model):

    slug = models.SlugField(editable=False)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    expiration_date = models.DateField()
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        """
        Check if the medicine has expired.
        Returns:
            bool: True if the medicine has expired, False otherwise.
        """
        return self.expiration_date.date() < datetime.now(pytz.utc).date()

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Operation(models.Model):

    slug = models.SlugField(editable=False)
    patient = models.ForeignKey(PatientPrincipal, on_delete=models.DO_NOTHING, related_name='patient_operations')
    surgeon = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING, related_name='surgeon_operations')
    operation_date = models.DateField()
    description = models.TextField()
    is_performed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Operation for  on {self.operation_date}"


class PrincipalContinuationSheet(models.Model):
    
    slug = models.SlugField(editable=False)

    description = models.TextField(null=True, blank=True)

    patient_principal = models.OneToOneField(PatientPrincipal, on_delete=models.CASCADE, related_name='patient_principal_principal_continuation_sheet')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
           
        super().save(*args, **kwargs)


class SpouseContinuationSheet(models.Model):
    
    slug = models.SlugField(editable=False)

    description = models.TextField(null=True, blank=True)

    spouse = models.OneToOneField(Spouse, on_delete=models.CASCADE, related_name='spouse_spouse_continuation_sheet')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
           
        super().save(*args, **kwargs)


class ChildContinuationSheet(models.Model):
    
    slug = models.SlugField(editable=False)

    description = models.TextField(null=True, blank=True)

    child = models.OneToOneField(Children, on_delete=models.CASCADE, related_name='child_child_continuation_sheet')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_code = generate_slug_code()
            self.slug = slugify(slug_code)
           
        super().save(*args, **kwargs)
