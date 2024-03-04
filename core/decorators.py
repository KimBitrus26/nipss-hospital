from functools import wraps

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

def login_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            messages.info(request, "Login required. Please login first.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")

    return wrapper


def is_receptionist_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            messages.info(request, "Login required. Please login first.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        if not request.user.is_receptionist:
            messages.info(request, "Permission denied.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        else:
            return func(request, *args, **kwargs)
    return wrapper

def is_doctor_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            messages.info(request, "Login required. Please login first.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        if not request.user.is_doctor:
            messages.info(request, "Permission denied.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        else:
            return func(request, *args, **kwargs)
    return wrapper

def is_pharmcist_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            messages.info(request, "Login required. Please login first.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        if not request.user.is_phamacist:
            messages.info(request, "Permission denied.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        else:
            return func(request, *args, **kwargs)
    return wrapper

def is_lab_technician_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            messages.info(request, "Login required. Please login first.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        if not request.user.is_lab_technician:
            messages.info(request, "Permission denied.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        else:
            return func(request, *args, **kwargs)
    return wrapper

def is_patient_required(func):

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            messages.info(request, "Login required. Please login first.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        if not request.user.is_patient:
            messages.info(request, "Permission denied.")
            return HttpResponseRedirect(reverse('home') + f"?next={request.path}")
        else:
            return func(request, *args, **kwargs)
    return wrapper