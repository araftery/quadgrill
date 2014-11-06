from django import forms
from django.contrib import admin

from menu.models import Item


class ItemAdminForm(forms.ModelForm):
    description = forms.CharField(max_length=2000, widget=forms.Textarea)

    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'active')


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = ('name', 'description', 'price', 'active')
    ordering = ('-active', 'name', 'price')
    search_fields = ('name', 'active')


admin.site.register(Item, ItemAdmin)
