from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from cards.models import Card, Color, CardType, Deck, Playground
from mtgsdk import Card as MtgCard
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from cards.forms import AddCardForm, DeckForm, EditDeckForm, AssociationForm, AddTokenForm, EditTokenForm


def index(request):
    cards = Card.objects.all().order_by('name')
    filteredCards = []
    for card in cards:
        for deck in card.deck.all():
            if deck.user == request.user and card not in filteredCards:
                filteredCards.append(card)
    return render(request, "cards/cards_index.html", {"cards": filteredCards})


def card(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    form = AssociationForm(user=request.user)

    return render(request, 'cards/card_consult.html', {"card": card, "form": form})


# Ajout d'une carte en mode FBV Function Based Views'
def addCard(request):
    if request.method == "POST":
        # request.POST = les données récupérées du formulaire (dictionnaire)
        form = AddCardForm(request.POST, user=request.user)
        if form.is_valid():
            print("jhferuih fguirhe uighreuih guirehg uierui gherui")
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
                if "Flying" in mtgcard[0].text or "Volant" in mtgcard[0].text:
                    card.isFlying = True
                card.save()

            # "commit=False", dans la fonction save() empêche la sauveagarde en BDD
            # Cela permet de traiter l'objet Card hydraté
            # form.save()
            # On redirige vers la même page pour éviter la ressoumission des données par erreur
            return HttpResponseRedirect(request.path)
    else:
        form = AddCardForm(user=request.user)

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
    decks = Deck.objects.filter(user=request.user).order_by('name')
    return render(request, "cards/decks_index.html", {"decks": decks})


def deck(request, deck_id):
    deck = get_object_or_404(Deck, pk=deck_id)
    return render(request, 'cards/deck_consult.html', {"deck": deck})


def deckAddView(request):
    if request.method == "POST":
        form = DeckForm(request.POST)
        if form.is_valid():
            deck = Deck(name=request.POST["name"], user=request.user)
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


def associateCardToDeckView(request, card_id):
    card = Card.objects.filter(pk=card_id)[0]
    if request.method == "POST":
        form = AssociationForm(request.POST, user=request.user)
        if form.is_valid():
            for deck in form.cleaned_data["deck"]:
                deck_to_associate = Deck.objects.filter(name=deck)[0]
                card.deck.add(deck_to_associate)
            card.save()
            return render(request, "cards/card_consult.html", context={"card": card, "form": form})
    else:
        form = AssociationForm(user=request.user)

    return render(request, "cards/card_consult.html", context={"card": card, "form": form})


def removeCardFromDeckView(request, deck_id, card_id):
    card = Card.objects.filter(pk=card_id)[0]
    deck = Deck.objects.filter(pk=deck_id)[0]
    card.deck.remove(deck)
    card.save()

    return redirect(deck)


def token_index(request):
    tokens = Card.objects.all().filter(description="Token")
    filteredCards = []
    for card in tokens:
        for deck in card.deck.all():
            if deck.user == request.user and card not in filteredCards:
                filteredCards.append(card)
    return render(request, "cards/tokens_index.html", {"tokens": filteredCards})


def token(request, token_id):
    token = get_object_or_404(Card, pk=token_id)
    form = AssociationForm(user=request.user)
    return render(request, 'cards/token_consult.html', {"token": token, "form": form})


def tokenAddView(request):
    if request.method == "POST":
        form = AddTokenForm(request.POST, user=request.user)
        if form.is_valid():
            token = Card(name=request.POST["name"] + ' Token')
            token.save()
            results = dict(QueryDict.lists(request.POST))
            # On associe les couleur le deck en création
            for color in results["colors"]:
                color_to_add = Color.objects.filter(color=color)
                if not color_to_add:
                    color = Color(color=color)
                    color.save()
                    token.colors.add(color)
                else:
                    token.colors.add(color_to_add[0])

            print(results)
            # On associe les types de la carte Magic avec la carte en création
            types = []
            if "types" in results:
                for type_item in results["types"]:
                    type_to_add = CardType.objects.filter(name=type_item)
                    types.append(type)
                    if not type_to_add:
                        new_type = CardType(name=type)
                        new_type.save()
                        token.types.add(new_type)
                    else:
                        token.types.add(type_to_add[0])

            # On associe les decks avec la carte en création
            for deck_item in results["deck"]:
                deck_to_add = Deck.objects.filter(name=deck_item)
                token.deck.add(deck_to_add[0])

            token.power = results["power"][0]
            token.defense = results["defense"][0]
            token.description = "Token"
            token.language = results["language"][0]

            for add_type in results["add_type"]:
                if add_type != "" and add_type not in types:
                    new_type = CardType(name=add_type)
                    new_type.save()
                    token.types.add(new_type)

            token.save()

            return redirect('tokens_index')
    else:
        form = AddTokenForm(user=request.user)

    return render(request, 'cards/token_add.html', context={"form": form})


class TokenEditView(UpdateView):
    model = Card
    context_object_name = "token"
    form_class = EditTokenForm
    template_name = "cards/token_add.html"


class TokenDeleteView(DeleteView):
    model = Card
    context_object_name = "token"
    template_name = "cards/token_delete.html"
    success_url = reverse_lazy("tokens_index")


def associateTokenToDeckView(request, card_id):
    token = Card.objects.filter(pk=card_id)[0]
    if request.method == "POST":
        form = AssociationForm(request.POST, user=request.user)
        if form.is_valid():
            for deck in form.cleaned_data["deck"]:
                deck_to_associate = Deck.objects.filter(name=deck)[0]
                token.deck.add(deck_to_associate)
            token.save()
            return render(request, "cards/token_consult.html", context={"token": token, "form": form})
    else:
        form = AssociationForm(user=request.user)
    return render(request, "cards/token_consult.html", context={"token": token, "form": form})


def removeTokenFromDeckView(request, deck_id, token_id):
    token = Card.objects.filter(pk=token_id)[0]
    deck = Deck.objects.filter(pk=deck_id)[0]
    token.deck.remove(deck)
    token.save()

    return redirect(deck)


def playground(request):
    user = request.user
    decks = Deck.objects.filter(user=user)
    return render(request, "cards/playground.html", context={"decks": decks})


def playground_game_starts(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]

    if not Playground.objects.filter(user=request.user, deck=deck):
        # On crée et on stocke la partie
        playground = Playground(user=request.user)
        playground.deck = deck
        json = {
            "life": 20,
            "cards": [],
        }
        playground.config = json
        playground.save()
    else:
        json = Playground.objects.filter(user=request.user, deck=deck)[0].config

    return render(request, "cards/playground_game_starts.html", context={"deck": deck, "json": json})


def playground_add_card(request, card_id, deck_id):
    card = Card.objects.filter(pk=card_id)[0]
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(user=request.user, deck=deck)[0]
    types = []
    for type in card.types.all():
        types.append(type.name)

    colors = []
    for color in card.colors.all():
        colors.append(color.color)

    json = playground.config

    index = len(json["cards"])

    json["cards"].append(
        {
            "pk": card.pk,
            "index": index + 1,
            "name": card.name,
            "colors": colors,
            "types": types,
            "description": card.description,
            "power": card.power,
            "defense": card.defense,
            "isFlying": card.isFlying,
            "language": card.language,
            "illustration": card.illustration,
        }
    )
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)


def playground_remove_creature(request, deck_id, index):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(user=request.user, deck=deck)[0]
    json = playground.config
    cards = []
    for card in json['cards']:
        if card['index'] != int(index):
            cards.append(card)
    json['cards'] = cards
    playground.config = json
    playground.save()

    return redirect('playground_game_starts', deck_id=deck.pk)

