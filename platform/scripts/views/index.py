from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from scripts.models import Script


@login_required
def index(request):
    scripts = Script.objects.all()
    return render(request, 'scripts/index.jinja', context={
        'scripts': scripts,
    })