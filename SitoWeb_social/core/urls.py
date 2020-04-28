from django.urls import path
from .views import Profilo_Utente, Lista_Utenti, funzione_ricerca, HomeView, visualizzaArticolo, CreaArticolo, Elimina_articolo


urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('articolo/<int:pk>', visualizzaArticolo, name='articolo_view'),
    path('articolo/<int:id>/elimina-articolo/<int:pk>', Elimina_articolo.as_view(), name='articolo_delete'),
    path('nuovo-articolo/', CreaArticolo.as_view(), name='crea_articolo'),
    path('user/<username>/', Profilo_Utente, name='profilo_utente'),
    path('users/', Lista_Utenti.as_view(), name='user_list'),
    path('cerca/', funzione_ricerca, name='funzione_cerca'),

]
