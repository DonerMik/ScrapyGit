from django.contrib import admin

from .models import *

admin.site.register(GitLink)
admin.site.register(Repositories)
admin.site.register(LastCommit)
admin.site.register(LastRelease)
