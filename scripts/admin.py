from django.contrib import admin
from scripts.models import Script, ScriptCategory, ScriptComment

# Register your models here.
admin.site.register(Script)
admin.site.register(ScriptCategory)
admin.site.register(ScriptComment)