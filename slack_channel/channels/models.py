from django.db import models
from django.utils.translation import ugettext_lazy as _


class Channel(models.Model):
    channel_id = models.CharField(_('ID'), max_length=16, unique=True)
    name = models.CharField(_('Name'), max_length=64)
    created_at = models.DateField(_('Created at'))
    is_archived = models.BooleanField(_('Is archived'), default=False)
    num_members = models.PositiveIntegerField(_('Number of members'), default=0)
    topic = models.CharField(_('Topic'), max_length=1024)
    purpose = models.CharField(_('Purpose'), max_length=1024)

    fetched_at = models.DateField(_('Fetched at'), auto_now=True)

    class Meta:
        verbose_name = _('Channel')
        ordering = ('is_archived', 'name')
