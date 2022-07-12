from django.contrib import admin
from cards.models import Card
from cards.models import Deck
from cards.models import CardType
from cards.models import Color


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # Ajoute une colonne à l'admin'
    list_display = ("name", "power", "defense")
    # Rend éditable les entrées sélectionnées
    list_editable = ("power", "defense")
    # Barre de recherche sur les éléments sélectionnés
    search_fields = ("name", "power", "defense")
    # Filtre permettant de sélectionner plusieurs options dans une relation ManyToMany
    filter_horizontal = ("types",)
    # Pagination
    list_per_page = 25


@admin.register(CardType)
class CardTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("color", "element")