# from typing_extensions import Required
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class Torneo(models.Model):
    title = models.CharField('título', max_length=200)
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # file will be saved to MEDIA_ROOT/pdf/2015/01/30
    file_pdf = models.FileField('bases', upload_to='pdf/%Y/%m/%d/', storage=RawMediaCloudinaryStorage())
    body = RichTextUploadingField('contenido', blank=True)
    image = models.ImageField('imagen', upload_to='torneos', blank=True)
    quantity = models.PositiveIntegerField('aforo', default=0)

    start = models.DateTimeField('inicio', default=timezone.now)
    finish = models.DateTimeField('final', default=timezone.now)
    end_registration = models.DateTimeField(
        'fin de inscripción', default=timezone.now, blank=True, null=True
    )  # tiene que ser campo obligatorio

    publish = models.DateTimeField('fecha de publicación', default=timezone.now)
    created = models.DateTimeField('fecha de creación', auto_now_add=True)
    updated = models.DateTimeField('fecha de edición', auto_now=True)

    location = models.CharField('localidad', max_length=200)
    province = models.CharField('provincia', max_length=200)
    registre = RichTextUploadingField('registrarse', blank=True)
    inscribed = models.URLField('inscritos', blank=True)

    class Meta:
        ordering = ['-start']
        verbose_name_plural = 'torneos'

    def get_absolute_url(self):
        return reverse(
            "torneo:torneo-detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )

    def __str__(self):
        return self.title


class TournamentRegistration(models.Model):
    name = models.CharField('nombre', max_length=50)
    surnames = models.CharField('apellidos', max_length=100)
    mail = models.EmailField('correo electrónico', max_length=100)
    population = models.CharField('población', max_length=100)
    zip_code = models.CharField('Código Postal', max_length=10)
    date_birth = models.DateTimeField('fecha de nacimiento')
    phone = models.CharField('teléfono', max_length=15)
    status = models.CharField('estado', max_length=100)
    privacy_policy = models.BooleanField('Aceptar política privacidad', default=False)
    tournament_title = models.CharField('nombre del torneo', max_length=200)
    tournament = models.ForeignKey(
        Torneo, on_delete=models.CASCADE, verbose_name='torneo', related_name='registros'
    )

    paid = models.BooleanField('pagado', default=False)

    class Meta:
        # unique_together = ['name', 'surnames', 'mail', 'tournament']
        constraints = [
            UniqueConstraint(
                fields=['name', 'surnames', 'mail', 'tournament_title'],
                name='unique_tournamentregistration',
            )
        ]
        verbose_name_plural = 'registros'
        ordering = ['-surnames']
