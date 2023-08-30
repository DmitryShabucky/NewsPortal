from django.contrib import admin
from .models import Post, Comment, Category, PostCategory
from import_export.admin import ImportExportModelAdmin


admin.site.register(Comment)
admin.site.register(Category)

class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...

admin.site.register(Post, PostAdmin)

# Register your models here.
