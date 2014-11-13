# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_order_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cancellation_message',
            field=models.CharField(max_length=2000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
