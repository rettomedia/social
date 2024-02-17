from django.shortcuts import render, redirect
from network.models import News
from posts.models import Post

def index(request):
    if request.user.is_authenticated:
        news = News.objects.all()
        posts = Post.objects.all()

        return render(request, 'network/feed.jinja', context={
            'news':news,
            'posts':posts,
        })
    else:
        return redirect('login')