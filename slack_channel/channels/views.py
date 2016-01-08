from django.views.generic.list import ListView
from slack_channel.channels.models import Channel


class ChannelListView(ListView):
    model = Channel
