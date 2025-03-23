from django.shortcuts import render, redirect
from network.models import News
from posts.models import Post, Like
from django.db.models import Count, Q
from django.core.paginator import Paginator

def index(request):
    if request.user.is_authenticated:
        news = News.objects.all()
        posts = Post.objects.annotate(like_count=Count('likes')).order_by('-id')

        # Arama işlemi
        search = request.GET.get('search')
        page = request.GET.get('page')
        if search:
            posts = posts.filter(
                Q(message__icontains=search) |
                Q(author__username__icontains=search)
            ).distinct()

        # Sayfalama işlemi
        paginator = Paginator(posts, 35)
        paginated_posts = paginator.get_page(page)

        # Kullanıcının beğendiği gönderileri belirleme
        user_liked_posts = set(
            Like.objects.filter(from_user=request.user).values_list('post_id', flat=True)
        )

        return render(request, 'network/feed.jinja', {
            'news': news,
            'posts': paginated_posts,
            'user_liked_posts': user_liked_posts,  # Kullanıcının beğendiği gönderiler
        })
    
    else:
        return redirect('login')
