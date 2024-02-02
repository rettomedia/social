from django.shortcuts import render, get_object_or_404, redirect
from account.models import Post
from account.forms import Creation
from django.contrib.auth.decorators import login_required

@login_required
def edit_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = Creation(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = Creation(instance=post)

    return render(request, 'account/edit-post.jinja', context={
        'form':form,
    })