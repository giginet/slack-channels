import datetime
from factory.django import DjangoModelFactory

from slack_channel.channels.models import Channel


class ChannelFactory(DjangoModelFactory):
    class Meta:
        model = Channel

    channel_id = 'ABCDEFGHIJ'
    name = '#freetalk'
    created_at = datetime.datetime(2015, 1, 24)
    is_archived = True
    num_numbers = 6
    topic = 'for free talk'
    purpose = 'for free talk'
    fetched_at = datetime.datetime(2015, 1, 24)
