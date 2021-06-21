from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin


class RecipeInline(admin.StackedInline):
    model = models.Recipe
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(MPTTModelAdmin):
    readonly_fields = ('slug',)
    pass


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    pass


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ["title", 'category', 'author', 'created_at']
    inlines = [
        RecipeInline,
    ]
    save_on_top = True


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', ]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
