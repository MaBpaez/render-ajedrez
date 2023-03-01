from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class ClubAjedrez(models.Model):
    name = models.CharField('nombre', max_length=100)
    address = models.CharField('sede social', max_length=100)
    play_place = models.CharField('lugar de juego', max_length=100)
    population = models.CharField('población', max_length=100, blank=True)
    zip_code = models.CharField('Código Postal', max_length=10, blank=True)
    president = models.CharField('presidente/a', max_length=100)
    website = models.CharField('sitio web', max_length=100, blank=True)
    social_network = models.CharField('red social', max_length=100, blank=True)
    phone = models.CharField('teléfono', max_length=15, blank=True)
    contact = models.EmailField('contacto', max_length=100)
    body = RichTextUploadingField('contenido', blank=True)

    publish = models.DateTimeField('fecha de publicación', default=timezone.now)
    created = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated = models.DateTimeField('fecha de edición', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'clubes de ajedrez'


    def __str__(self):
        return self.name

