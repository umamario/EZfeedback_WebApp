import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from bos.models import Trade, Currency


def logout_view(request):
    logout(request)
    return redirect(login_view)


@login_required
def index(request):
    trades = Trade.objects.filter(client=request.user).order_by('-created_time')
    return render(request, 'index.html', {'trades': trades})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('user', '')
        password = request.POST.get('contrasenia', '')
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'login.html', {'login_incorrect': True})
        else:
            login(request, user)
            return redirect(index)

    if request.user.is_authenticated and not request.user.is_anonymous():
        return redirect(index)
    else:
        return render(request, 'login.html', {'login_incorrect': False})


@login_required
def delete(request, identifier):
    trade = get_object_or_404(Trade, id=identifier)
    trade.delete()
    return redirect(index)


@login_required
def new_trade(request):
    from fake_bos.forms import TradeForm
    if request.method == 'GET':
        form = TradeForm()
        return render(request, 'new_trade.html', {'form': form})
    else:
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = Trade()
            trade.created_time = datetime.datetime.now()
            trade.expected_clearing_date = form.cleaned_data['expected_clearing_date']
            trade.sell_currency = Currency.objects.get(
                symbol=form.cleaned_data['sell_currency'])
            trade.buy_currency = Currency.objects.get(
                symbol=form.cleaned_data['buy_currency'])
            trade.buy_amount = form.cleaned_data['buy_amount']
            trade.sell_amount = form.cleaned_data['sell_amount']
            trade.rate = form.cleaned_data['client_rate']
            trade.client = request.user
            trade.save()
            return redirect(index)
        else:
            return render(request, 'new_trade.html', {'form': form})


def autocomplete_sell_currency(request):
    """
    View used to autocomplete the buy currency field with the corresponding currency symbol
    :param request:
    :return: Json response with the matched symbols
    """
    from django.http import JsonResponse
    if request.is_ajax():
        queryset = Currency.objects.filter(symbol__startswith=request.GET.get('sell_currency', ''))
        list = []
        for i in queryset:
            list.append(i.symbol)
        data = {
            'list': list,
        }
        return JsonResponse(data)


def autocomplete_buy_currency(request):
    """
    View used to autocomplete the buy currency field with the corresponding currency symbol
    :param request:
    :return: Json response with the matched symbols
    """
    from django.http import JsonResponse
    if request.is_ajax():
        queryset = Currency.objects.filter(symbol__startswith=request.GET.get('buy_currency', ''))
        list = []
        for i in queryset:
            list.append(i.symbol)
        data = {
            'list': list,
        }
        return JsonResponse(data)


def get_rate(request):
    """
    View to get the current rates from api.fixer.io
    :param request:
    :return: Json with the current rate
    """
    from django.http import JsonResponse
    import requests
    import json
    js = requests.get('http://api.fixer.io/latest?base={}'.format(request.GET.get('sell_currency',''))).text
    d = json.loads(js)
    data = {
        'rate': d['rates'][request.GET.get('buy_currency', '')],
    }
    return JsonResponse(data)