from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, QueryDict
from cards.models import Card, Color, CardType, Deck
from mtgsdk import Card as MtgCard
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from cards.forms import AddCardForm, DeckForm, EditDeckForm, AssociationForm


def index(request):
    cards = Card.objects.all().order_by('name')
    return render(request, "cards/cards_index.html", {"cards": cards})


def card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    form = AssociationForm(request.POST)

    return render(request, 'cards/card_consult.html', {"card": card, "form": form})

# Ajout d'une carte en mode FBV Function Based Views'
def addCard(request):
    if request.method == "POST":
        # request.POST = les données récupérées du formulaire (dictionnaire)
        form = AddCardForm(request.POST)
        if form.is_valid():
            mtgcard = MtgCard\
                .where(name=request.POST["name"]) \
                .where(language=request.POST["language"]) \
                .where(power=request.POST["power"]) \
                .where(toughness=request.POST["defense"]) \
                .all()
            if not mtgcard:
                mtgcard = MtgCard \
                    .where(name=request.POST["name"]) \
                    .where(power=request.POST["power"]) \
                    .where(toughness=request.POST["defense"]) \
                    .all()
            if not mtgcard:
                error = "La carte n'existe pas !"
                return render(request, 'cards/card_add.html', context={
                    "form": form,
                    "error": error
                })
            else:
                card = Card(name=request.POST["name"])
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

                # On associe les decks avec la carte en création
                results = dict(QueryDict.lists(request.POST))
                for deck in results["deck"]:
                    deck_to_add = Deck.objects.filter(name=deck)
                    card.deck.add(deck_to_add[0])

                card.power = mtgcard[0].power
                card.defense = mtgcard[0].toughness
                card.description = mtgcard[0].text
                card.language = request.POST["language"]
                card.save()

            # "commit=False", dans la fonction save() empêche la sauveagarde en BDD
            # Cela permet de traiter l'objet Card hydraté
            # form.save()
            # On redirige vers la même page pour éviter la ressoumission des données par erreur
            return HttpResponseRedirect(request.path)
    else:
        form = AddCardForm()

    return render(request, 'cards/card_add.html', context={"form": form})


# Edition d'une carte en mode CBV Class Based Views
class CardEditView(UpdateView):
    model = Card
    context_object_name = "card"
    form_class = AddCardForm
    template_name = "cards/card_add.html"


# Suppression d'une carte en mode CBV Class Based View
class CardDeleteView(DeleteView):
    model = Card
    context_object_name = "card"
    template_name = "cards/card_delete.html"
    success_url = reverse_lazy("cards_index")


def deck_index(request):
    decks = Deck.objects.all().order_by('name')
    return render(request, "cards/decks_index.html", {"decks": decks})


def deck(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    return render(request, 'cards/deck_consult.html', {"deck": deck})


def deckAddView(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = Deck(name=request.POST["name"])
            deck.save()
            results = dict(QueryDict.lists(request.POST))
            # On associe les couleur le deck en création
            for color in results["colors"]:
                color_to_add = Color.objects.filter(color=color)
                if not color_to_add:
                    color = Color(color=color)
                    color.save()
                    deck.colors.add(color)
                else:
                    deck.colors.add(color_to_add[0])
            deck.save()

            return redirect('decks_index')
    else:
        form = DeckForm()

    return render(request, 'cards/deck_add.html', context={"form": form})


class DeckEditView(UpdateView):
    model = Deck
    context_object_name = "deck"
    form_class = EditDeckForm
    template_name = "cards/deck_add.html"


class DeckDeleteView(DeleteView):
    model = Deck
    context_object_name = "deck"
    template_name = "cards/deck_delete.html"
    success_url = reverse_lazy("decks_index")


class AssociateCardToDeckView(UpdateView):
    model = Card
    context_object_name = "card"
    form_class = AssociationForm
    template_name = "cards/card_edit.html"


def removeCardFromDeckView(request, deck_id, card_id):
    card = Card.objects.filter(pk=card_id)[0]
    deck = Deck.objects.filter(pk=deck_id)[0]
    card.deck.remove(deck)
    card.save()

    return redirect(deck)
