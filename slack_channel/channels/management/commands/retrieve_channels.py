from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Update all channels status of your team'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Succeed'))
