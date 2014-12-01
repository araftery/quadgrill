import datetime
import json

from django.views.generic import TemplateView, View
from django.utils import timezone

from braces.views import JSONResponseMixin
from core.utils import send_text

from order.models import Order
from order.forms import CancellationReasonForm


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

        send_text('accepted', unicode(order.customer.phone), {'order': order})

        return self.render_json_response({'status': 'success'})


class CancelOrder(JSONResponseMixin, View):
    def post(self, request, **kwargs):
        generic_error_response = self.render_json_response({'status': 'error', 'errors': {'non_field_errors': 'Invalid submission.'}})

        cancel_verb = kwargs.get('cancel_verb')

        order_pk = request.POST.get('order')
        if order_pk is None:
            return generic_error_response

        try:
            order = Order.objects.get(pk=order_pk, completed=False, canceled=False)
        except Order.DoesNotExist:
            return generic_error_response

        cancellation_reason_form = CancellationReasonForm(data={'cancellation_reason': request.POST.get('cancellation_reason')})

        if cancellation_reason_form.is_valid():
            cancellation_reason = cancellation_reason_form.cleaned_data.get('cancellation_reason')
        else:
            cancellation_reason = None

        order.cancellation_reason = cancellation_reason
        order.canceled = True
        order.save()

        send_text('cancel', unicode(order.customer.phone), {'order': order, 'verb': cancel_verb, 'reason': cancellation_reason})

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

        send_text('complete', unicode(order.customer.phone), {'order': order})

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
                'payment_type': order.payment_type_display,
                'time': order.time.strftime('%m/%d %I:%M %p'),
                'customer_name': order.customer.full_name,
                'tip': order.tip,
                'total': order.total,
                'order_items': order_items,
            })

        return self.render_json_response({'status': 'success', 'orders': payload})
