from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


def get_upload_path(instance, filename):
    return f"articles/user_{instance.author.id}/{filename}"


class Category(MPTTModel):
    name = models.CharField("Название", max_length=100)
    slug = models.CharField("Slug", max_length=100)
    parent = TreeForeignKey(
        'self',
        related_name='children',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.CharField("Slug", max_length=100)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField("Название", max_length=200)
    text = models.TextField("Содержание")
    image = models.ImageField(upload_to=get_upload_path)
    category = models.ForeignKey(
        Category,
        related_name='post',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(Tag, related_name='post')
    created_at = models.DateTimeField("Время создания", auto_now_add=True)
    slug = models.CharField("Slug", max_length=200, default='')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug": self.category.slug, "post_slug": self.slug})

    def get_recipes(self):
        return self.recipes.all()


class Recipe(models.Model):
    name = models.CharField("Название рецепта", max_length=100)
    serves = models.CharField(max_length=50)
    prep_time = models.PositiveIntegerField("Время подготовки", default=0)
    cook_time = models.PositiveIntegerField("Время готовки", default=0)
    ingredients = models.TextField("Ингредиенты")
    direction = models.TextField("Процесс приготовления")
    post = models.ForeignKey(
        Post,
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.CharField(max_length=150)
    message = models.TextField(max_length=500)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
