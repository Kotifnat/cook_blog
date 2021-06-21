from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.core import validators
from django.utils.text import slugify
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


def get_upload_path(instance, filename):
    return f"articles/user_{instance.author.id}/{instance.title}/{filename}"


class Category(MPTTModel):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField(unique=True, help_text="Не трогайте это поле!")
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField("Название", max_length=100)
    slug = models.SlugField(unique=True, help_text="Не трогайте это поле!")

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User, to_field='username', related_name='posts', on_delete=models.CASCADE,
                               verbose_name='Автор', )
    title = models.CharField("Название", max_length=200,
                             validators=[validators.MinLengthValidator(4)],
                             )
    slug = models.SlugField(unique=True)
    text = models.TextField("Содержание")
    image = models.ImageField(upload_to=get_upload_path)
    category = models.ForeignKey(
        Category,
        to_field='name',
        related_name='post',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(Tag, related_name='post')
    created_at = models.DateTimeField("Время создания", auto_now_add=True)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        constraints = (
            models.UniqueConstraint(fields=['title', ], name='unique_title'),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={"slug": self.category.slug, "post_slug": self.slug})

    def get_recipes(self):
        return self.recipes.all()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Recipe(models.Model):
    name = models.CharField("Название рецепта", max_length=100)
    serves = models.CharField("Размер порции(кол-во персон)", max_length=50)
    prep_time = models.PositiveIntegerField("Время подготовки", default=0)
    cook_time = models.PositiveIntegerField("Время готовки", default=0)
    ingredients = RichTextField("Ингредиенты")
    directions = RichTextField("Процесс приготовления")
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
