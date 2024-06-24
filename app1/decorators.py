# decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages

def writer_required(function):
    def check_writer(user):
        return user.is_authenticated and hasattr(user, 'writer_profile') and user.writer_profile.is_writer

    decorated_view = user_passes_test(check_writer, login_url='become_writer')(function)
    
    def wrapper(request, *args, **kwargs):
        if not check_writer(request.user):
            messages.info(request, "You need to complete your writer profile to access this page.")
            return redirect('become_writer')
        return decorated_view(request, *args, **kwargs)
    
    return wrapper