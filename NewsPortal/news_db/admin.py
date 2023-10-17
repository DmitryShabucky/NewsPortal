from django.contrib import admin
from .models import Post, Comment, Category, PostCategory
from import_export.admin import ImportExportModelAdmin


admin.site.register(Comment)
admin.site.register(Category)

def nullfy_rate(modeladmin, request, queryset):
    queryset.update(rate=0)
nullfy_rate.short_description = 'Обнулить рейтинг'
class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('create_date', 'author', 'title', 'rate')
    list_filter = ('author', 'create_date', 'rate')
    search_fields = ('author', 'category')
    actions = [nullfy_rate]

admin.site.register(Post, PostAdmin)

# Register your models here.
