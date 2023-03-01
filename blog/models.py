import requests
import json
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from taggit.managers import TaggableManager

url = "https://onesignal.com/api/v1/notifications"


# Modelo CATEGORIA
class Category(models.Model):
    name = models.CharField("nombre", max_length=100)
    created = models.DateTimeField("fecha de creación", auto_now_add=True)
    updated = models.DateTimeField("fecha de edición", auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.name


# Manager Personalizado
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")


# Modelo POST
class Post(models.Model):
    STATUS_CHOICES = (("draft", "Borrador"), ("published", "Publicado"))

    title = models.CharField("titulo", max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User,
        verbose_name="autor",
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )

    image = models.ImageField("imagen", upload_to="blog", blank=True, null=True)
    body = RichTextUploadingField("contenido")
    categories = models.ManyToManyField(
        Category,
        verbose_name="categorías",
        related_name="get_posts",
        blank=True,
    )

    publish = models.DateTimeField("fecha de publicación", default=timezone.now)
    created = models.DateTimeField("fecha de creación", auto_now_add=True)
    updated = models.DateTimeField("fecha de modificación", auto_now=True)
    search_date = models.CharField(
        blank=True, max_length=200
    )  # desde cero no hara falta blank=True
    status = models.CharField(
        "estado", max_length=10, choices=STATUS_CHOICES, default="draft"
    )

    objects = models.Manager()  # el manager por defecto
    published = PublishedManager()  # nuestro manager personalizado.
    tags = TaggableManager()

    class Meta:
        ordering = ["-publish"]

    def get_absolute_url(self):
        return reverse(
            "blog:post-detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    def save(self, *args, **kwargs):
        self.search_date = self.publish.strftime("%d %B %Y")
        super().save(*args, **kwargs)
        payload = {
            "app_id": "a916b202-a622-4aa2-8556-b4dcf3bc60ef",
            # "included_segments": ["Subscribed Users"],
            "excluded_segments": ["Inactive Users"],
            "filters": [
                # segment e include_segments son ignorados y por tanto no se ponen cuando se
                # utiliza filters.
                {
                    "field": "tag",
                    "key": "articulos_del_blog",
                    "relation": "=",
                    "value": "1",
                }
            ],
            # "delayed_option": "last-active",
            "delayed_option": "immediate",
            "headings": {
                "en": "The notification's title.",
                "es": self.title,
            },
            "contents": {
                "en": "New Article in our blog.",
                "es": "Nuevo artículo creado, visita nuestro blog.",
            },
            "web_url": f"http://127.0.0.1:8000{self.get_absolute_url()}",
            "chrome_web_image": self.image.url,
            "web_buttons": [
                {
                    "id": "read-more-button",
                    "text": "Leer artículo",
                    "icon": "http://i.imgur.com/MIxJp1L.png",
                    "url": f"http://127.0.0.1:8000{self.get_absolute_url()}",
                },
            ],
            "name": "Probando api",
        }
        headers = {
            "accept": "application/json",
            "Authorization": "Basic ODdiMWIyNGItYTJkNC00ZDRhLTk3YjMtNjVhODJmOWJkZjdl",
            "content-type": "application/json",
        }

        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(response.text)
        print(response.status_code)
        # super().save(*args, **kwargs)

    def __str__(self):
        return self.title
