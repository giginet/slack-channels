import os
import requests
import json
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from slack_channel.channels.models import Channel


class Command(BaseCommand):
    BASE_URL = 'https://slack.com/api/channels.list'
    help = 'Update all channels status of your team'

    def _get_auth_token(self):
        token = getattr(settings, 'SLACK_AUTH_TOKEN', None)
        if not token:
            token = os.environ.get('SLACK_AUTH_TOKEN', None)
        if not token:
            raise CommandError('SLACK_AUTH_TOKEN is not set')
        return token

    def handle(self, *args, **options):
        token = self._get_auth_token()
        url = '{}?token={}'.format(self.BASE_URL, token)
        response = requests.get(url)
        response_dict = json.loads(response.text)
        status = response_dict['ok']
        if status:
            channels = response_dict['channels']
            for obj in channels:
                channel, created = Channel.objects.get_or_create(
                    channel_id=obj['id'],
                    defaults={
                        'name': obj['name'],
                        'created_at': datetime.fromtimestamp(obj['created']),
                        'is_archived': obj['is_archived'],
                        'num_members': obj['num_members'],
                        'topic': obj['topic']['value'],
                        'purpose': obj['purpose']['value']
                })
                if created:
                    self.stdout.write("Created {}".format(channel.name))
                else:
                    self.stdout.write("Updated {}".format(channel.name))
            self.stdout.write(self.style.SUCCESS('Succeed'))
        else:
            self.stdout.write(self.style.ERROR(response_dict['error']))
