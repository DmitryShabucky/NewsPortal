from django.contrib import admin
from .models import Post, Comment
from import_export.admin import ImportExportModelAdmin

class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
# Register your models here.
