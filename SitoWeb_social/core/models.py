from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Articolo(models.Model):
    nome_articolo = models.CharField(max_length=90)
    descrizione_articolo = models.CharField(max_length=90, blank=True, null=True)
    immagine_articolo = models.ImageField(blank=True, null=True)
    contenuto = models.TextField()
    data_di_creazione = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_articolo
    

    class Meta:
        verbose_name = "Articolo"
        verbose_name_plural = "Articoli"

    def get_absolute_url(self):
        return reverse("articolo_view", kwargs={"pk": self.pk})
