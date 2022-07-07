from django.urls import path
from .views import index, card, addCard, CardEditView, CardDeleteView

urlpatterns = [
    path('', index, name="cards_index"),
    path('card/<str:card_id>', card, name="card_consult"),
    path('add', addCard, name="card_add"),
    path('card/<str:pk>/edit', CardEditView.as_view(), name="card_edit"),
    path('card/<str:pk>/delete', CardDeleteView.as_view(), name="card_delete"),
]