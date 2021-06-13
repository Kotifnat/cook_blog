from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin


class RecipeInline(admin.TabularInline):
    model = models.Recipe
    extra = 0


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", 'category', 'author', 'created_at']
    inlines = [
        RecipeInline,
    ]


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', ]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
