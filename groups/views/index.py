from django.shortcuts import render
from groups.models import Group, Member

def index(request):
    groups = Group.objects.all()
    user_groups = []
    
    if request.user.is_authenticated:
        user_groups = Member.objects.filter(user=request.user).values_list('group', flat=True)

    return render(request, 'groups/index.jinja', context={
        'groups':groups,
        'user_groups':user_groups
    })