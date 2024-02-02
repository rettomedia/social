from django.shortcuts import render, get_object_or_404, redirect
from core.models import CustomUser
from account.forms import EditProfile
from django.contrib.auth.decorators import login_required

@login_required
def settings(request):
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfile(instance=request.user)

    return render(request, 'account/edit.jinja', context={
        'form':form,
    })