from unittest.mock import patch
from django.core.management import call_command, CommandError
from django.test import TestCase


class RetriveChannelsCommandTestCase(TestCase):
    def test_without_slack_token(self):
        self.assertRaises(CommandError, call_command, 'retrieve_channels')
