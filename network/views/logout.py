from django.contrib.auth import logout as logg
from django.shortcuts import redirect

def logout(request):
    logg(request)
    return redirect('index')