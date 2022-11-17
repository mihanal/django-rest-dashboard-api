from django.db.models import Sum
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from league.models import Player, Team, Summary, Score, Game
from league.permission import IsCoach, IsAdmin
from league.serializers import PlayerSerializer, TeamSerializer, GameSerializer

AVERAGE_THRESHOLD = 90


# GET all players
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_players(request):

    players = Player.objects.all()
    players_serializer = PlayerSerializer(players, many=True)
    return JsonResponse(players_serializer.data, safe=False)


# GET player info
@api_view(['GET'])
def get_player(request, id):

    try:
        player = Player.objects.get(pk=id)
    except Player.DoesNotExist:
        return JsonResponse({'message': 'The player does not exist'}, status=status.HTTP_404_NOT_FOUND)

    player_serializer = PlayerSerializer(player)
    return JsonResponse(player_serializer.data, safe=False)


# GET all teams
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_teams(request):

    teams = Team.objects.all()
    teams_serializer = TeamSerializer(teams, many=True)
    return JsonResponse(teams_serializer.data, safe=False)


# GET team info
@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsCoach | IsAdmin)])
def get_team(request, id):

    try:
        team = Team.objects.get(pk=id)
    except Team.DoesNotExist:
        return JsonResponse({'message': 'The team does not exist'}, status=status.HTTP_404_NOT_FOUND)

    team_serializer = TeamSerializer(team)
    return JsonResponse(team_serializer.data, safe=False)


# GET players of a team
@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsCoach | IsAdmin)])
def get_team_players(request, id):

    try:
        Team.objects.get(pk=id)
    except Team.DoesNotExist:
        return JsonResponse({'message': 'The team does not exist'}, status=status.HTTP_404_NOT_FOUND)

    players = Player.objects.filter(team__id=id)
    players_serializer = PlayerSerializer(players, many=True)
    return JsonResponse(players_serializer.data, safe=False)


# GET above average player : const
@api_view(['GET'])
@permission_classes([IsAuthenticated, (IsCoach | IsAdmin)])
def get_average_players(request, id):

    try:
        Team.objects.get(pk=id)
    except Team.DoesNotExist:
        return JsonResponse({'message': 'The team does not exist'}, status=status.HTTP_404_NOT_FOUND)

    team_sum_score = Summary.objects.filter(team__id=id).aggregate(Sum('score'))['score__sum']
    team_match_count = Summary.objects.filter(team__id=id).count()
    team_player_average = 0
    if team_match_count is not None:
        team_player_average = team_sum_score/(team_match_count * 5)

    averaged_players = []
    if team_player_average > 0:
        players = Player.objects.filter(team__id=id)
        for player in players:
            player_score = Score.objects.filter(player__id=player.pk).aggregate(Sum('count'))['count__sum']
            played_games = Player.objects.get(pk=player.pk).games.all().count()
            if player_score is not None and played_games is not None:
                player_avg_score = player_score/played_games
                percentage = player_avg_score/team_player_average * 100
                if percentage >= AVERAGE_THRESHOLD:
                    averaged_players.append(player)

    players_serializer = PlayerSerializer(averaged_players, many=True)
    return JsonResponse(players_serializer.data, safe=False)


# GET all games
@api_view(['GET'])
def get_games(request):

    games = Game.objects.all()
    games_serializer = GameSerializer(games, many=True)
    return JsonResponse(games_serializer.data, safe=False)

