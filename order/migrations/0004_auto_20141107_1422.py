# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20141106_0227'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time_accepted',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 7, 19, 22, 0, 934489, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='time_estimate',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(default=b'Crimson Cash', max_length=100, choices=[(b'Crimson Cash', b'Crimson Cash'), (b'Board Plus', b'Board Plus'), (b'Cash', b'Cash')]),
            preserve_default=True,
        ),
    ]
