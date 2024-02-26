from rest_framework import status
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (CreateAPIView, RetrieveAPIView, ListAPIView, 
                                     UpdateAPIView, DestroyAPIView,)

from .serializers import  (PatientPrincipalSerializer, DoctorProfileSerializer,
                           PharmarcistProfileSerializer, 
                           LabTechnicianProfileSerializer,
                           NurseProfileSerializer,
                           AccountantProfileSerializer,
                           ChildrenSerializer, SpouseSerializer,
                           PrincipalSerializer, ChildrenSingleSerializer,
                           SpouseSingleSerializer, SearchPatientByNHISSerializer,
                           SearchChildByFileNumberSerializer,
                           SearchPatientByFileNumberSerializer,
                           SearchSpouseByFileNumbererializer,
                           PrincipalContinuationSheetSerializer,
                           SpouseContinuationSheetSerializer,
                           ChildContinuationSheetSerializer,
                           
                           )
from nipps_hms.permission import (IsAuthenticatedNurse,
                                  IsAuthenticatedDoctor,
                                  IsAuthenticatedAccountsRecord,
                                  IsAuthenticatedLabTechnician,
                                  IsAuthenticatedPharmacist,
                                        )

from accounts.models import _generate_code
from .models import (PatientPrincipal, Spouse, Children, Prescription,
                     PrincipalContinuationSheet, ChildContinuationSheet,
                     SpouseContinuationSheet, Doctor, Pharmacist, AccountsRecords,
                     LabTechnician, Nurse,
                     
                     )


class CreatePatientView(CreateAPIView):

    permission_classes = (IsAuthenticatedAccountsRecord, )
    serializer_class = PatientPrincipalSerializer

    @transaction.atomic
    def post(self, request,  format=None):
        
        children = request.data.get("children")
        if children and len(children) > 4:
            return Response({"message": "Children cannot be more than 4."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(raise_exception=True):

            last_name = serializer.validated_data["last_name"]

            patient = serializer.save()
            if children:
                for child in children if children else None:
                    
                    child["patient_principal"] = patient.id
                    code_number = _generate_code()
                    child["file_number"] = f"nipss-{code_number}"
                    child["last_name"] = last_name
                    
                    child_serializer = ChildrenSerializer(data=child)
                    child_serializer.is_valid(raise_exception=True)
                    child_serializer.save()
                
            return Response({"message": "Patient file created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "An error occured, please try again."}, status=status.HTTP_400_BAD_REQUEST)
        

class CreateDoctorProfileView(CreateAPIView):

    permission_classes = (IsAuthenticatedDoctor, )
    serializer_class = DoctorProfileSerializer


    def post(self, request,  format=None):

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            
            doctor = serializer.save(user=self.request.user, is_available=True)
            doctor.user.is_profile_completed = True
            doctor.user.save()
            return Response({"message": "Doctor profile created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "An error occured, please try again."}, status=status.HTTP_400_BAD_REQUEST)


class GetDoctorDetailsView(APIView):
    
    permission_classes = (IsAuthenticatedDoctor, )
    serializer_class = DoctorProfileSerializer

    def get(self, request, *args, **kwargs):
        try:
            doctor = Doctor.objects.get(user=self.request.user)
        except Doctor.DoesNotExist:
            return Response({"message": "Doctor not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(doctor)
        return Response({"message": "Retrieved doctor successfully", "data": serializer.data}, status=status.HTTP_200_OK)
     

class CreateNurseProfileView(CreateAPIView):

    permission_classes = (IsAuthenticatedNurse, )
    serializer_class = NurseProfileSerializer


    def post(self, request,  format=None):

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            
            nurse = serializer.save(user=self.request.user)
            nurse.user.is_profile_completed = True
            nurse.user.save()
            return Response({"message": "Nurse profile created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "An error occured, please try again."}, status=status.HTTP_400_BAD_REQUEST)


class GetNurseDetailsView(APIView):

    permission_classes = (IsAuthenticatedNurse, )
    serializer_class = NurseProfileSerializer

    def get(self, request, *args, **kwargs):
        try:
            nurse = Nurse.objects.get(user=self.request.user)
        except Nurse.DoesNotExist:
            return Response({"message": "Nurse not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(nurse)
        return Response({"message": "Retrieved nurse successfully", "data": serializer.data}, status=status.HTTP_200_OK)
     

class CreatePharmacistProfileView(CreateAPIView):

    permission_classes = (IsAuthenticatedPharmacist, )
    serializer_class = PharmarcistProfileSerializer


    def post(self, request,  format=None):

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            
            pharmacist = serializer.save(user=self.request.user)
            pharmacist.user.is_profile_completed = True
            pharmacist.user.save()
            return Response({"message": "Pharmacist profile created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "An error occured, please try again."}, status=status.HTTP_400_BAD_REQUEST)
        

class GetPharmacistDetailsView(APIView):
    
    permission_classes = (IsAuthenticatedPharmacist, )
    serializer_class = PharmarcistProfileSerializer

    def get(self, request, *args, **kwargs):
        try:
            pharmacist = Pharmacist.objects.get(user=self.request.user)
        except Pharmacist.DoesNotExist:
            return Response({"message": "Pharmacist not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(pharmacist)
        return Response({"message": "Retrieved pharmacist successfully", "data": serializer.data}, status=status.HTTP_200_OK)
     

class CreateAccountantProfileView(CreateAPIView):

    permission_classes = (IsAuthenticatedAccountsRecord, )
    serializer_class = AccountantProfileSerializer

    def post(self, request,  format=None):

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            
            accounts = serializer.save(user=self.request.user)
            accounts.user.is_profile_completed = True
            accounts.user.save()
            return Response({"message": "Accounts/records profile created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "An error occured, please try again."}, status=status.HTTP_400_BAD_REQUEST)
        

class GetAccountsDetailsView(APIView):
   
    permission_classes = (IsAuthenticatedAccountsRecord, )
    serializer_class = AccountantProfileSerializer

    def get(self, request, *args, **kwargs):
        try:
            account = AccountsRecords.objects.get(user=self.request.user)
        except AccountsRecords.DoesNotExist:
            return Response({"message": "Accounts not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(account)
        return Response({"message": "Retrieved accounts/records successfully", "data": serializer.data}, status=status.HTTP_200_OK)
     

class CreateLabTechnicianProfileView(CreateAPIView):

    permission_classes = (IsAuthenticatedLabTechnician, )
    serializer_class = LabTechnicianProfileSerializer


    def post(self, request,  format=None):

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            
            lab = serializer.save(user=self.request.user)
            lab.user.is_profile_completed = True
            lab.user.save()
     
            return Response({"message": "Lab Technician profile created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message": "An error occured, please try again."}, status=status.HTTP_400_BAD_REQUEST)
   
        
class GetLabDetailsView(APIView):
    
    permission_classes = (IsAuthenticatedLabTechnician, )
    serializer_class = LabTechnicianProfileSerializer

    def get(self, request, *args, **kwargs):
        try:
            lab = LabTechnician.objects.get(user=self.request.user)
        except LabTechnician.DoesNotExist:
            return Response({"message": "Lab not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(lab)
        return Response({"message": "Retrieved lab successfully", "data": serializer.data}, status=status.HTTP_200_OK)
     

class ListPatientsView(APIView):
    """
    An endpoint to list patients
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician,)
    serializer_class = PatientPrincipalSerializer

    def get(self, request, *args, **kwargs):
        patients = PatientPrincipal.objects.all()
        if patients:
            serializer = self.serializer_class(patients, many=True)
            return Response({"message": "Retrieved patients successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
    

class GetPatientView(APIView):
    """
    An endpoint to get specific patient
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician,)
    serializer_class = PrincipalSerializer

    def get(self, request, file_number, *args, **kwargs):

        try:
            patient = PatientPrincipal.objects.get(file_number=file_number)
        except PatientPrincipal.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        if patient:
            serializer = self.serializer_class(patient)
            return Response({"message": "Retrieved patient successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
    

class GetSpouseView(APIView):
    """
    An endpoint to get specific spouse
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician,)
    serializer_class = SpouseSingleSerializer

    def get(self, request, file_number, *args, **kwargs):

        try:
            spouse = Spouse.objects.get(file_number=file_number)
        except Spouse.DoesNotExist:
            return Response({"message": "No spouse found"}, status=status.HTTP_404_NOT_FOUND)
        if spouse:
            serializer = self.serializer_class(spouse)
            return Response({"message": "Retrieved spouse successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "No spouse found"}, status=status.HTTP_404_NOT_FOUND)
    

class GetChildView(APIView):
    """
    An endpoint to get specific child
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician,)
    serializer_class = ChildrenSingleSerializer

    def get(self, request, file_number, *args, **kwargs):

        try:
            child = Children.objects.get(file_number=file_number)
        except Children.DoesNotExist:
            return Response({"message": "No child found"}, status=status.HTTP_404_NOT_FOUND)
        if child:
            serializer = self.serializer_class(child)
            return Response({"message": "Retrieved child successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "No child available"}, status=status.HTTP_404_NOT_FOUND)
    

class SearchPrincipalPatientByNHISView(APIView):
    """
    An endpoint to search principal patient by NHIS number
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician | IsAuthenticatedNurse,)
    serializer_class = SearchPatientByNHISSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            nhis_number = serializer.validated_data["nhis_number"]

            try:
                patient = PatientPrincipal.objects.get(nhis_number=nhis_number)
            except PatientPrincipal.DoesNotExist:
                return Response({"message": "No Patient found"}, status=status.HTTP_404_NOT_FOUND)
            if patient:
                serializer = PatientPrincipalSerializer(patient)
                return Response({"message": "Retrieved patient successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Something went wrong. Please try again"}, status=status.HTTP_404_NOT_FOUND)
    

class SearchPrincipalPatientByFileNumberView(APIView):
    """
    An endpoint to search principal patient by file number
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician | IsAuthenticatedNurse,)
    serializer_class = SearchPatientByFileNumberSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            file_number = serializer.validated_data["file_number"]

            try:
                patient = PatientPrincipal.objects.get(file_number=file_number)
            except PatientPrincipal.DoesNotExist:
                return Response({"message": "No Patient found"}, status=status.HTTP_404_NOT_FOUND)
            if patient:
                serializer = PatientPrincipalSerializer(patient)
                return Response({"message": "Retrieved patient successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Something went wrong. Please try again"}, status=status.HTTP_404_NOT_FOUND)
    

class SearchChildByFileNumberView(APIView):
    """
    An endpoint to search child by file number
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician | IsAuthenticatedNurse,)
    serializer_class = SearchChildByFileNumberSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            file_number = serializer.validated_data["file_number"]

            try:
                child = Children.objects.get(file_number=file_number)
            except Children.DoesNotExist:
                return Response({"message": "No Child found"}, status=status.HTTP_404_NOT_FOUND)
            if child:
                serializer = ChildrenSerializer(child)
                return Response({"message": "Retrieved child successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "No child found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Something went wrong. Please try again"}, status=status.HTTP_404_NOT_FOUND)
    


class SearchSpouseByFileNumberView(APIView):
    """
    An endpoint to search spouse by file number
    """
    
    permission_classes = (IsAuthenticatedAccountsRecord | IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician | IsAuthenticatedNurse,)
    serializer_class = SearchSpouseByFileNumbererializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):

            file_number = serializer.validated_data["file_number"]

            try:
                spouse = Spouse.objects.get(file_number=file_number)
            except Spouse.DoesNotExist:
                return Response({"message": "No spouse found"}, status=status.HTTP_404_NOT_FOUND)
            if spouse:
                serializer = SpouseSerializer(spouse)
                return Response({"message": "Retrieved spouse successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "No spouse found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Something went wrong. Please try again"}, status=status.HTTP_404_NOT_FOUND)
    

class GetPrincipalContinuationSheetView(APIView):
    """
    An endpoint to get patient principal continuation sheet
    """
    
    permission_classes = (IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician | IsAuthenticatedNurse,)
    serializer_class = PrincipalContinuationSheetSerializer

    def get(self, request, slug, *args, **kwargs):

        try:
            patient = PatientPrincipal.objects.get(slug=slug)
        except PatientPrincipal.DoesNotExist:
            return Response({"message": "No patient found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            patient_sheet = PrincipalContinuationSheet.objects.get(patient_principal=patient)
        except PrincipalContinuationSheet.DoesNotExist:
            return Response({"message": "No patient continuation sheet found"}, status=status.HTTP_404_NOT_FOUND)
        if patient_sheet:
            serializer = self.serializer_class(patient_sheet)
            return Response({"message": "Retrieved patient continuation sheet successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "No patient available"}, status=status.HTTP_404_NOT_FOUND)
    


class GetSpouseContinuationSheetView(APIView):
    """
    An endpoint to get spouse continuation sheet
    """
    
    permission_classes = (IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician | IsAuthenticatedNurse,)
    serializer_class = SpouseContinuationSheetSerializer

    def get(self, request, slug, *args, **kwargs):

        try:
            spouse = Spouse.objects.get(slug=slug)
        except Spouse.DoesNotExist:
            return Response({"message": "No spouse found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            spouse_sheet = SpouseContinuationSheet.objects.get(spouse=spouse)
        except SpouseContinuationSheet.DoesNotExist:
            return Response({"message": "No spouse continuation sheet found"}, status=status.HTTP_404_NOT_FOUND)
        if spouse_sheet:
            serializer = self.serializer_class(spouse_sheet)
            return Response({"message": "Retrieved spouse continuation sheet successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "No spouse available"}, status=status.HTTP_404_NOT_FOUND)
    


class GetChildContinuationSheetView(APIView):
    """
    An endpoint to get child continuation sheet
    """
    
    permission_classes = (IsAuthenticatedDoctor | IsAuthenticatedPharmacist | IsAuthenticatedLabTechnician | IsAuthenticatedNurse,)
    serializer_class = ChildContinuationSheetSerializer

    def get(self, request, slug, *args, **kwargs):

        try:
            child = Children.objects.get(slug=slug)
        except Children.DoesNotExist:
            return Response({"message": "No child found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            child_sheet = ChildContinuationSheet.objects.get(child=child)
        except ChildContinuationSheet.DoesNotExist:
            return Response({"message": "No child continuation sheet found"}, status=status.HTTP_404_NOT_FOUND)
        if child_sheet:
            serializer = self.serializer_class(child_sheet)
            return Response({"message": "Retrieved child continuation sheet successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "No child available"}, status=status.HTTP_404_NOT_FOUND)
    

class UpdatePrincipalContinuationSheetView(APIView):
    """
    An endpoint to update principal continuation sheet
    """
    
    permission_classes = (IsAuthenticatedDoctor,)
    serializer_class = PrincipalContinuationSheetSerializer

    def post(self, request, slug, *args, **kwargs):

        user = self.request.user

        last_name = user.user_doctor.last_name

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):

            description = serializer.validated_data["description"]

            try:
                patient_sheet = PrincipalContinuationSheet.objects.get(slug=slug)
            except PrincipalContinuationSheet.DoesNotExist:
                return Response({"message": "No patient sheet found"}, status=status.HTTP_404_NOT_FOUND)
            if patient_sheet:

                datetime_object = patient_sheet.updated_at

                # Format the datetime object as required
                formatted_date = datetime_object.strftime("%d-%m-%Y")

                print(formatted_date)
                if patient_sheet.description:
                    patient_sheet.description += f"Dr {last_name} on {formatted_date}\n {description}\n\n"
                else:
                    patient_sheet.description = f"Dr {last_name} on {formatted_date}\n {description}\n\n"
                patient_sheet.save()
                serializer = self.serializer_class(patient_sheet)
                return Response({"message": "Updated patient continuation sheet successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "No patient available"}, status=status.HTTP_404_NOT_FOUND)
    

class UpdateSpouseContinuationSheetView(APIView):
    """
    An endpoint to update spouse continuation sheet
    """
    
    permission_classes = (IsAuthenticatedDoctor,)
    serializer_class = SpouseContinuationSheetSerializer

    def post(self, request, slug, *args, **kwargs):

        user = self.request.user

        last_name = user.user_doctor.last_name

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):

            description = serializer.validated_data["description"]

            try:
                spouse_sheet = SpouseContinuationSheet.objects.get(slug=slug)
            except SpouseContinuationSheet.DoesNotExist:
                return Response({"message": "No spouse sheet found"}, status=status.HTTP_404_NOT_FOUND)
            if spouse_sheet:

                datetime_object = spouse_sheet.updated_at
                # Format the datetime object as required
                formatted_date = datetime_object.strftime("%d-%m-%Y")

                if spouse_sheet.description:
                    spouse_sheet.description += f"Dr {last_name} on {formatted_date}\n {description}\n\n"
                else:
                    spouse_sheet.description = f"Dr {last_name} on {formatted_date}\n {description}\n\n"
                spouse_sheet.save()
                
                serializer = self.serializer_class(spouse_sheet)
                return Response({"message": "Updated spouse continuation sheet successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "No spouse available"}, status=status.HTTP_404_NOT_FOUND)
    

class UpdateChildContinuationSheetView(APIView):
    """
    An endpoint to update child continuation sheet
    """
    
    permission_classes = (IsAuthenticatedDoctor,)
    serializer_class = ChildContinuationSheetSerializer

    def post(self, request, slug, *args, **kwargs):

        user = self.request.user

        last_name = user.user_doctor.last_name

        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):

            description = serializer.validated_data["description"]

            try:
                child_sheet = ChildContinuationSheet.objects.get(slug=slug)
            except ChildContinuationSheet.DoesNotExist:
                return Response({"message": "No child sheet found"}, status=status.HTTP_404_NOT_FOUND)
            
            if child_sheet:

                datetime_object = child_sheet.updated_at
                # Format the datetime object as required
                formatted_date = datetime_object.strftime("%d-%m-%Y")

                if child_sheet.description:
                    child_sheet.description += f"Dr {last_name} on {formatted_date}\n {description}\n\n"
                else:
                    child_sheet.description = f"Dr {last_name} on {formatted_date}\n {description}\n\n"
                child_sheet.save()
                
                serializer = self.serializer_class(child_sheet)
                return Response({"message": "Updated child continuation sheet successfully", "data": serializer.data}, status=status.HTTP_200_OK)
            return Response({"message": "No child available"}, status=status.HTTP_404_NOT_FOUND)
    