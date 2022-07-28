from django.urls import path
from .views import index, card, addCard, CardEditView, CardDeleteView, \
    deck_index, deck, deckAddView, DeckEditView, DeckDeleteView, associateCardToDeckView, \
    removeCardFromDeckView, token_index, tokenAddView, token, TokenEditView, TokenDeleteView, associateTokenToDeckView, \
    removeTokenFromDeckView, playground, playground_game_starts, playground_add_card, playground_remove_creature, \
    playground_save, playground_save_for_all, playground_reset_all, playground_kill_game, playground_life_save, \
    playground_attack, playground_untap, playground_attack_all, playground_untap_all, playground_reorder_cards, \
    playground_kill_all, playground_flying_creature, playground_non_flying_creature, playground_flying_all, \
    playground_non_flying_all, playground_non_lifelink_all, playground_lifelink_all, playground_lifelink_creature, \
    playground_non_lifelink_creature, playground_turn_on, playground_turn_off

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
    path('deck/associate/card/<str:card_id>', associateCardToDeckView, name="associate_card_to_deck"),
    path('deck/dissociate/deck/<str:deck_id>/card/<str:card_id>', removeCardFromDeckView, name="remove_card_from_deck"),

    # TOKEN VIEWS
    path('tokens/', token_index, name="tokens_index"),
    path('token/add', tokenAddView, name="token_add"),
    path('token/<str:token_id>', token, name="token_consult"),
    path('token/<str:pk>/edit', TokenEditView.as_view(), name="token_edit"),
    path('token/<str:pk>/delete', TokenDeleteView.as_view(), name="token_delete"),
    path('deck/associate/token/<str:card_id>', associateTokenToDeckView, name="associate_token_to_deck"),
    path('deck/dissociate/deck/<str:deck_id>/token/<str:card_id>', removeTokenFromDeckView, name="remove_token_from_deck"),

    # PLAYGROUN VIEWS
    path('playground/', playground, name="playground"),

    path('playground/starts/<str:deck_id>', playground_game_starts, name="playground_game_starts"),
    path('playground/deck/<str:deck_id>/card/add/<str:card_id>/<str:number_of_cards>', playground_add_card, name="playground_add_card"),
    path('playground/deck/<str:deck_id>/delete/<str:index>', playground_remove_creature, name="playground_remove_creature"),
    path('playground/deck/<str:deck_id>/card/<str:card_index>/save/<str:button>/<str:new_value>', playground_save, name="playground_save"),
    path('playground/deck/<str:deck_id>/save/<str:button>', playground_save_for_all, name="playground_save_for_all"),
    path('playground/deck/<str:deck_id>/reset', playground_reset_all, name="playground_reset_all"),
    path('playground/deck/<str:deck_id>/kill_game', playground_kill_game, name="kill_game"),
    path('playground/deck/<str:deck_id>/life/<str:button>', playground_life_save, name="playground_life_save"),
    path('playground/deck/<str:deck_id>/card/<str:card_index>/attack', playground_attack, name="playground_attack"),
    path('playground/deck/<str:deck_id>/card/<str:card_index>/untap', playground_untap, name="playground_untap"),
    path('playground/deck/<str:deck_id>/attack/all', playground_attack_all, name="playground_attack_all"),
    path('playground/deck/<str:deck_id>/untap/all', playground_untap_all, name="playground_untap_all"),
    path('playground/deck/<str:deck_id>/kill/all', playground_kill_all, name="playground_kill_all"),
    path('playground/deck/<str:deck_id>/reorder/<str:slug>', playground_reorder_cards, name="playground_reorder_cards"),
    path('playground/deck/<str:deck_id>/become_flying/<str:index>', playground_flying_creature, name="playground_flying_creature"),
    path('playground/deck/<str:deck_id>/become_non_flying/<str:index>', playground_non_flying_creature, name="playground_non_flying_creature"),
    path('playground/deck/<str:deck_id>/flying/all', playground_flying_all, name="playground_flying_all"),
    path('playground/deck/<str:deck_id>/non-flying/all', playground_non_flying_all, name="playground_non_flying_all"),
    path('playground/deck/<str:deck_id>/become_lifelink/<str:index>', playground_lifelink_creature, name="playground_lifelink_creature"),
    path('playground/deck/<str:deck_id>/become_non_lifelink/<str:index>', playground_non_lifelink_creature, name="playground_non_lifelink_creature"),
    path('playground/deck/<str:deck_id>/lifelink/all', playground_lifelink_all, name="playground_lifelink_all"),
    path('playground/deck/<str:deck_id>/non-lifelink/all', playground_non_lifelink_all, name="playground_non_lifelink_all"),
    path('playground/deck/<str:deck_id>/turn-off', playground_turn_off, name="playground_turn_off"),
    path('playground/deck/<str:deck_id>/turn-on', playground_turn_on, name="playground_turn_on"),
]