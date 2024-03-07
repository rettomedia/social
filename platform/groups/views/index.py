from django.shortcuts import render
from groups.models import Group

def index(request):
    groups = Group.objects.all()

    return render(request, 'groups/index.jinja', context={
        'groups':groups
    })