# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20141107_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='canceled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
