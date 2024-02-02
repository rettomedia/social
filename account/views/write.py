from django.shortcuts import render, redirect
from account.models import Post
from account.forms import Creation
from django.contrib.auth.decorators import login_required

@login_required
def write(request):
    if request.method == 'POST':
        form = Creation(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('profile')
    else:
        form = Creation()

    return render(request, 'account/write.jinja', context={
        'form':form,
    })