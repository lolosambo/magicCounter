from django import forms
import json
from cards.models import Card, Deck, CardType
from magicCounter.form.widgets.HorizontalCheckboxSelectMultiple import HorizontalCheckboxSelectMultiple


class AddCardForm(forms.Form):
    name = forms.CharField(
        label="Nom de la carte",
        required=True
    )

    power = forms.CharField(
        max_length=4,
        label="Attaque",
        required=True
    )

    defense = forms.CharField(
        max_length=4,
        label="Défense",
        required=True
    )

    LANGUAGES = [
        ("english", "Anglais"),
        ("french", "Français"),
    ]
    language = forms.ChoiceField(
        label="Langue",
        choices=LANGUAGES,
        required=True
    )

    decks = Deck.objects.all().order_by("name")
    formatted_decks = []

    for deck in decks:
        formatted_decks.append((deck.name, deck.name))

    deck = forms.MultipleChoiceField(
        label="Deck(s)",
        choices=formatted_decks,
        widget=HorizontalCheckboxSelectMultiple()
    )

    # Validation des éléments de formulaire après soumission.
    # ATTENTION au nommage "clean_" + "NomDuChamp" obligatoire
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if "$" in name:
            raise forms.ValidationError('Le nom ne peut pas contenir de "$"')
        return name


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            "name",
            "power",
            "defense"
        ]
        labels = {
            "name": "Nom de la carte",
            "power": "Attaque",
            "defense": "Défense"

        }
        # widgets = {
        #     "colors": forms.CheckboxSelectMultiple(choices=COLORS),
        #     "types": forms.CheckboxSelectMultiple()
        # }

    # Validation des éléments de formulaire après soumission.
    # ATTENTION au nommage "clean_" + "NomDuChamp" obligatoire
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if "$" in name:
            raise forms.ValidationError('Le nom ne peut pas contenir de "$"')
        return name


class DeckForm(forms.Form):
    COLORS = [
        ("White", "Blanc"),
        ("Black", "Noir"),
        ("Red", "Rouge"),
        ("Green", "Vert"),
        ("Blue", "Bleu"),
        ("Uncolored", "Incolore"),
    ]
    model = Deck
    name = forms.CharField(
        label="Nom du deck",
        required=True
    )

    colors = forms.MultipleChoiceField(
        label="Couleur(s)",
        required=True,
        choices=COLORS,
        widget=HorizontalCheckboxSelectMultiple()
    )

    # Validation des éléments de formulaire après soumission.
    # ATTENTION au nommage "clean_" + "NomDuChamp" obligatoire
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if "$" in name:
            raise forms.ValidationError('Le nom ne peut pas contenir de "$"')
        return name


class EditDeckForm(forms.ModelForm):
    class Meta:
        model = Deck
        fields = [
            "name",
            "colors",
        ]
        labels = {
            "name": "Nom du deck",
            "colors": "Couleurs",

        }
        widgets = {
            "colors": HorizontalCheckboxSelectMultiple(),
        }

    # Validation des éléments de formulaire après soumission.
    # ATTENTION au nommage "clean_" + "NomDuChamp" obligatoire
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if "$" in name:
            raise forms.ValidationError('Le nom ne peut pas contenir de "$"')
        return name


class AssociationForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            "deck",
        ]
        widgets = {
            "deck": HorizontalCheckboxSelectMultiple(),
        }


class AddTokenForm(forms.Form):
    name = forms.CharField(
        label="Nom de la carte",
        required=True
    )

    power = forms.CharField(
        max_length=4,
        label="Attaque",
        required=True
    )

    defense = forms.CharField(
        max_length=4,
        label="Défense",
        required=True
    )

    LANGUAGES = [
        ("english", "Anglais"),
        ("french", "Français"),
    ]
    language = forms.ChoiceField(
        label="Langue",
        choices=LANGUAGES,
        required=True
    )

    decks = Deck.objects.all().order_by("name")
    formatted_decks = []

    for deck in decks:
        formatted_decks.append((deck.name, deck.name))

    deck = forms.MultipleChoiceField(
        label="Deck(s)",
        choices=formatted_decks,
        widget=HorizontalCheckboxSelectMultiple()
    )

    COLORS = [
        ("White", "Blanc"),
        ("Black", "Noir"),
        ("Red", "Rouge"),
        ("Green", "Vert"),
        ("Blue", "Bleu"),
        ("Uncolored", "Incolore"),
    ]

    colors = forms.MultipleChoiceField(
        label="Couleur(s)",
        required=True,
        choices=COLORS,
        widget=HorizontalCheckboxSelectMultiple()
    )

    types = CardType.objects.all().order_by("name")
    formatted_types = []

    for type in types:
        formatted_types.append((type.name, type.name))

    types = forms.MultipleChoiceField(
        label="Type(s)",
        choices=formatted_types,
        required=False,
        widget=HorizontalCheckboxSelectMultiple()
    )

    add_type = forms.CharField(
        label="Ajouter des types (séparés par une virgule)",
        required=False
    )

    # Validation des éléments de formulaire après soumission.
    # ATTENTION au nommage "clean_" + "NomDuChamp" obligatoire
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if "$" in name:
            raise forms.ValidationError('Le nom ne peut pas contenir de "$"')
        return name
