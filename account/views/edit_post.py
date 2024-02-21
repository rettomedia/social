from django.shortcuts import render, get_object_or_404, redirect
from account.forms import PostForm
from posts.models import Post

def edit_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PostForm(instance=post)
    return render(request, 'account/edit-post.jinja', context={
        'form':form
    })