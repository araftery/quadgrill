from django.views.generic import ListView

from menu.models import Item


class MenuHome(ListView):
    queryset = Item.objects.filter(active=True).order_by('name')
    template_name = 'menu/home.html'
