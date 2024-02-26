from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def help_center(request):
    return render(request, 'network/help-center.jinja')