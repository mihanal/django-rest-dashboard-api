from django.core.management.base import BaseCommand
from django.core.management import call_command

from league.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        call_command('loaddata', 'initial_data.json')
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()
