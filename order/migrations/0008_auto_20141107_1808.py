# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_time_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='fulfilled',
            new_name='completed',
        ),
    ]
