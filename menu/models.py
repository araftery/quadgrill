from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, null=True, blank=True)
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __unicode__(self):
        return self.name
