from django.contrib import admin
from .models import Post, Comment, Category, PostCategory, MyModel, CategoryName
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = CategoryName


class MyModelAdmin(TranslationAdmin):
    model = MyModel




def nullfy_rate(modeladmin, request, queryset):
    queryset.update(rate=0)
nullfy_rate.short_description = 'Обнулить рейтинг'

class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('create_date', 'author', 'title', 'rate')
    list_filter = ('author', 'create_date', 'rate')
    search_fields = ('author', 'category')
    actions = [nullfy_rate]

admin.site.register(Post, PostAdmin)
admin.site.register(MyModel)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(CategoryName)
