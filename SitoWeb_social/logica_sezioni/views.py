from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from .mixins import StaffMixing
from django.views.generic.edit import CreateView, DeleteView
from .models import Sezione, Post, Discussione
from .forms import DiscussioneModelForm, PostModelForm
from django.http import HttpResponseRedirect, HttpResponseBadRequest #vedi aggiungiRisposta()
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
# Create your views here.

#con CreateView puoi creare sezioni fuori dal pannello di amministrazione


# senza CreateView avrei dovuto creare il modello, il suo form e poi la funzione view. come  F_di_Form_Modello_di_Commento nel progetto for_study
class CreaSezione(StaffMixing, CreateView):
    model = Sezione
    fields = "__all__"
    template_name = "crea_sezione.html"
    success_url = "/sezioni/"



class ListaSezioni(ListView):
    # si può specificare anche model, la differenza è che con "queryset" so possono dare comandi più dettagliati come filter
    queryset = Sezione.objects.all()
    template_name = 'lista_sezioni.html'
    context_object_name = "lista_sezioni"



def visualizzaSezione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    discussioni_sezione = Discussione.objects.filter(sezione_appartenenza=sezione).order_by("-data_creazione")
    context = {"sezione": sezione, "discussioni": discussioni_sezione}
    return render(request, "sezioni_singole.html", context)


@login_required
def creaDiscussione(request, pk):
    sezione = get_object_or_404(Sezione, pk=pk)
    if request.method == "POST":
        form = DiscussioneModelForm(request.POST)
        if form.is_valid():
            discussione = form.save(commit=False) #sospende la creazione dell'oggetto permettendo l'aggiunta di altri attributi
            discussione.sezione_appartenenza = sezione
            discussione.autore_discussione = request.user
            discussione.save()
            primo_post = Post.objects.create(
                discussione=discussione,
                autore_post=request.user,
                contenuto = form.cleaned_data["contenuto"])
            return HttpResponseRedirect(discussione.get_absolute_url())
    else:
        form = DiscussioneModelForm()

    context = {"form":form, "sezione": sezione}
    return render(request, "crea_discussione.html", context)



def visualizzaDiscussione(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)
    posts_discussione = Post.objects.filter(discussione=discussione)

    paginator = Paginator(posts_discussione, 10)
    page = request.GET.get("pagina")
    posts = paginator.get_page(page)

    form_risposta = PostModelForm()
    context =  {"discussione": discussione, 
                "posts_discussione": posts,
                "form_risposta": form_risposta}
    return render(request, "singola_discussione.html", context)

    

@login_required
def aggiungiRisposta(request, pk):
    discussione = get_object_or_404(Discussione, pk=pk)

    if request.method == "POST":
        form = PostModelForm(request.POST)
        if form.is_valid():
            form.save(commit= False)
            form.instance.discussione = discussione
            form.instance.autore_post = request.user
            form.save()
            url_discussione = reverse("visualizza_discussione", kwargs={"pk": pk})
            pagine_in_discussione = discussione.get_page_numbers()
            if pagine_in_discussione > 1:
                success_url = url_discussione + "?pagina=" + str(pagine_in_discussione)
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(url_discussione)

            
    else:
        return HttpResponseBadRequest()  # vogliamo solo aggiungere dei dati,
                                         # non abbiamo bisogno di GET


class Post_Delete(DeleteView):
    model = Post
    success_url = "/"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(autore_post_id=self.request.user.id)

        
