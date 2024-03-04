from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedDoctor(BasePermission):

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_authenticated and request.user.is_doctor)


class IsAuthenticatedPharmacist(BasePermission):

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_authenticated and request.user.is_pharmacist)


class IsAuthenticatedLabTechnician(BasePermission):

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_authenticated and request.user.is_lab_technician)
    
class IsAuthenticatedAccountsRecord(BasePermission):

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_authenticated and request.user.is_account)
      
class IsAuthenticatedNurse(BasePermission):

    def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_authenticated and request.user.is_nurse)
      