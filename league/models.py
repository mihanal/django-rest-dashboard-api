from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Team(models.Model):
    id = models.IntegerField(primary_key=True, default='0', editable=False)
    name = models.CharField(max_length=200, blank=False, default='')

    class Meta:
        verbose_name = 'team'
        verbose_name_plural = 'teams'
        ordering = ['id']

    def __str__(self):
        return self.name


class Game(models.Model):
    id = models.IntegerField(primary_key=True, default='0', editable=False)
    venue = models.CharField(max_length=200, blank=False, default='')

    class Meta:
        verbose_name = 'game'
        verbose_name_plural = 'games'
        ordering = ['id']

    def __str__(self):
        return self.venue


class Summary(models.Model):
    class Result(models.TextChoices):
        DRAWN = 'drawn'
        ABANDONED = 'abandoned'
        RESULT = 'result'
        WON = 'won'
        LOST = 'lost'

    id = models.IntegerField(primary_key=True, default='0', editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField(default='0', editable=False)
    result = models.CharField(max_length=200, choices=Result.choices)


class Admin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)


class Coach(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Player(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    height = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal(0.00))
    games = models.ManyToManyField(Game, blank=True)


class Score(models.Model):
    id = models.IntegerField(primary_key=True, default='0', editable=False)
    game = models.ForeignKey(Game, related_name='game_score', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    count = models.IntegerField(default='0', editable=False)
