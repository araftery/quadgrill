# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20141107_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time_accepted',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
