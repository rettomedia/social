from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from network.forms import SignupForm  

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            if 'agree' in request.POST:
                agree = True
            else:
                agree = False

            if agree:
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect('index')
            else:
                form.add_error('agree', 'You must accept the terms and conditions')
    else:
        form = SignupForm()

    return render(request, 'network/signup.jinja', context={
        'form':form,
    })