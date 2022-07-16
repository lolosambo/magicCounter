from django.shortcuts import render, redirect
from cards.models import Deck


def index(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("compte/login")
    else:
        decks = Deck.objects.filter(user=user)
        return render(request, "magicCounter/index.html", context={"user": user, "decks": decks})