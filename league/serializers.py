from django.db.models import Sum, Avg, F
from rest_framework import serializers
from league.models import Player, Team, Summary, Score, Game, User


class PlayerSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    number_of_games = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = ('id',
                  'first_name',
                  'last_name',
                  'height',
                  'number_of_games',
                  'average_score')

    @staticmethod
    def get_first_name(obj):
        return User.objects.get(pk=obj.id).first_name

    @staticmethod
    def get_last_name(obj):
        return User.objects.get(pk=obj.id).last_name

    @staticmethod
    def get_number_of_games(obj):
        player = Player.objects.get(pk=obj.pk)
        return player.games.all().count()

    @staticmethod
    def get_average_score(obj):
        player_score = Score.objects.filter(player_id=obj.pk).aggregate(Sum('count'))
        played_games = Player.objects.get(pk=obj.pk).games.all().count()
        if player_score['count__sum'] is not None and played_games is not None:
            return player_score['count__sum']/played_games
        return 0


class TeamSerializer(serializers.ModelSerializer):
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ('id',
                  'name',
                  'average_score')

    @staticmethod
    def get_average_score(obj):
        return Summary.objects.filter(team__id=obj.pk).aggregate(average=Avg(F('score')))['average']


class GameSerializer(serializers.ModelSerializer):
    final_score = serializers.SerializerMethodField()
    team_won = serializers.SerializerMethodField()
    team_lost = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = ('id',
                  'venue',
                  'final_score',
                  'team_won',
                  'team_lost')

    @staticmethod
    def get_final_score(obj):
        team_score_won = Summary.objects.filter(game__id=obj.pk, result='won').values_list('score', flat=True)[0]
        team_score_lost = Summary.objects.filter(game__id=obj.pk, result='lost').values_list('score', flat=True)[0]
        return [team_score_won, team_score_lost]

    @staticmethod
    def get_team_won(obj):
        return Summary.objects.filter(game__id=obj.pk, result='won').values_list('team_id', flat=True)[0]

    @staticmethod
    def get_team_lost(obj):
        return Summary.objects.filter(game__id=obj.pk, result='lost').values_list('team_id', flat=True)[0]

