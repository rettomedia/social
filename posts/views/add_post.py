from django.shortcuts import redirect
from posts.models import Post
from django.utils.timezone import now
from datetime import timedelta
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@login_required
def add_post(request):
    if request.method == 'POST':
        author = request.user
        message = request.POST.get('message', '').strip()
        ip = get_client_ip(request)

        if not message:
            messages.error(request, "Message cannot be empty!")
            return redirect('index')

        last_post = Post.objects.filter(author=author).order_by('-writed_at').first()

        if last_post:
            if (now() - last_post.writed_at) < timedelta(seconds=30):
                messages.error(request, "You are posting too often, please wait!")
                return redirect('index')

            if last_post.message == message:
                messages.error(request, "You cannot re-share the same content!")
                return redirect('index')

        cache_key = f"post_limit_{ip}"
        post_count = cache.get(cache_key, 0)
        if post_count >= 5:
            messages.error(request, "You have shared too much, please wait!")
            
            author.delete()
            messages.error(request, "Your account has been deleted due to spamming!")
            return redirect('index')

        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi', 'mkv', 'webm']
        allowed_mime_types = ['image/jpeg', 'image/png', 'image/gif', 
                              'video/mp4', 'video/quicktime', 'video/x-msvideo', 
                              'video/x-matroska', 'video/webm']

        image = None
        if 'image' in request.FILES:
            image = request.FILES.get('image')
            extension = image.name.split('.')[-1].lower()
            mime_type = image.content_type

            if extension not in allowed_extensions or mime_type not in allowed_mime_types:
                messages.error(request, "You can only upload photos or videos!")
                return redirect('index')

        Post.objects.create(author=author, message=message, image=image)

        cache.set(cache_key, post_count + 1, timeout=60)

        messages.success(request, "Post shared successfully!")
        return redirect('index')

    return redirect('index')
