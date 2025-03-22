from django.shortcuts import render, redirect
from network.models import News
from posts.models import Post
from django.db.models import Q
from django.core.paginator import Paginator


def index(request):
    if request.user.is_authenticated:
        news = News.objects.all()
        posts = Post.objects.all().order_by('-id')

        # search
        search = request.GET.get('search')
        page = request.GET.get('page')
        if search:
            posts = posts.filter(
                Q(message__contains=search) |
                Q(author__username__contains=search)
            ).distinct()

        paginator = Paginator(posts, 35)

        return render(request, 'network/feed.jinja', context={
            'news':news,
            'posts':paginator.get_page(page),
        })
    else:
        return redirect('login')