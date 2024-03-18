from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import  (PatientPrincipal, Doctor, Nurse, Pharmacist, AccountsRecords,
                      LabTechnician, Children, Spouse, PrincipalContinuationSheet,
                      ChildContinuationSheet, SpouseContinuationSheet,
                      ChildTestRequestSheet, SpouseTestRequestSheet,
                      PrincipalPatientTestRequestSheet, PrincipalPatientPrescriptionForm,
                      ChildPrescriptionForm, SpousePrescriptionForm,
                      )
from accounts.serializers import CustomUserDetailsSerializer
from accounts.models import _generate_code

class PrincipalSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientPrincipal
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ChildrenSingleSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Children
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

class SpouseSingleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spouse
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ChildrenSerializer(serializers.ModelSerializer):

    principal = serializers.SerializerMethodField("get_patient_principal")
    
    class Meta:
        model = Children
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate_date_of_birth(self, value):
        from datetime import datetime, timedelta
        import pytz

        date_diff = datetime.now(pytz.utc).date() - value
        max_years_in_days = timedelta(days=365*18)

        if date_diff >= max_years_in_days:
            raise serializers.ValidationError(f"Children Age must be below 18 age.")

        return value
    
    def get_patient_principal(self, obj):
        return PrincipalSerializer(obj.patient_principal).data


class SpouseSerializer(serializers.ModelSerializer):

    principal = serializers.SerializerMethodField("get_patient_principal")

    class Meta:
        model = Spouse
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_patient_principal(self, obj):
        return PrincipalSerializer(obj.spouse_patient).data


class PatientSerializer(serializers.ModelSerializer):


    class Meta:
        model = PatientPrincipal
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class PatientPrincipalSerializer(serializers.ModelSerializer):
    
    spouse = SpouseSerializer(required=False)
    children = serializers.SerializerMethodField("get_children")

    class Meta:
        model = PatientPrincipal
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    
    def create(self, validated_data):

        spouse_data = validated_data.pop("spouse", None)
        last_name = validated_data.get("last_name", None)
        
        if spouse_data:

            spouse_serializer = SpouseSerializer(data=spouse_data)
            spouse_serializer.is_valid(raise_exception=True)
            spouse = spouse_serializer.save()
            spouse_code_number = _generate_code()
            spouse.file_number = f"nipss-{spouse_code_number}"
            spouse.last_name = last_name
            spouse.save()
            validated_data["spouse"] = spouse
        
        patient_principal = super().create(validated_data)

        code_number = _generate_code()
        patient_principal.file_number = f"nipss-{code_number}"
        patient_principal.save()

        return patient_principal
        
    def validate_nhis_number(self, value):

        if PatientPrincipal.objects.filter(nhis_number=value).exists():
            raise serializers.ValidationError("NHIS number already exists.")
        return value
    
    def get_children(self, obj):
        return ChildrenSerializer(obj.children, many=True).data


class DoctorProfileSerializer(serializers.ModelSerializer):
    
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):

        user = self.context.get("request").user
        if Doctor.objects.filter(user=user).exists():
            raise serializers.ValidationError("Doctor profile already exist.")
        return data


class NurseProfileSerializer(serializers.ModelSerializer):
    
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Nurse
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
    
    def validate(self, data):

        user = self.context.get("request").user
        if Nurse.objects.filter(user=user).exists():
            raise serializers.ValidationError("Nurse profile already exist.")
        return data

class AccountantProfileSerializer(serializers.ModelSerializer):
    
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = AccountsRecords
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):

        user = self.context.get("request").user
        if AccountsRecords.objects.filter(user=user).exists():
            raise serializers.ValidationError("Accounts profile already exist.")
        return data


class LabTechnicianProfileSerializer(serializers.ModelSerializer):
    
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = LabTechnician
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):

        user = self.context.get("request").user
        if LabTechnician.objects.filter(user=user).exists():
            raise serializers.ValidationError("Lab profile already exist.")
        return data

class PharmarcistProfileSerializer(serializers.ModelSerializer):
    
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Pharmacist
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):

        user = self.context.get("request").user
        if Pharmacist.objects.filter(user=user).exists():
            raise serializers.ValidationError("Pharmacist profile already exist.")
        return data


class SearchPatientByNHISSerializer(serializers.Serializer):
    
    nhis_number = serializers.CharField(max_length=20)

class SearchPatientByFileNumberSerializer(serializers.Serializer):
    
    file_number = serializers.CharField(max_length=20)

class SearchSpouseByFileNumbererializer(serializers.Serializer):
    
    file_number = serializers.CharField(max_length=20)

class SearchChildByFileNumberSerializer(serializers.Serializer):
    
    file_number = serializers.CharField(max_length=20)


class PrincipalContinuationSheetSerializer(serializers.ModelSerializer):
    
    patient_principal = PrincipalSerializer(read_only=True)
    description = serializers.CharField()

    class Meta:
        model = PrincipalContinuationSheet
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):

        request = self.context.get('request')
        
        if request.method == "POST":
            description = data.get("description")
            if not description:
                raise serializers.ValidationError("Please provide update description")
            
            return data


class SpouseContinuationSheetSerializer(serializers.ModelSerializer):
    
    spouse = SpouseSingleSerializer(read_only=True)
    description = serializers.CharField()

    class Meta:
        model = SpouseContinuationSheet
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):

        request = self.context.get('request')
        
        if request.method == "POST":
            description = data.get("description")
            if not description:
                raise serializers.ValidationError("Please provide update description")
            
            return data


class ChildContinuationSheetSerializer(serializers.ModelSerializer):
    
    child = ChildrenSingleSerializer(read_only=True)
    description = serializers.CharField()

    class Meta:
        model = ChildContinuationSheet
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):

        request = self.context.get('request')
        
        if request.method == "POST":
            description = data.get("description")
            if not description:
                raise serializers.ValidationError("Please provide update description")
            
            return data
        

class ChildTestRequestSerializer(serializers.ModelSerializer):

    patient_child = serializers.SerializerMethodField("get_patient_child")

    class Meta:
        model = ChildTestRequestSheet
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_patient_child(self, obj):

        try:
            child = Children.objects.get(id=obj.child.id)
        except Children.DoesNotExist:
            return
        return ChildrenSingleSerializer(child).data


class SpouseTestRequestSerializer(serializers.ModelSerializer):
    patient_spouse = serializers.SerializerMethodField("get_patient_spouse")

    class Meta:
        model = SpouseTestRequestSheet
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_patient_spouse(self, obj):
        try:
            spouse = Spouse.objects.get(id=obj.spouse.id)
        except Spouse.DoesNotExist:
            return
        return SpouseSingleSerializer(spouse).data
    

class PrincipalPatientTestRequestSerializer(serializers.ModelSerializer):

    patient = serializers.SerializerMethodField("get_principal_patient")

    class Meta:
        model = PrincipalPatientTestRequestSheet
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def get_principal_patient(self, obj):
        try:
            patient = PatientPrincipal.objects.get(id=obj.principal_patient.id)
        except PatientPrincipal.DoesNotExist:
            return
        return PrincipalSerializer(patient).data
    


class UploadTestRequestSerializer(serializers.Serializer):

    upload_result = serializers.CharField()


class PrincipalPatientPrescriptionFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrincipalPatientPrescriptionForm
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ChildPrescriptionFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChildPrescriptionForm
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class SpousePrescriptionFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpousePrescriptionForm
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")



class BillPrescriptionSerializer(serializers.Serializer):

    amount = serializers.IntegerField()