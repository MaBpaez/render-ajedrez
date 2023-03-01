from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class Circular(models.Model):
    title = models.CharField('título circular', max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User,
        verbose_name='autor',
        on_delete=models.CASCADE,
        related_name='get_circulares',
    )

    file_pdf = models.FileField('circulares', upload_to='pdf/%Y/%m/%d/', storage=RawMediaCloudinaryStorage())
    publish = models.DateTimeField('fecha de la circular', default=timezone.now)
    created = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated = models.DateTimeField('fecha de edición', auto_now=True)
    search_date = models.CharField(blank=True, max_length=200)  # desde cero no hara falta blank=True

    class Meta:
        ordering = ['-publish']
        verbose_name_plural = 'circulares'

    def save(self, *args, **kwargs):
        self.search_date = self.publish.strftime("%d %B %Y")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
