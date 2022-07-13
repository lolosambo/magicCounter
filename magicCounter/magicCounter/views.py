from django.shortcuts import render
from cards.models import Deck


def index(request):
    user = request.user
    decks = Deck.objects.filter(user=user)
    return render(request, "magicCounter/index.html", context={"user": user, "decks": decks})