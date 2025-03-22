from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.forms import ProfileForm
from PIL import Image


def make_square(image_path):
    image = Image.open(image_path)
    width, height = image.size
    
    if width != height:
        new_width = min(width, height)
        new_height = new_width
        top_left_x = (width - new_width) // 2
        top_left_y = (height - new_height) // 2
        bottom_right_x = top_left_x + new_width
        bottom_right_y = top_left_y + new_height
        image = image.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    
    image.save(image_path)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            profile = form.save()
            if profile.avatar:
                make_square(profile.avatar.path)
            return redirect('settings')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'account/edit-profile.jinja', context={
        'form':form,
    })