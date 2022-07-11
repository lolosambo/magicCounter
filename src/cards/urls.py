from django.urls import path
from .views import index, card, addCard, CardEditView, CardDeleteView, \
     deck_index, deck, deckAddView, DeckEditView, DeckDeleteView, AssociateCardToDeckView, \
     removeCardFromDeckView

urlpatterns = [
    # CARD VIEWS
    path('', index, name="cards_index"),
    path('card/<str:card_id>', card, name="card_consult"),
    path('add', addCard, name="card_add"),
    path('card/<str:pk>/edit', CardEditView.as_view(), name="card_edit"),
    path('card/<str:pk>/delete', CardDeleteView.as_view(), name="card_delete"),

    # DECK VIEWS
    path('decks/', deck_index, name="decks_index"),
    path('deck/add', deckAddView, name="deck_add"),
    path('deck/<str:deck_id>', deck, name="deck_consult"),
    path('deck/<str:pk>/edit', DeckEditView.as_view(), name="deck_edit"),
    path('deck/<str:pk>/delete', DeckDeleteView.as_view(), name="deck_delete"),
    path('deck/associate/card/<str:pk>', AssociateCardToDeckView.as_view(), name="associate_card_to_deck"),
    path('deck/dissociate/deck/<str:deck_id>/card/<str:card_id>', removeCardFromDeckView, name="remove_card_from_deck"),
]