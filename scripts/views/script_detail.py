from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from scripts.models import Script, ScriptComment


@login_required
def script_detail(request, username, slug):
    script = get_object_or_404(Script, slug=slug, author__username=username)
    script_comments = ScriptComment.objects.filter(script=script)
    
    if request.method == 'POST':
        if script.is_active:
            content = request.POST.get('content')
            if content:
                ScriptComment.objects.create(author=request.user,script=script,content=content)

                return redirect(request.META.get("HTTP_REFERER", "/"))

    return render(request, 'scripts/script-detail.jinja', {
        'script':script,
        'script_comments':script_comments,
    })
    