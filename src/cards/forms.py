from django import forms
import json

from cards.models import Card

COLORS = (
    ("red", "Rouge"),
    ("blue", "Bleu"),
    ("green", "Vert"),
    ("black", "Noir"),
    ("white", "Blanc"),
    ("no_color", "Incolore"),
)


class AddCardForm(forms.Form):
    name = forms.CharField(
        label="Nom de la carte",
        required=True
    )
    colors = forms.MultipleChoiceField(
        label="Couleurs",
        required=True,
        choices=COLORS,
        widget=forms.CheckboxSelectMultiple()
    )

    # types = forms.ModelChoiceField(
    #     label="Types",
    #     required=True,
    #
    #     widget=forms.CheckboxSelectMultiple()
    # )

    description = forms.CharField(
        label="Description",
        required=False
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
