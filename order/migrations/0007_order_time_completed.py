# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time_completed',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
