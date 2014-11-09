from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    cc_number = models.CharField(max_length=20, null=True, blank=True)
    phone = PhoneNumberField()

    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def __unicode__(self):
        return self.full_name


class OrderItem(models.Model):
    item = models.ForeignKey('menu.Item')
    order = models.ForeignKey('order.Order')
    quantity = models.IntegerField(default=1)

    def __unicode__(self):
        return u'{} {}'.format(self.quantity, self.item.name)


class Order(models.Model):

    PAYMENT_CHOICES = [
        ('Crimson Cash', 'Crimson Cash',),
        ('Board Plus', 'Board Plus',),
        ('Cash', 'Cash',),
    ]

    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES, default='Crimson Cash')
    time = models.DateTimeField(auto_now=True)
    tip = models.DecimalField(max_digits=6, decimal_places=2)
    customer = models.ForeignKey(Customer)
    accepted = models.BooleanField(default=False)
    time_accepted = models.DateTimeField(null=True, blank=True)
    time_estimate = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    time_completed = models.DateTimeField(null=True, blank=True)

    def add_item(self, item, quantity=1):
        try:
            current_item = self.orderitem_set.get(item=item)
            current_item.quantity += quantity
            current_item.save()
        except ObjectDoesNotExist:
            OrderItem.objects.create(item=item, quantity=quantity, order=self)

    @property
    def total(self):
        total = self.tip
        for order_item in self.orderitem_set.all():
            total += order_item.quantity * order_item.item.price
        return total

    @property
    def time_to_complete(self):
        delta = (self.time_completed - self.time_accepted)
        seconds = float(delta.seconds)
        minutes = round(seconds/60, 0)
        return '{} minutes'.format(int(minutes))

    def __unicode__(self):
        return u"{}'s order for ${} at {}".format(
            self.customer.full_name,
            self.total,
            self.time,
        )
