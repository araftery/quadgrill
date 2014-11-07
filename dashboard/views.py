from django.views.generic import TemplateView, View
from django.utils import timezone

from braces.views import JSONResponseMixin

from order.models import Order


class OrdersDashboard(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super(OrdersDashboard, self).get_context_data(**kwargs)
        context['orders_in_progress'] = Order.objects.filter(accepted=True, fulfilled=False, canceled=False).order_by('time')
        context['incoming_orders'] = Order.objects.filter(accepted=False, fulfilled=False, canceled=False).order_by('time')
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
            order = Order.objects.get(pk=order_pk, accepted=False, fulfilled=False, canceled=False)
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
            order = Order.objects.get(pk=order_pk, fulfilled=False, canceled=False)
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
            order = Order.objects.get(pk=order_pk, accepted=True, fulfilled=False, canceled=False)
        except Order.DoesNotExist:
            return generic_error_response

        order.fulfilled = True
        order.save()

        # TODO: send text logic here

        return self.render_json_response({'status': 'success'})
