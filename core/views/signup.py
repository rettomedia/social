from django.shortcuts import render, redirect
from core.forms import SignupForm
from django.contrib.auth import authenticate, login

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']

                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect('index')
        else:
            form = SignupForm()

        return render(request, 'core/signup.jinja', context={
            'form':form,
        })