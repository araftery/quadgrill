import hashlib
import json

from django.views.generic import ListView, View
from django.http import Http404
from django.shortcuts import render

from braces.views import JSONResponseMixin

from menu.models import Item
from order.models import Order, Customer
from order.forms import OrderForm, OrderItemForm, CustomerForm


class OrderHome(ListView):
    queryset = Item.objects.filter(active=True).order_by('name')
    template_name = 'order/home.html'


class SubmitOrder(JSONResponseMixin, View):
    def post(self, request):
        generic_error_response = self.render_json_response({'status': 'error', 'errors': {'non_field_errors': 'Invalid submission.'}})
        try:
            data = json.loads(request.POST.get('data'))
            tip = data.get('tip')
            items = data.get('items')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            phone_number = data.get('phone_number')
            cc_number = data.get('crimsoncash')
        except (IndexError, ValueError):
            return generic_error_response

        if any(i is None for i in [tip, items, first_name, last_name, phone_number, cc_number]):
            return generic_error_response

        order_form = OrderForm(data={'tip': tip})
        if not order_form.is_valid():
            return self.render_json_response({'status': 'error', 'errors': order_form.errors})
        else:
            tip = order_form.cleaned_data.get('tip')

        order_items = []
        for pk, quantity in items.iteritems():
            order_item_form = OrderItemForm(data={'item': pk, 'quantity': quantity})
            if not order_item_form.is_valid():
                return self.render_json_response({'status': 'error', 'errors': order_item_form.errors})
            else:
                quantity = order_item_form.cleaned_data.get('quantity')
                item = order_item_form.cleaned_data.get('item')
                if quantity > 0:
                    order_items.append((item, quantity))

        # add the phone number country code if necessary
        if not phone_number[:1] == '+' and not phone_number[:1] == '1':
            phone_number = u'+1{}'.format(phone_number)
        elif not phone_number[:1] == '+':
            phone_number = u'+{}'.format(phone_number)

        customer_form = CustomerForm(data={'first_name': first_name, 'last_name': last_name, 'phone': phone_number, 'cc_number': cc_number})
        if not customer_form.is_valid():
            return self.render_json_response({'status': 'error', 'errors': customer_form.errors})

        # if they submitted an order with all quantities = 0
        if not order_items:
            return generic_error_response

        first_name = customer_form.cleaned_data.get('first_name')
        last_name = customer_form.cleaned_data.get('last_name')
        phone_number = customer_form.cleaned_data.get('phone')
        cc_number = customer_form.cleaned_data.get('cc_number')

        customer, created = Customer.objects.get_or_create(
            first_name=first_name,
            last_name=last_name,
            phone=phone_number,
            cc_number=cc_number,
        )

        order = Order.objects.create(
            customer=customer,
            tip=tip,
        )

        m = hashlib.md5()
        m.update('{}{}'.format(order.customer.last_name, order.pk))
        key = m.hexdigest()
        order.key = key
        order.save()

        for item, quantity in order_items:
            order.add_item(item, quantity)

        return self.render_json_response({'status': 'success', 'key': order.key})


class TrackOrder(View):
    def get(self, request, key):
        try:
            order = Order.objects.get(key=key)
        except Order.DoesNotExist:
            raise Http404

        return render(request, 'order/track.html', {'order': order})
