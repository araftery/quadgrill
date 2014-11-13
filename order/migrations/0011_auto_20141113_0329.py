# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_order_cancellation_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cancellation_message',
        ),
        migrations.AddField(
            model_name='order',
            name='cancellation_reason',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
