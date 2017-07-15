from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey('auth.User', null=True)
    symbol = models.TextField(max_length=3)
    name = models.TextField(max_length=100)

    def __str__(self):
        return self.symbol


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    deal_id = models.TextField(max_length=40, blank=True, null=True, unique=True)
    client = models.ForeignKey('auth.User', null=True)
    created_time = models.DateTimeField(default=timezone.now)
    expected_clearing_date = models.DateTimeField(default=timezone.now)
    sell_currency = models.ForeignKey('bos.Currency', related_name="sell_currency", blank=False, null=False)
    buy_currency = models.ForeignKey('bos.Currency', related_name="buy_currency", blank=False, null=False)
    sell_amount = models.FloatField()
    buy_amount = models.FloatField()
    rate = models.FloatField()

    def __str__(self):
        return 'Trade {}'.format(self.deal_id)

    def save(self):
        super(Trade, self).save()
        if not self.deal_id:
            import uuid
            self.deal_id = 'TR{}'.format(str(uuid.uuid1()).replace('-', '')[:7].upper())
            super(Trade, self).save()


