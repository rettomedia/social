# your_project/context_processors.py

from groups.models import Member

def user_groups(request):
    if request.user.is_authenticated:
        groups = Member.objects.filter(user=request.user).select_related('group')
        return {'my_groups': groups}
    return {'my_groups': []}
