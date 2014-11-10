# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20141107_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='key',
            field=models.CharField(max_length=64, null=True, blank=True),
            preserve_default=True,
        ),
    ]
