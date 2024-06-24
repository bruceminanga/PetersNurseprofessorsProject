# decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def writer_required(function):
    def check_writer(user):
        return user.is_authenticated and hasattr(user, 'writer_profile') and user.writer_profile.is_writer

    def wrapper(request, *args, **kwargs):
        if not check_writer(request.user):
            messages.info(request, "You need to complete your writer profile to access this page.")
            return redirect(reverse('app1:become_writer'))
        return function(request, *args, **kwargs)

    return wrapper