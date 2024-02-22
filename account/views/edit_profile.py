from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.forms import ProfileForm


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'account/edit-profile.jinja', context={
        'form':form,
    })