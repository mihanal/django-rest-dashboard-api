from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from league.models import User, Player, Team


class GetPlayersTest(APITestCase):

    def setUp(self):

        """ Players """
        user = User.objects.create(first_name='Damien', last_name='Sam', username='Damien', is_player=True)
        team = Team.objects.create(name='Light')
        Player.objects.create(height=130, user=user, team=team)

        self.superuser = User.objects.create_superuser('abc', 'abc@a.com', 'pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)

    def test_get_players(self):
        response = self.client.get(reverse('get_all_players'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['first_name'], 'Damien')


class GetPlayer(APITestCase):

    def setUp(self):

        """ Player """
        user = User.objects.create(first_name='Damien', last_name='Sam', username='Damien', is_player=True)
        team = Team.objects.create(name='Light')
        Player.objects.create(id='1', height=130, user=user, team=team)

        self.superuser = User.objects.create_superuser('abc', 'abc@a.com', 'pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)

    def test_get_player(self):
        response = self.client.get(reverse('get_player', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'Damien')


class GetTeamsTest(APITestCase):

    def setUp(self):

        """ Teams """
        Team.objects.create(id='1', name='White')
        Team.objects.create(id='2', name='Black')

        self.superuser = User.objects.create_superuser('abc', 'abc@a.com', 'pass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)

    def test_get_user_list(self):
        response = self.client.get(reverse('get_all_teams'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)


