from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from logica_sezioni.models import Sezione, Discussione, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Articolo
from .mixins import StaffMixing
from django.http import HttpResponseRedirect
from django.urls import reverse



class CreaArticolo(StaffMixing, CreateView):
    model = Articolo
    fields = "__all__"
    template_name = "crea_articolo.html"
    success_url = "/"


class Elimina_articolo(DeleteView):
    model = Articolo
    success_url = "/"


class HomeView(ListView):
    # si può specificare anche model, la differenza è che con "queryset" so possono dare comandi più dettagliati come filter
    queryset = Articolo.objects.all()
    template_name = 'homepage.html'
    context_object_name = "articoli"




def visualizzaArticolo(request, pk):
    articolo = get_object_or_404(Articolo, pk=pk)
    context = {"articolo": articolo}
    return render(request, "singolo_articolo.html", context)




def Profilo_Utente(request, username):
    user = get_object_or_404(User, username=username)
    discussioni_utente = Discussione.objects.filter(autore_discussione=user).order_by("-pk")
    context = {"user": user, "discussioni_utente": discussioni_utente}
    return render(request, 'profilo_utente.html', context)


class Lista_Utenti(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users.html'


    #da notare che entramble le views prendono lo stesso modello User, questo sigifica che entrambe le views possono richiamare gli username


def funzione_ricerca(request):
    if "q" in request.GET:
        querystring =request.GET.get("q")
        print(querystring)
        if len(querystring) == 0:
            return redirect("/cerca/")
        
        articoli = Articolo.objects.filter(nome_articolo__icontains=querystring)
        discussioni = Discussione.objects.filter(titolo__icontains=querystring)
        posts = Post.objects.filter(contenuto__icontains=querystring)
        users = User.objects.filter(username__icontains=querystring)

        context = {"discussioni": discussioni, "posts": posts, "users": users, "articoli": articoli}
        return render(request, "cerca.html", context)
    
    else:
        return render(request, "cerca.html")


