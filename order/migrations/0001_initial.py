# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_name', models.CharField(max_length=200)),
                ('payment_type', models.CharField(max_length=100, choices=[(b'Crimson Cash', b'Crimson Cash'), (b'Board Plus', b'Board Plus'), (b'Cash', b'Cash')])),
                ('cc_number', models.CharField(max_length=20, null=True, blank=True)),
                ('customer_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('time', models.DateTimeField(auto_now=True)),
                ('tip', models.DecimalField(max_digits=6, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(to='menu.Item')),
                ('order', models.ForeignKey(to='order.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
