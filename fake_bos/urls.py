"""fake_bos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from fake_bos import views

app_name = 'fake_bos'

urlpatterns = [
    url(r'^$', views.login_view, name='login_view'),
    url(r'^admin/', admin.site.urls),
    url(r'^index$', views.index, name='index'),
    url(r'^login$', views.login_view, name='login_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^delete/(?P<identifier>[0-9]+)/$', views.delete, name='delete'),
    url(r'^new_trade$', views.new_trade, name='new_trade'),
    url(r'^ajax/autocomplete_buy_currency/$', views.autocomplete_buy_currency, name='autocomplete_buy_currency'),
    url(r'^ajax/autocomplete_sell_currency/$', views.autocomplete_sell_currency, name='autocomplete_sell_currency'),
    url(r'^ajax/get_rate/$', views.get_rate, name='autocomplete_sell_currency'),

]
