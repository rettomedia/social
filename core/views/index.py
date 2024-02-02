from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from account.models import Post

def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        search = request.GET.get('search')
        page = request.GET.get('posts')
        
        if search:
            posts = posts.filter(
                Q(title__contains=search) |
                Q(content__contains=search) |
                Q(author__username__contains=search)
            ).distinct()
        
        paginator = Paginator(posts, 10)
        return render(request, 'core/network.jinja', context={
            'posts':paginator.get_page(page)
        })
    else:
        return render(request, 'core/index.jinja')