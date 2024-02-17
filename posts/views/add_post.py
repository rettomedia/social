from django.shortcuts import redirect
from posts.models import Post
from django.contrib.auth.decorators import login_required


@login_required
def add_post(request):
    if request.method == 'POST':
        author = request.user
        message = request.POST.get('message')

        if 'image' in request.FILES:
            image = request.FILES.get('image')
            Post.objects.create(author=author, message=message, image=image)
        else:
            Post.objects.create(author=author, message=message)

        return redirect('index')