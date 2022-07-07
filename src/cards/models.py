from itertools import count

from django.db import models
from django.urls import reverse


class Color(models.Model):
    color = models.CharField(max_length=25)
    element = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Couleur"

    def __str__(self):
        return self.color


class Deck(models.Model):
    SAME_CARD_NUMBER = 4
    name = models.CharField(max_length=255)
    colors = models.ManyToManyField(Color, blank=True)

    class Meta:
        verbose_name = "Deck"

    def __str__(self):
        return self.name


class CardType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Type de carte"

    def __str__(self):
        return self.name


class Card(models.Model):
    deck = models.ManyToManyField(Deck)
    name = models.CharField(max_length=100)
    types = models.ManyToManyField(CardType)
    colors = models.ManyToManyField(Color, blank=True)
    description = models.TextField(blank=True)
    power = models.CharField(max_length=4)
    defense = models.CharField(max_length=4)
    illustration = models.URLField(blank=True)

    class Meta:
        verbose_name = "Carte"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("card_consult", kwargs={"card_id": self.pk})




