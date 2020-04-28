from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import math
# Create your models here.


class Sezione(models.Model):
    nome_sezione = models.CharField(max_length=90)
    descrizione = models.CharField(max_length=90, blank=True, null=True)
    logo_sezione = models.ImageField(blank=True, null=True)
# "blank" indica campo vuoto possibile nel Form, "null" nel database
#la classe Sezione è padre della classe Discussione, le sezioni vengono create dagli amministratori, le discussioni dagli utenti

    def __str__(self):
        return self.nome_sezione

    class Meta:
        verbose_name = "Sezione"
        verbose_name_plural = "Sezioni"

    def get_absolute_url(self):
        return reverse("sezione_view", kwargs={"pk": self.pk})

    
    def ottieni_ultime_due_discussioni(self):
        return Discussione.objects.filter(sezione_appartenenza=self).order_by("-data_creazione")[:5]


    def ottieni_numero_post_in_sezione(self):
        return Post.objects.filter(discussione__sezione_appartenenza=self).count()

    #si richiama la funzione per un'istanza di sezione_appartenenza della classe discussione


class Discussione(models.Model):
    titolo = models.CharField(max_length=100)
    data_creazione = models.DateTimeField(auto_now_add=True) #la data di creazione della discussione verrà impostata nel momento della creazione dello stesso secondo l'orario attuale.
    autore_discussione = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussioni")
    sezione_appartenenza = models.ForeignKey(Sezione, on_delete=models.CASCADE) #senza related_name si richiamerà discussione_set

    def __str__(self):
        return self.titolo
    

    def get_page_numbers(self):
        posts_discussione = self.post_set.count()
        numero_pagine = math.ceil(posts_discussione / 10)
        return numero_pagine


    class Meta:
        verbose_name = "Discussione"
        verbose_name_plural = "Discussioni"


    def get_absolute_url(self):
        return reverse("visualizza_discussione", kwargs={"pk": self.pk})


class Post(models.Model):
    autore_post = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "posts")
    contenuto = models.TextField()
    data_creazione = models.DateTimeField(auto_now_add=True)
    discussione = models.ForeignKey(Discussione, on_delete=models.CASCADE)

    def __str__(self):
        return self.autore_post.username

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

