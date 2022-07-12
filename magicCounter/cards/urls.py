from django.urls import path
from .views import index, card, addCard, CardEditView, CardDeleteView, \
     deck_index, deck, deckAddView, DeckEditView, DeckDeleteView, AssociateCardToDeckView, \
     removeCardFromDeckView, token_index, tokenAddView, token, TokenEditView, TokenDeleteView, AssociateTokenToDeckView,\
     removeTokenFromDeckView

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

    # TOKEN VIEWS
    path('tokens/', token_index, name="tokens_index"),
    path('token/add', tokenAddView, name="token_add"),
    path('token/<str:token_id>', token, name="token_consult"),
    path('token/<str:pk>/edit', TokenEditView.as_view(), name="token_edit"),
    path('token/<str:pk>/delete', TokenDeleteView.as_view(), name="token_delete"),
    path('deck/associate/token/<str:pk>', AssociateTokenToDeckView.as_view(), name="associate_token_to_deck"),
    path('deck/dissociate/deck/<str:deck_id>/token/<str:card_id>', removeTokenFromDeckView, name="remove_token_from_deck"),
]