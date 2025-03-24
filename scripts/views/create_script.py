from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from scripts.forms import ScriptForm

@login_required
def create_script(request):
    if request.method == "POST":
        form = ScriptForm(request.POST)
        if form.is_valid():
            script = form.save(commit=False)
            script.author = request.user 
            script.save()
            return redirect('scripts') 
    else:
        form = ScriptForm()

    return render(request, "scripts/create_script.jinja", {"form": form})