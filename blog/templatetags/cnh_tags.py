import requests
from django import template
from blog.forms import SubscribeForm
from blog.models import *

register = template.Library()


@register.inclusion_tag("cnh/tags/subscribe_form.html")
def subscribe_form():
    return {"subscribe_form": SubscribeForm()}


@register.simple_tag()
def get_last_news():
    return PostModel.objects.order_by('-datetime_create')[:5].select_related('author').prefetch_related('tag')


@register.simple_tag()
def get_authors():
    return AuthorModel.objects.all().order_by('-staff')


@register.simple_tag()
def get_category():
    return CategoryTagModel.objects.all().prefetch_related('tag')


@register.simple_tag()
def get_price():
    url = 'https://api.exmo.com/v1.1/trades'
    r = requests.post(url, data={"pair": "BTC_RUB,BTC_USD,ETH_USD,ETH_RUB"}).json()
    price = {'btc_usd': r['BTC_USD'][0]['price'].split('.', 1)[0],
             'btc_rub': r['BTC_RUB'][0]['price'].split('.', 1)[0],
             'eth_usd': r['ETH_USD'][0]['price'].split('.', 1)[0],
             'eth_rub': r['ETH_RUB'][0]['price'].split('.', 1)[0]}
    return price
