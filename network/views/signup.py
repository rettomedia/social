from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from network.models import CustomUser
from network.forms import SignupForm  
from network.models import Regions

def signup(request):
    regions = Regions.objects.all()

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            region = form.cleaned_data['region']

            # Kullanıcıyı oluştur
            user = CustomUser.objects.create_user(username=username, password=password, email=email)

            # Kullanıcının region bilgisini güncelle
            user.region = region
            user.save()

            # Kullanıcıyı giriş yap
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Giriş yaptıktan sonra anasayfaya yönlendir
            else:
                # Giriş yapmadıysa hata durumu
                form.add_error(None, 'There was an error logging you in.')
        else:
            # Form geçerli değilse
            form.add_error(None, 'Please correct the errors below.')

    else:
        form = SignupForm()

    return render(request, 'network/signup.jinja', context={
        'form': form,
        'regions': regions,
    })
