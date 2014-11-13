from django import forms

from order.models import OrderItem, Customer


class OrderForm(forms.Form):
    tip = forms.DecimalField(max_digits=6, decimal_places=2, required=True)


class CancellationReasonForm(forms.Form):
    cancellation_reason = forms.CharField(max_length=500, required=False)


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ('item', 'quantity')


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'phone')
