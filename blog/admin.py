from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin


class RecipeInline(admin.TabularInline):
    model = models.Recipe
    extra = 0


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    pass


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", 'category', 'author', 'created_at']
    inlines = [
        RecipeInline,
    ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', ]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
