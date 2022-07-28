from itertools import count

from django.db import models
from django.urls import reverse

from user.models import CustomUser


class Color(models.Model):
    color = models.CharField(max_length=25)
    element = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Couleur"

    def __str__(self):
        return self.color


class Deck(models.Model):
    name = models.CharField(max_length=255)
    colors = models.ManyToManyField(Color, blank=True)
    user = models.ForeignKey(CustomUser, editable=False, on_delete=models.CASCADE, blank=True, null=True, default=0)

    class Meta:
        verbose_name = "Deck"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("deck_consult", kwargs={"deck_id": self.pk})


class CardType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Type de carte"

    def __str__(self):
        return self.name


class Card(models.Model):
    deck = models.ManyToManyField(Deck, related_name="cards")
    name = models.CharField(max_length=100)
    types = models.ManyToManyField(CardType, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    description = models.TextField(blank=True)
    power = models.CharField(max_length=4)
    defense = models.CharField(max_length=4)
    isFlying = models.BooleanField(default=False)
    isLifeLink = models.BooleanField(default=False)
    hasHaste = models.BooleanField(default=False)
    illustration = models.URLField(blank=True)
    language = models.CharField(max_length=50, default="English")

    class Meta:
        verbose_name = "Carte"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("card_consult", kwargs={"card_id": self.pk})


class Playground(models.Model):
    user = models.ForeignKey(CustomUser, editable=False, on_delete=models.CASCADE, blank=True, null=True, default=0)
    deck = models.ForeignKey(Deck, editable=False, on_delete=models.CASCADE, blank=True, null=True, default=0)
    config = models.JSONField(blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    last_update_date = models.DateField(blank=True, null=True)
    history = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name = "Aire de jeu"

    def __str__(self):
        return "playground-" + self.pk

    def get_absolute_url(self):
        return reverse("playground_consult", kwargs={"playground_id": self.pk})







