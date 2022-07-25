from django import forms
from cards.models import Card, Deck, CardType, Playground
from magicCounter.form.widgets.HorizontalCheckboxSelectMultiple import HorizontalCheckboxSelectMultiple


class AddCardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        print(kwargs)
        super(AddCardForm, self).__init__(*args, **kwargs)
        if user:
            formatted_decks = []
            for deck in Deck.objects.filter(user=user):
                formatted_decks.append((deck.name, deck.name))
            self.fields["deck"] = forms.MultipleChoiceField(
                label="Deck(s)",
                choices=formatted_decks,
                widget=HorizontalCheckboxSelectMultiple()
            )

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
            "defense",
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


class EditCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditCardForm, self).__init__(*args, **kwargs)
        self.fields['types'].queryset = CardType.objects.all().order_by('name')
    class Meta:
        model = Card
        fields = [
            "name",
            "colors",
            "types",
            "power",
            "defense",
            "isFlying",
            "isLifeLink"
        ]
        labels = {
            "name": "Nom de la carte",
            "colors": "Couleur(s)",
            "types": "Type(s)",
            "power": "Attaque",
            "defense": "Défense",
            "isFlying": "Vol",
            "isLifeLink": "Lien de vie"
        }
        widgets = {
            "colors": HorizontalCheckboxSelectMultiple(),
            "types": HorizontalCheckboxSelectMultiple(),
        }



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
        exclude = ('user',)
        fields = [
            "deck",
        ]
        widgets = {
            "deck": HorizontalCheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AssociationForm, self).__init__(*args, **kwargs)
        if user == Deck.objects.filter(user=user)[0].user:
            self.fields['deck'].queryset = Deck.objects.filter(user=user)


class AddTokenForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddTokenForm, self).__init__(*args, **kwargs)
        if user:
            formatted_decks = []
            for deck in Deck.objects.filter(user=user):
                formatted_decks.append((deck.name, deck.name))
            self.fields["deck"] = forms.MultipleChoiceField(
                label="Deck(s)",
                choices=formatted_decks,
                widget=HorizontalCheckboxSelectMultiple()
            )
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

    isFlying = forms.BooleanField(
        required=False,
        initial=False,
        label="Vol"
    )

    isLifeLink = forms.BooleanField(
        required=False,
        initial=False,
        label="Lien de vie"
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

    formatted_types.sort()
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


class EditTokenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EditTokenForm, self).__init__(*args, **kwargs)
        self.fields['types'].queryset = CardType.objects.all().order_by('name')
    class Meta:
        model = Card
        fields = [
            "name",
            "colors",
            "types",
            "power",
            "defense",
            "isFlying",
            "isLifeLink"
        ]
        labels = {
            "name": "Nom du jeton",
            "colors": "Couleur(s)",
            "types": "Type(s)",
            "power": "Attaque",
            "defense": "Défense",
            "isFlying": "Vol",
            "isLifLink": "Lien de vie"
        }
        widgets = {
            "colors": HorizontalCheckboxSelectMultiple(),
            "types": HorizontalCheckboxSelectMultiple(),
        }


class CustomCounterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        deck = kwargs.pop('deck')
        super(CustomCounterForm, self).__init__(*args, **kwargs)
        if deck:
            formatted_types = []
            formatted_colors = []
            for card in Card.objects.filter(deck=deck):
                for type in card.types.all():
                    to_search = (type.name, type.name)
                    if to_search not in formatted_types:
                        formatted_types.append(to_search)
                for color in card.colors.all():
                    to_search = (color.color, color.color)
                    if to_search not in formatted_colors:
                        formatted_colors.append(to_search)
            formatted_types.sort()
            self.fields["types"] = forms.MultipleChoiceField(
                label="Type(s)",
                choices=formatted_types,
                widget=HorizontalCheckboxSelectMultiple()
            )
            formatted_colors.sort()
            self.fields["colors"] = forms.MultipleChoiceField(
                label="Couleur(s)",
                choices=formatted_colors,
                widget=HorizontalCheckboxSelectMultiple()
            )

    model = Playground

    power = forms.IntegerField(
        label="Attaque",
        required=True,
        initial=1
    )

    defense = forms.IntegerField(
        label="Defense",
        required=True,
        initial=1
    )

    forFlying = forms.BooleanField(
        label="Vol",
        required=False
    )
