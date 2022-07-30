from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from cards.models import Card, Color, CardType, Deck, Playground, PlainsWalker
from mtgsdk import Card as MtgCard
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from cards.forms import AddCardForm, DeckForm, EditDeckForm, AssociationForm, AddTokenForm, EditTokenForm,  \
     CustomCounterForm, EditCardForm, AddPlainswalkerForm, EditPlainswalkerForm
from datetime import datetime
import json





def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        cards = Card.objects.all().order_by('name')
        filteredCards = []
        for card in cards:
            for deck in card.deck.all():
                if deck.user == request.user and card not in filteredCards:
                    filteredCards.append(card)
        return render(request, "cards/cards_index.html", {"cards": filteredCards})


def card(request, card_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        card = get_object_or_404(Card, id=card_id)
        form = AssociationForm(user=request.user)

        return render(request, 'cards/card_consult.html', {"card": card, "form": form})


# Ajout d'une carte en mode FBV Function Based Views'
def addCard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        if request.method == "POST":
            # request.POST = les données récupérées du formulaire (dictionnaire)
            form = AddCardForm(request.POST, user=request.user)
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
                    if "flying" in mtgcard[0].text.lower() or "vol" in mtgcard[0].text.lower():
                        card.isFlying = True
                    if "lifelink" in mtgcard[0].text.lower() or "lien de vie" in mtgcard[0].text.lower():
                        card.isLifeLink = True
                    if "haste" in mtgcard[0].text.lower() or "Célérité" in mtgcard[0].text.lower():
                        card.hasHaste = True
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
    form_class = EditCardForm
    template_name = "cards/card_edit.html"


# Suppression d'une carte en mode CBV Class Based View
class CardDeleteView(DeleteView):
    model = Card
    context_object_name = "card"
    template_name = "cards/card_delete.html"
    success_url = reverse_lazy("cards_index")


def deck_index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        decks = Deck.objects.filter(user=request.user).order_by('name')
        return render(request, "cards/decks_index.html", {"decks": decks})


def deck(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = get_object_or_404(Deck, pk=deck_id)
        return render(request, 'cards/deck_consult.html', {"deck": deck})


def deckAddView(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
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
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
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
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        card = Card.objects.filter(pk=card_id)[0]
        deck = Deck.objects.filter(pk=deck_id)[0]
        card.deck.remove(deck)
        card.save()

        return redirect(deck)


def token_index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        tokens = Card.objects.all().filter(description="Token")
        filteredCards = []
        for card in tokens:
            for deck in card.deck.all():
                if deck.user == request.user and card not in filteredCards:
                    filteredCards.append(card)
        return render(request, "cards/tokens_index.html", {"tokens": filteredCards})


def token(request, token_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        token = get_object_or_404(Card, pk=token_id)
        form = AssociationForm(user=request.user)
        return render(request, 'cards/token_consult.html', {"token": token, "form": form})


def tokenAddView(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
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
                token.isFlying = results["isFlying"][0]
                token.isLifeLink = results["isLifeLink"][0]
                token.hasHaste = results["hasHaste"][0]


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
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
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
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        token = Card.objects.filter(pk=token_id)[0]
        deck = Deck.objects.filter(pk=deck_id)[0]
        token.deck.remove(deck)
        token.save()

        return redirect(deck)


def plainswalkers_index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        plainswalkers = PlainsWalker.objects.all().order_by('name')
        filteredCards = []
        for card in plainswalkers:
            for deck in card.deck.all():
                if deck.user == request.user and plainswalker not in filteredCards:
                    filteredCards.append(plainswalker)
        return render(request, "cards/plainswalkers_index.html", {"plainswalkers": plainswalkers})


def plainswalker(request, plainswalker_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        plainswalker = get_object_or_404(PlainsWalker, pk=plainswalker_id)
        form = AssociationForm(user=request.user)
        return render(request, 'cards/plainswalker_consult.html', {"plainswalker": plainswalker, "form": form})


def plainswalkerAddView(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        if request.method == "POST":
            # request.POST = les données récupérées du formulaire (dictionnaire)
            form = AddPlainswalkerForm(request.POST, user=request.user)
            if form.is_valid():
                mtgcard = MtgCard \
                    .where(name=request.POST["name"]) \
                    .where(language=request.POST["language"]) \
                    .all()
                if not mtgcard:
                    mtgcard = MtgCard \
                        .where(name=request.POST["name"]) \
                        .all()
                if not mtgcard:
                    error = "Le plainswalker n'existe pas !"
                    return render(request, 'cards/plainswalker_add.html', context={
                        "form": form,
                        "error": error
                    })
                else:
                    plainswalker = PlainsWalker(name=request.POST["name"])
                    illustration = mtgcard[0].image_url
                    if illustration:
                        plainswalker.illustration = illustration
                    else:
                        for i in range(1, len(mtgcard)):
                            illustration = mtgcard[i].image_url
                            if illustration:
                                plainswalker.illustration = illustration
                                break
                            else:
                                "Aucune illustration trouvée"
                    plainswalker.save()

                    # On associe les couleur de la carte Magic avec la carte en création
                    for color in mtgcard[0].colors:
                        color_to_add = Color.objects.filter(color=color)
                        if not color_to_add:
                            new_color = Color(color=color)
                            new_color.save()
                            plainswalker.colors.add(new_color)
                        else:
                            plainswalker.colors.add(color_to_add[0])

                    # On associe les decks avec la carte en création
                    results = dict(QueryDict.lists(request.POST))
                    for deck in results["deck"]:
                        deck_to_add = Deck.objects.filter(name=deck)
                        plainswalker.deck.add(deck_to_add[0])

                    # plainswalker.loyalty = mtgcard[0].power
                    plainswalker.description = mtgcard[0].text
                    plainswalker.loyalty= mtgcard[0].loyalty
                    plainswalker.language = request.POST["language"]
                    plainswalker.save()

                # "commit=False", dans la fonction save() empêche la sauveagarde en BDD
                # Cela permet de traiter l'objet Card hydraté
                # form.save()
                # On redirige vers la même page pour éviter la ressoumission des données par erreur
                return HttpResponseRedirect(request.path)
        else:
            form = AddPlainswalkerForm(user=request.user)

        return render(request, 'cards/plainswalker_add.html', context={"form": form})


class PlainswalkerEditView(UpdateView):
    model = PlainsWalker
    context_object_name = "plainswalker"
    form_class = EditPlainswalkerForm
    template_name = "cards/plainswalker_add.html"


class PlainswalkerDeleteView(DeleteView):
    model = PlainsWalker
    context_object_name = "plainswalker"
    template_name = "cards/plainswalker_delete.html"
    success_url = reverse_lazy("plainswalkers_index")


def associatePlainswalkerToDeckView(request, plainswalker_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        plainswalker = PlainsWalker.objects.filter(pk=plainswalker_id)[0]
        if request.method == "POST":
            form = AssociationForm(request.POST, user=request.user)
            if form.is_valid():
                for deck in plainswalker.deck.all():
                    plainswalker.deck.remove(deck)
                for deck in form.cleaned_data["deck"]:
                    deck_to_associate = Deck.objects.filter(name=deck)[0]
                    plainswalker.deck.add(deck_to_associate)
                plainswalker.save()
                return render(request, "cards/plainswalker_consult.html", context={"plainswalker": plainswalker, "form": form})
        else:
            form = AssociationForm(user=request.user)
        return render(request, "cards/plainswalker_consult.html", context={"plainswalker": plainswalker, "form": form})


def removePlainswalkerFromDeckView(request, deck_id, plainswalker_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        plainswalker = PlainsWalker.objects.filter(pk=plainswalker_id)[0]
        deck = Deck.objects.filter(pk=deck_id)[0]
        plainswalker.deck.remove(deck)
        plainswalker.save()

        return redirect(deck)


def playground(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        user = request.user
        decks = Deck.objects.filter(user=user)
        return render(request, "cards/playground.html", context={"decks": decks})


def playground_game_starts(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        is_flying_deck = False
        is_lifelink_deck = False
        is_haste_deck = False
        deck = Deck.objects.filter(pk=deck_id)[0]
        if not Playground.objects.filter(user=request.user, deck=deck):
            # On crée et on stocke la partie
            playground = Playground(user=request.user)
            playground.deck = deck
            json = {
                "life": 20,
                "damages": 0,
                "turn": {
                    "count": 1,
                    "state": "open"
                },
                "cemetery": [],
                "cards": [],
                "plainswalkers": []
            }
            playground.config = json
            playground.creation_date = datetime.today()
            playground.last_update_date = datetime.today()
            playground.history = { "logs" : [
                    {
                        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S') : request.user.username + " a débuté une partie."
                    }
                ]
            }
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                    "Le tour " + str(playground.config["turn"]['count']) + " commence."
            })
            playground.save()
            form = CustomCounterForm(deck=deck)
            return render(request, "cards/playground_game_starts.html", context={
                "deck": deck,
                "json": json,
                "form": form,
                "is_flying_deck": is_flying_deck,
                "is_lifelink_deck": is_lifelink_deck,
                "is_haste_deck": is_haste_deck,
                "history": list(reversed(playground.history["logs"]))
            })
        else:
            playground = Playground.objects.filter(user=request.user, deck=deck)[0]
            json = playground.config
            if request.method == "POST":
                form = CustomCounterForm(request.POST, deck=deck)
                if form.is_valid:
                    power = request.POST.get("power")
                    defense = request.POST.get("defense")
                    forFlying = request.POST.get("forFlying")
                    types = request.POST.get("types")
                    colors = request.POST.get("colors")

                    if forFlying:
                        flyingToAddInLogs = "volantes"
                    else:
                        flyingToAddInLogs = ""

                    if types is not None:
                        typesToAddInLogs = types
                    else:
                        typesToAddInLogs = ""

                    if colors is not None:
                        colorsToAddInLogs = colors
                    else:
                        colorsToAddInLogs = ""

                    for card in json['cards']:
                        to_be_incremented = False
                        for type in card['types']:
                            if types is not None and type in types:
                                to_be_incremented = True
                                typesToAddInLogs = type
                                break
                        for color in card['colors']:
                            if colors is not None and color in colors:
                                to_be_incremented = True
                                colorsToAddInLogs = color
                                break
                        if card['isFlying'] and forFlying:
                            to_be_incremented = True
                        if card['isFlying']:
                            is_flying_deck = True
                        if card['isLifeLink']:
                            is_lifelink_deck = True
                        if to_be_incremented:
                            if card['tapped']:
                                json['damages'] -= int(card['power'])

                            if "*" in card['power'] or "*" in card['defense']:
                                card['power'] = str(0 + int(power))
                                card['defense'] = str(0 + int(defense))
                            else:
                                card['power'] = str(int(card['power']) + int(power))
                                card['defense'] = str(int(card['defense']) + int(defense))

                            if card['tapped']:
                                json['damages'] += int(card['power'])

                    playground.last_update_date = datetime.today()
                    playground.history['logs'].append(
                        {
                            playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                            "Toutes les creatures " + typesToAddInLogs + " " + colorsToAddInLogs + " "
                            + flyingToAddInLogs + " ont reçu " + power + "/" + defense + "."
                        }
                    )

                    playground.last_update_date = datetime.today()
                    playground.save()
                    return redirect("playground_game_starts", deck_id=deck.pk)
            else:
                for card in json['cards']:
                    if card['isFlying']:
                        is_flying_deck = True
                    if card['isLifeLink']:
                        is_lifelink_deck = True
                    if card['hasHaste']:
                        is_haste_deck = True
                    if card["invokation"]["turn"] != json["turn"]["count"]:
                        card["invokation"]["state"] = False
                        playground.last_update_date = datetime.today()
                        playground.save()
                form = CustomCounterForm(deck=deck)

                return render(request, "cards/playground_game_starts.html", context={
                    "deck": deck,
                    "json": json,
                    "form": form,
                    "is_flying_deck": is_flying_deck,
                    "is_lifelink_deck": is_lifelink_deck,
                    "is_haste_deck": is_haste_deck,
                    "history": list(reversed(playground.history["logs"]))
                })


def playground_add_card(request, card_id, deck_id, number_of_cards):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        card = Card.objects.filter(pk=card_id)[0]
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]

        for i in range(0, int(number_of_cards)):
            types = []
            for type in card.types.all():
                types.append(type.name)

            colors = []
            for color in card.colors.all():
                colors.append(color.color)

            json = playground.config

            index = len(json["cards"])

            invokation = True
            if card.hasHaste:
                invokation = False

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
                    "isLifeLink": card.isLifeLink,
                    "hasHaste": card.hasHaste,
                    "language": card.language,
                    "illustration": card.illustration,
                    "tapped":False,
                    "invokation": {
                        "state":invokation,
                        "turn": json['turn']['count']
                    },
                    "isDefended": False
                }
            )

            playground.last_update_date = datetime.today()
            playground.history['logs'].append({ playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S') : card.name + " a été invoqué !"})
            playground.save()
        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_remove_creature(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        cards = []
        count = 1
        for card in json['cards']:
            if "*" in str(card['power']):
                card['power'] = 0
            if "*" in str(card['defense']):
                card['defense'] = 0
            if card['index'] != int(index):
                card['index'] = count
                cards.append(card)
                count += 1
            else:
                if "Token" not in card["description"]:
                    json['cemetery'].append(card)
                if card['tapped']:
                    json['damages'] -= int(card['power'])
                playground.last_update_date = datetime.today()
                playground.history['logs'].append(
                    {
                        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                        + " a été mise au cimetière !"
                    }
                )
        json['cards'] = cards
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)

def playground_remove_plainswalker(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        plainswalkers = []
        count = 1
        for plainswalker in json['plainswalkers']:
            if plainswalker['index'] != int(index):
                plainswalker['index'] = count
                plainswalkers.append(plainswalker)
                count += 1
            else:
                playground.last_update_date = datetime.today()
                playground.history['logs'].append(
                    {
                        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Le planeswalker "
                        + plainswalker['name'] + " a été mise au cimetière !"
                    }
                )
        json['plainswalkers'] = plainswalkers
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_save(request, deck_id, card_index, button, new_value):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        for card in json['cards']:
            if card['index'] == int(card_index):
                if button == "defense-plus" or button == "defense-minus":
                    card['defense'] = new_value
                    if button == "defense-plus":
                        playground.last_update_date = datetime.today()
                        playground.history['logs'].append(
                            {
                                playground.last_update_date.strftime(
                                    '%d-%m-%Y %H:%M:%S'): card['name'] + " a gagné +1 en défense."
                            }
                        )
                    else:
                        playground.last_update_date = datetime.today()
                        playground.history['logs'].append(
                            {
                                playground.last_update_date.strftime(
                                    '%d-%m-%Y %H:%M:%S'): card['name'] + " a perdu -1 en défense."
                            }
                        )
                else:
                    if button == "power-plus":
                        playground.last_update_date = datetime.today()
                        playground.history['logs'].append(
                            {
                                playground.last_update_date.strftime(
                                    '%d-%m-%Y %H:%M:%S'): card['name'] + " a gagné +1 en attaque."
                            }
                        )
                        if card['isLifeLink']:
                            json["life"] += 1
                            playground.last_update_date = datetime.today()
                            playground.history['logs'].append({
                                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                                    request.user.username + " gagne 1 point de vie (lien de vie de " + card['name']
                                    + "). Nouveau total de points de vie : "
                                    + str(json['life'])}
                            )
                    else:
                        playground.last_update_date = datetime.today()
                        playground.history['logs'].append(
                            {
                                playground.last_update_date.strftime(
                                    '%d-%m-%Y %H:%M:%S'): card['name'] + " a perdu -1 en attaque."
                            }
                        )
                        if card['isLifeLink']:
                            json["life"] -= 1
                            playground.last_update_date = datetime.today()
                            playground.history['logs'].append({
                                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                                    request.user.username + " a perdu 1 point de vie (lien de vie de " + card['name']
                                    + "). Nouveau total de points de vie : "
                                    + str(json['life'])}
                            )
                    if card['tapped']:
                        json['damages'] -= int(card['power'])
                    card['power'] = new_value
                    if card['tapped']:
                        json['damages'] += int(new_value)
        playground.config = json
        playground.save()
        return HttpResponse()

def playground_save_plainswalker(request, deck_id, plainswalker_index, button, new_value):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        for plainswalker in json['plainswalkers']:
            if plainswalker['index'] == int(plainswalker_index):
                if button == "loyalty-plus" or button == "loyalty-minus":
                    playground.last_update_date = datetime.today()
                    plainswalker['loyalty'] = new_value
                    if button == "loyalty-plus":
                        playground.history['logs'].append(
                            {
                                playground.last_update_date.strftime(
                                    '%d-%m-%Y %H:%M:%S'): "La loyauté de " + plainswalker['name'] + " a gagné +1."
                            }
                        )
                    else:
                        playground.history['logs'].append(
                            {
                                playground.last_update_date.strftime(
                                    '%d-%m-%Y %H:%M:%S'): "La loyauté de " + plainswalker['name'] + " a perdu -1."
                            }
                        )
        playground.config = json
        playground.save()
        return HttpResponse()


def playground_save_for_all(request, deck_id, button):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config

        playground.last_update_date = datetime.today()
        if button == "power-plus":
            playground.history['logs'].append(
                {
                    playground.last_update_date.strftime(
                        '%d-%m-%Y %H:%M:%S'): "toutes les cartes ont gagné +1 en attaque."
                }
            )
        elif button == "power-minus":
            playground.history['logs'].append(
                {
                    playground.last_update_date.strftime(
                        '%d-%m-%Y %H:%M:%S'): "toutes les cartes ont perdu -1 en attaque."
                }
            )
        elif button == "defense-plus":
            playground.history['logs'].append(
                {
                    playground.last_update_date.strftime(
                        '%d-%m-%Y %H:%M:%S'): "toutes les cartes ont gagné +1 en défense."
                }
            )
        else:
            playground.history['logs'].append(
                {
                    playground.last_update_date.strftime(
                        '%d-%m-%Y %H:%M:%S'): "toutes les cartes ont perdu -1 en défense."
                }
            )

        for card in json['cards']:
            power = card['power']
            defense = card['defense']
            if "*" in card['power']:
                power = 0
            if "*" in card['defense']:
                defense = 0
            power = int(power)
            defense = int(defense)

            if button == "power-plus":
                if card['tapped']:
                    json['damages'] -= power
                    power += 1
                    json['damages'] += power
                    if card['isLifeLink']:
                        json["life"] += 1
                        playground.history['logs'].append({
                            playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                                request.user.username + " gagne 1 point de vie (lien de vie de " + card['name']
                                + "). Nouveau total de points de vie : "
                                + str(json['life'])}
                        )
                else:
                    power += 1
            elif button == "power-minus":
                if power != 0:
                    if card['tapped']:
                        json['damages'] -= power
                        power -= 1
                        json['damages'] += power
                        if card['isLifeLink']:
                            json["life"] -= 1
                            playground.history['logs'].append({
                                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                                    request.user.username + " a perdu 1 point de vie (lien de vie de " + card['name']
                                    + "). Nouveau total de points de vie : "
                                    + str(json['life'])}
                            )
                    else:
                        power -= 1
            elif button == "defense-plus":
                defense += 1
            elif button == "defense-minus":
                if  defense != 0:
                    defense -= 1

            card['power'] = str(power)
            card['defense'] = str(defense)

        playground.config = json
        playground.save()
        return HttpResponse()


def playground_reset_all(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config

        for plainswalker in json['plainswalkers']:
            for original_plainswalker in deck.plainswalkers.all():
                if plainswalker['pk'] == original_plainswalker.pk:
                    plainswalker['loyalty'] = str(original_plainswalker.loyalty)
        for card in json['cards']:
            for original_card in deck.cards.all():
                if card['pk'] == original_card.pk:
                    if "*" in original_card.power:
                        card['power'] = str(0)
                    else:
                        card['power'] = str(original_card.power)

                    if "*" in original_card.defense:
                        card['defense'] = str(0)
                    else:
                        card['defense'] = str(original_card.defense)

        playground.last_update_date = datetime.today()
        playground.history['logs'].append(
            {
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les cartes ont été réinitialisées."
            }
        )
        playground.save()
        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_kill_game(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        playground.delete()
        return redirect('playground')


def playground_life_save(request, deck_id, button):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        if button == "life-plus":
            json['life'] = int(json['life']) + 1
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                request.user.username + " a gagné 1 point de vie ! Total des points de vies : " + str(json['life'])}
            )
        elif button == "life-minus":
            json['life'] = int(json['life']) - 1
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): request.user.username
                + " a perdu 1 point de vie ! Total des points de vies : " + str(json['life'])}
            )
        playground.config = json
        playground.save()
        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_attack(request, deck_id, card_index):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config

    tapped = 0
    for card in json['cards']:
        if card['tapped']:
            tapped += 1
    if tapped == 0:
        json['turn']['state'] = "attack"
        playground.last_update_date = datetime.today()
        playground.history['logs'].append({
            playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                "Le tour " + str(playground.config["turn"]['count']) + " est passé en mode attaque."
        })

    for card in json["cards"]:
        power = card['power']
        if "*" in str(card['power']):
            power = 0
        power = int(power)
        if card['index'] == int(card_index):
            card['tapped'] = True
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                + " attaque et inflige "
                + str(power) + " points de dégats !"}
            )
            if card['isLifeLink']:

                json['life'] += int(card['power'])
                playground.last_update_date = datetime.today()
                playground.history['logs'].append({
                    playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                    "Durant l'attaque, "
                    + card['name']
                    + " donne +" + str(power) + " points de vie à " + request.user.username
                    + " grâce à son lien de vie. Nouveau total de points de vie : "
                    + str(json['life'])}
                )
            json['damages'] += power

    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)


def playground_untap(request, deck_id, card_index):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config
    count = 0
    for card in json["cards"]:
        power = card['power']
        if "*" in card['power']:
            power = 0
        power = int(power)
        if card['index'] == int(card_index):
            card['tapped'] = False
            json['damages'] -= power
            if card['isLifeLink']:
                json['life'] -= power
        if card['tapped']:
            count += 1

    if count == 0:
        json['turn']['state'] = "open"
        playground.last_update_date = datetime.today()
        playground.history['logs'].append({
            playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                "Le tour " + str(playground.config["turn"]['count']) + " est repassé en actif."
        })
    playground.config = json
    playground.last_update_date = datetime.today()
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)

def playground_attack_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config
    json['damages'] = 0
    json['turn']['state'] = "attack"
    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
            "Le tour " + str(playground.config["turn"]['count']) + " est passé en mode attaque."
    })
    for card in json["cards"]:
        power = card['power']
        if "*" in str(card['power']):
            power = 0
        power = int(power)
        if not card['invokation']['state'] and "Wall" not in card['types']:
            card['tapped'] = True
            json['damages'] += power
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                + " attaque et inflige "
                + str(power) + " points de dégats !"}
            )
            if card['isLifeLink']:
                json['life'] += int(power)
                playground.last_update_date = datetime.today()
                playground.history['logs'].append({
                    playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                    "Durant l'attaque, "
                    + card['name']
                    + " donne +" + str(power) + " points de vie à " + request.user.username
                    + " grâce à son lien de vie. Nouveau total de points de vie : "
                    + str(json['life'])}
                )
    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)

def playground_untap_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config
    for card in json["cards"]:
        power = card['power']
        if "*" in str(card['power']):
            power = 0
        power = int(power)
        if card['tapped']:
            if not card['isDefended']:
                json['damages'] -= power
            if card['isLifeLink']:
                json['life'] -= power
        card['tapped'] = False
        card['isDefended'] = False

    json['turn']["state"] = "open"
    playground.config = json
    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
            "L'attaque a été annulée par " + request.user.username
    })
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)

def playground_reorder_cards(request, deck_id, slug):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    config = playground.config
    slug = json.loads(slug)

    cards = []
    for c in config['cards']:
        cards.append({})

    for card in config["cards"]:
        card['index'] = int(slug.get(str(card['index'])))
        cards[card['index'] - 1] = card

    config['cards'] = cards
    playground.config = config
    playground.last_update_date = datetime.today()
    playground.save()
    return HttpResponse()


def playground_kill_all(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config

        plainswalkers = []
        for plainswalker in json['plainswalkers']:
            json['cemetery'].append(plainswalker)
        json['plainswalkers'] = plainswalkers

        cards = []
        for card in json['cards']:
            if "Token" not in card["description"]:
                json['cemetery'].append(card)
            if card['tapped']:
                json['damages'] -= int(card['power'])
        json['cards'] = cards
        playground.config = json
        playground.last_update_date = datetime.today()
        playground.history['logs'].append({
            playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les créatures ont été mises au cimetière !"
        })
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_flying_creature(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        cards = []
        for card in json['cards']:
            if card['index'] == int(index):
               card["isFlying"] = True
               playground.last_update_date = datetime.today()
               playground.history['logs'].append({
                   playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                   + " a maintenant le vol"}
               )
            cards.append(card)
        json['cards'] = cards
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)

def playground_non_flying_creature(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        cards = []
        for card in json['cards']:
            if card['index'] == int(index):
               card["isFlying"] = False
               playground.last_update_date = datetime.today()
               playground.history['logs'].append({
                   playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name'] + " a perdu le vol"}
               )
            cards.append(card)

        json['cards'] = cards
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)

def playground_flying_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config

    for card in json["cards"]:
        card['isFlying'] = True

    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les créatures ont maintenant le vol"}
    )
    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)


def playground_non_flying_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config

    for card in json["cards"]:
        card['isFlying'] = False

    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les créatures ont perdu le vol"}
    )

    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)

def playground_lifelink_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config

    for card in json["cards"]:
        card['isLifeLink'] = True

    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les créatures ont maintenant le lien de vie."}
    )

    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)


def playground_non_lifelink_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config

    for card in json["cards"]:
        card['isLifeLink'] = False

    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les créatures ont perdu le lien de vie."}
    )

    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)


def playground_lifelink_creature(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        cards = []
        for card in json['cards']:
            if card['index'] == int(index):
               card["isLifeLink"] = True
               playground.last_update_date = datetime.today()
               playground.history['logs'].append({
                   playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                   + " a maintenant le lien de vie"
               })
            cards.append(card)
        json['cards'] = cards
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)

def playground_non_lifelink_creature(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        cards = []
        for card in json['cards']:
            if card['index'] == int(index):
               card["isLifeLink"] = False
               playground.last_update_date = datetime.today()
               playground.history['logs'].append({
                   playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                   + " a perdu le lien de vie"
               })
            cards.append(card)
        json['cards'] = cards
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_haste_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config

    for card in json["cards"]:
        card['hasHaste'] = True

    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les créatures ont maintenant la célérité."}
    )

    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)


def playground_non_haste_all(request, deck_id):
    deck = Deck.objects.filter(pk=deck_id)[0]
    playground = Playground.objects.filter(deck=deck, user=request.user)[0]
    json = playground.config

    for card in json["cards"]:
        card['hasHaste'] = False

    playground.last_update_date = datetime.today()
    playground.history['logs'].append({
        playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): "Toutes les créatures ont perdu la célérité."}
    )

    playground.config = json
    playground.save()
    return redirect('playground_game_starts', deck_id=deck.pk)


def playground_haste_creature(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        cards = []
        for card in json['cards']:
            if card['index'] == int(index):
               card["hasHaste"] = True
               card["invokation"]['state'] = False
               playground.last_update_date = datetime.today()
               playground.history['logs'].append({
                   playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                   + " a maintenant la célérité."
               })
            cards.append(card)
        json['cards'] = cards
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)

def playground_non_haste_creature(request, deck_id, index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        cards = []
        for card in json['cards']:
            if card['index'] == int(index):
               card["hasHaste"] = False
               playground.last_update_date = datetime.today()
               playground.history['logs'].append({
                   playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name']
                   + " a perdu la célérité"
               })
            cards.append(card)
        json['cards'] = cards
        playground.config = json
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_turn_off(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        playground.config["turn"]["state"] = "close"
        playground.last_update_date = datetime.today()
        playground.history['logs'].append({
            playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                "Le tour " + str(playground.config["turn"]['count']) + " a pris fin."
        })
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)

def playground_turn_on(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        playground.config["turn"]["count"] += 1
        playground.config["turn"]["state"] = "open"
        for plainswalker in playground.config['plainswalkers']:
            plainswalker['loyalty'] = str(int(plainswalker['loyalty']) + 1)
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                    "Le planeswalker " + plainswalker["name"] + " gagne +1 en loyauté."
            })
        for card in playground.config['cards']:
            card['isDefended'] = False
            card['tapped'] = False
        playground.config['damages'] = 0
        playground.last_update_date = datetime.today()
        playground.history['logs'].append({
            playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                "Le tour " + str(playground.config["turn"]['count']) + " commence."
        })
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)

def playground_turn_attack(request, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        count = 0
        for card in playground.config["cards"]:
            if card['tapped']:
                count += 1
        if count == 0:
            playground.config["turn"]["state"] = "close"
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                    "Aucune créature n'a attaqué ce tour ci, le tour " + str(playground.config["turn"]['count'])
                    + " a pris fin."
            })
        else:
            playground.config["turn"]["state"] = "attack"
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                    "Le tour " + str(playground.config["turn"]['count']) + " est passé en mode attaque."
            })
        playground.save()

        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_defend(request, deck_id, card_index):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]
        json = playground.config
        count = 0
        for card in json["cards"]:
            power = card['power']
            if "*" in str(card['power']):
                power = 0
            power = int(power)

            if card['index'] == int(card_index):
                json['damages'] -= power
                card['isDefended'] = True
                playground.last_update_date = datetime.today()
                playground.history['logs'].append({
                    playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'): card['name'] + " a été paré. Il reste "
                    + str(json['damages']) + " points de dommage à parer."                                                                            }
                )
            if card['tapped'] and not card['isDefended']:
                count += 1

        if count == 0:
            playground.last_update_date = datetime.today()
            playground.history['logs'].append({
                playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S'):
                    "Le tour " + str(json['turn']['count']) + " a pris fin."
            })
            json['turn']['state'] = "close"

        playground.config = json
        playground.save()
        return redirect('playground_game_starts', deck_id=deck.pk)


def playground_add_plainswalker(request, plainswalker_id, deck_id):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    else:
        plainswalker = PlainsWalker.objects.filter(pk=plainswalker_id)[0]
        deck = Deck.objects.filter(pk=deck_id)[0]
        playground = Playground.objects.filter(user=request.user, deck=deck)[0]

        colors = []
        for color in plainswalker.colors.all():
            colors.append(color.color)

        json = playground.config

        index = len(json["plainswalkers"])

        json["plainswalkers"].append(
            {
                "pk": plainswalker.pk,
                "index": index + 1,
                "name": plainswalker.name,
                "colors": colors,
                "description": plainswalker.description,
                "loyalty": plainswalker.loyalty,
                "language": plainswalker.language,
                "illustration": plainswalker.illustration,
                "tapped":False,
                "invokation": {
                    "state":True,
                    "turn": json['turn']['count']
                },
            }
        )

        playground.last_update_date = datetime.today()
        playground.history['logs'].append({ playground.last_update_date.strftime('%d-%m-%Y %H:%M:%S') : "le Planeswalker " + plainswalker.name + " a été invoqué !"})
        playground.save()
        return redirect('playground_game_starts', deck_id=deck.pk)

