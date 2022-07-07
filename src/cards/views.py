from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from cards.models import Card
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
            # "commit=False", dans la fonction save() empêche la sauveagarde en BDD
            # Cela permet de traiter l'objet Card hydraté
            form.save()
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

