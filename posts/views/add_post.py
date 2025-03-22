from django.shortcuts import redirect
from posts.models import Post
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages

@login_required
def add_post(request):
    if request.method == 'POST':
        author = request.user
        message = request.POST.get('message')

        if message != '':
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi', 'mkv', 'webm']
            allowed_mime_types = ['image/jpeg', 'image/png', 'image/gif', 
                                'video/mp4', 'video/quicktime', 'video/x-msvideo', 
                                'video/x-matroska', 'video/webm']

            if 'image' in request.FILES:
                image = request.FILES.get('image')
                extension = image.name.split('.')[-1].lower()
                mime_type = image.content_type

                if extension not in allowed_extensions or mime_type not in allowed_mime_types:
                    messages.error(request, "You can only upload photos or videos!")
                    return redirect('index')

                Post.objects.create(author=author, message=message, image=image)
            else:
                Post.objects.create(author=author, message=message)

            return redirect('index')
        else:
            return redirect('index')