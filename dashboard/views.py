import datetime
import json
import pytz

from django.conf import settings
from django.views.generic import TemplateView, View
from django.utils import timezone

from braces.views import JSONResponseMixin

from order.models import Order


class OrdersDashboard(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersDashboard, self).get_context_data(**kwargs)
        context['orders_in_progress'] = Order.objects.filter(accepted=True, completed=False, canceled=False).order_by('time')
        context['incoming_orders'] = Order.objects.filter(accepted=False, completed=False, canceled=False).order_by('time')
        fifteen_minutes_ago = timezone.now() - datetime.timedelta(seconds=60 * 15)
        context['recently_completed_orders'] = Order.objects.filter(completed=True, time_completed__gte=fifteen_minutes_ago).order_by('-time_completed')[:10]
        return context


class AcceptOrder(JSONResponseMixin, View):
    def post(self, request):
        generic_error_response = self.render_json_response({'status': 'error', 'errors': {'non_field_errors': 'Invalid submission.'}})

        order_pk = request.POST.get('order')
        if order_pk is None:
            return generic_error_response

        minutes_estimate = request.POST.get('minutes_estimate')
        try:
            minutes_estimate = int(minutes_estimate)
        except:
            return self.render_json_response({'status': 'error', 'errors': {'minutes_estimate': 'Invalid value.'}})

        if not minutes_estimate or minutes_estimate <= 0:
            return self.render_json_response({'status': 'error', 'errors': {'minutes_estimate': 'Invalid value.'}})

        try:
            order = Order.objects.get(pk=order_pk, accepted=False, completed=False, canceled=False)
        except Order.DoesNotExist:
            return generic_error_response

        order.accepted = True
        order.time_estimate = minutes_estimate
        order.time_accepted = timezone.now()
        order.save()

        # TODO: send text logic here

        return self.render_json_response({'status': 'success'})


class CancelOrder(JSONResponseMixin, View):
    def post(self, request, **kwargs):
        generic_error_response = self.render_json_response({'status': 'error', 'errors': {'non_field_errors': 'Invalid submission.'}})

        cancel_type = kwargs.get('cancel_type')

        order_pk = request.POST.get('order')
        if order_pk is None:
            return generic_error_response

        try:
            order = Order.objects.get(pk=order_pk, completed=False, canceled=False)
        except Order.DoesNotExist:
            return generic_error_response

        order.canceled = True
        order.save()

        # TODO: send text logic here

        return self.render_json_response({'status': 'success'})


class CompleteOrder(JSONResponseMixin, View):
    def post(self, request, **kwargs):
        generic_error_response = self.render_json_response({'status': 'error', 'errors': {'non_field_errors': 'Invalid submission.'}})

        order_pk = request.POST.get('order')
        if order_pk is None:
            return generic_error_response

        try:
            order = Order.objects.get(pk=order_pk, accepted=True, completed=False, canceled=False)
        except Order.DoesNotExist:
            return generic_error_response

        order.completed = True
        order.time_completed = timezone.now()
        order.save()

        # TODO: send text logic here

        return self.render_json_response({'status': 'success', 'pk': order.pk, 'customer_name': order.customer.full_name, 'total': order.total, 'time_taken': order.time_to_complete})


class Poll(JSONResponseMixin, View):
    def post(self, request):
        generic_error_response = self.render_json_response({'status': 'error'})

        try:
            loaded = json.loads(request.POST.get('loaded'))
        except ValueError:
            return generic_error_response

        if loaded is None:
            return generic_error_response

        orders = Order.objects.filter(accepted=False, completed=False, canceled=False).exclude(pk__in=loaded).order_by('time')

        payload = []
        for order in orders:
            order_items = {}
            for order_item in order.orderitem_set.all():
                order_items[order_item.item.name] = order_item.quantity

            payload.append({
                'pk': order.pk,
                'payment_type': order.payment_type,
                'time': order.time.strftime('%m/%d %I:%M %p'),
                'customer_name': order.customer.full_name,
                'tip': order.tip,
                'total': order.total,
                'order_items': order_items,
            })

        return self.render_json_response({'status': 'success', 'orders': payload})
