from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Modelo para las PAGINAS SECUNDARIAS
# ===================================
class Page(models.Model):
    title = models.CharField('titulo', max_length=100)
    content = RichTextUploadingField('contenido')
    created = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated = models.DateTimeField('fecha de edición', auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name = 'página'
        verbose_name_plural = 'páginas'

    def __str__(self):
        return self.title
