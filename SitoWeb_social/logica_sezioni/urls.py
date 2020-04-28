from django.urls import path
from .views import ListaSezioni, CreaSezione, visualizzaSezione, creaDiscussione, visualizzaDiscussione, aggiungiRisposta, Post_Delete


urlpatterns = [
    path('', ListaSezioni.as_view(), name='lista_sezioni'),
    path('nuova-sezione/', CreaSezione.as_view(), name='crea_sezione'),
    path('sezione/<int:pk>', visualizzaSezione, name='sezione_view'),
    path('sezione/<int:pk>/crea-discussione/', creaDiscussione, name='crea_discussione'),
    path('discussione/<int:pk>', visualizzaDiscussione, name='visualizza_discussione'),
    path('discussione/<int:pk>/rispondi/', aggiungiRisposta, name='rispondi_a_discussione'),
    path('discussione/<int:id>/elimina-post/<int:pk>/', Post_Delete.as_view(), name='cancella_post'),

]
