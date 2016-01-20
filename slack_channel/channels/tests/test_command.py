from unittest.mock import patch, MagicMock, PropertyMock
from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings

from slack_channel.channels.models import Channel


class RetrieveChannelsCommandTestCase(TestCase):
    DUMMY_RESPONSE = '''
{
    "ok": true,
    "channels": [
        {
            "id": "C024BE91L",
            "name": "fun",
            "created": 1360782804,
            "creator": "U024BE7LH",
            "is_archived": false,
            "is_member": false,
            "num_members": 6,
            "topic": {
                "value": "Fun times",
                "creator": "U024BE7LV",
                "last_set": 1369677212
            },
            "purpose": {
                "value": "This channel is for fun",
                "creator": "U024BE7LH",
                "last_set": 1360782804
            }
        }
    ]
}
'''

    def _mock_response(self, text):
        response = MagicMock()
        type(response).text = PropertyMock(return_value=self.DUMMY_RESPONSE)
        return response

    def test_without_slack_token(self):
        self.assertRaises(CommandError, call_command, 'retrieve_channels')

    @override_settings(SLACK_AUTH_TOKEN='testtoken')
    def test_create_room_correctly(self):
        with patch('requests.get') as requests_get:
            requests_get.return_value = self._mock_response(self.DUMMY_RESPONSE)
            self.assertEqual(Channel.objects.count(), 0)
            call_command('retrieve_channels')
            requests_get.assert_called_once_with('https://slack.com/api/channels.list?token=testtoken')
            self.assertEqual(Channel.objects.count(), 1)
            channel = Channel.objects.get()
            self.assertEqual(channel.channel_id, "C024BE91L")
            self.assertEqual(channel.name, "fun")
            self.assertEqual(channel.topic, 'Fun times')
            self.assertEqual(channel.purpose, 'This channel is for fun')
            self.assertFalse(channel.is_archived)
            self.assertEqual(channel.num_members, 6)
