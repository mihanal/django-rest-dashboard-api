from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.get_players, name='get_all_players'),
    path('players/<int:id>', views.get_player, name='get_player'),
    path('teams/', views.get_teams, name='get_all_teams'),
    path('teams/<int:id>', views.get_team),
    path('teams/<int:id>/players', views.get_team_players),
    path('teams/<int:id>/average', views.get_average_players),
    path('games/', views.get_games)
]