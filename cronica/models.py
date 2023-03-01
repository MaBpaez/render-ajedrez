from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from core.models import Torneo
from ckeditor_uploader.fields import RichTextUploadingField


class Cronica(models.Model):
    title = models.CharField('titulo', max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User, verbose_name='autor', on_delete=models.CASCADE, related_name='get_cronicas'
    )
    torneo = models.OneToOneField(Torneo, on_delete=models.CASCADE)

    image = models.ImageField('imagen', upload_to='cronicas', blank=True)
    body = RichTextUploadingField('contenido')

    publish = models.DateTimeField('fecha de publicación', default=timezone.now)
    created = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated = models.DateTimeField('fecha de modificación', auto_now=True)

    class Meta:
        ordering = ['-publish']
        verbose_name_plural = 'crónicas'

    def __str__(self):
        return self.title
