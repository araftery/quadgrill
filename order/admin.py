from django.contrib import admin

from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order

admin.site.register(Order, OrderAdmin)
