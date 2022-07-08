from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from cards.models import Card, Color, CardType
from mtgsdk import Card as MtgCard
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from cards.forms import CardForm


def index(request):
    cards = Card.objects.all()
    return render(request, "cards/index.html", {"cards": cards})


def card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    return render(request, 'cards/card_consult.html', {"card": card})

# Ajout d'une carte en mode FBV Function Based Views'
def addCard(request):
    if request.method == "POST":
        # request.POST = les données récupérées du formulaire (dictionnaire)
        form = CardForm(request.POST)
        if form.is_valid():
            mtgcard = MtgCard\
                .where(name=request.POST["name"])\
                .where(power=request.POST["power"]) \
                .where(toughness=request.POST["defense"])\
                .all()
            if not mtgcard:
                error = "La carte n'existe pas !"
                return render(request, 'cards/card_add.html', context={
                    "form": form,
                    "error": error
                })
            else:
                card = Card(name=mtgcard[0].name)
                illustration = mtgcard[0].image_url
                if illustration:
                    card.illustration = illustration
                else:
                    for i in range(1, len(mtgcard)):
                        illustration = mtgcard[i].image_url
                        if illustration:
                            card.illustration = illustration
                            break
                        else:
                            "Aucune illustration trouvée"
                card.save()

                # On associe les couleur de la carte Magic avec la carte en création
                for color in mtgcard[0].colors:
                    color_to_add = Color.objects.filter(color=color)
                    if not color_to_add:
                        new_color = Color(color=color)
                        new_color.save()
                        card.colors.add(new_color)
                    else:
                        card.colors.add(color_to_add[0])

                # On associe les types de la carte Magic avec la carte en création
                for type in mtgcard[0].subtypes:
                    type_to_add = CardType.objects.filter(name=type)
                    if not type_to_add:
                        new_type = CardType(name=type)
                        new_type.save()
                        card.types.add(new_type)
                    else:
                        card.types.add(type_to_add[0])

                card.power = mtgcard[0].power
                card.defense = mtgcard[0].toughness
                card.description = mtgcard[0].text
                card.save()

            # "commit=False", dans la fonction save() empêche la sauveagarde en BDD
            # Cela permet de traiter l'objet Card hydraté
            # form.save()
            # On redirige vers la même page pour éviter la ressoumission des données par erreur
            return HttpResponseRedirect(request.path)
    else:
        form = CardForm()

    return render(request, 'cards/card_add.html', context={"form": form})


# Edition d'une carte en mode CBV Class Based Views
class CardEditView(UpdateView):
    model = Card
    context_object_name = "card"
    form_class = CardForm
    template_name = "cards/card_add.html"


# Suppression d'une carte en mode CBV Class Based View
class CardDeleteView(DeleteView):
    model = Card
    context_object_name = "card"
    template_name = "cards/card_delete.html"
    success_url = reverse_lazy("cards_index")

