import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from bos.models import Trade, Profile, Response, Survey, Question, CompanyPartner
from django.contrib.auth.models import User


def logout_view(request):
    logout(request)
    return redirect(login_view)


@login_required
def index(request):
    from django.db.models import Sum
    from django.contrib.auth.models import Group
    responses = Response.objects.filter(user=request.user).order_by('-response_date')
    acumulated = responses.aggregate(Sum('point_rewarded'))
    isCompany = Group.objects.get_or_create(name='Company')[0] in request.user.groups.all()
    if isCompany:
        surveys = Survey.objects.filter(company=CompanyPartner.objects.first())
    else:
        surveys = None
    return render(request, 'index.html', {'responses': responses,
                                          'isCompany': isCompany,
                                          'surveys': surveys,
                                          'user_acumulated': acumulated['point_rewarded__sum']})


@login_required
def view_survey(request, survey_id):
    questions = Survey.objects.get(pk=survey_id).questions.all()
    responses = Response.objects.filter(question__in=questions)
    return render(request, 'view_survey.html', {'responses': responses,
                                                'questions': questions})


def register_response(request, id_user, id_question, answer):
    try:
        print (id_user, id_question, answer)
        response = Response.objects.create(user=User.objects.get(pk=id_user), response_text=answer,
                                           question=Question.objects.get(pk=id_question))
    except:
        import traceback
        return render(request, 'error.html', {'error_trace': traceback.format_exc()})
    return render(request, 'confirmation.html')


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


# @login_required
# def new_trade(request):
#     from fake_bos.forms import RegistrationForm
#     if request.method == 'GET':
#         form = RegistrationForm()
#         return render(request, 'new_trade.html', {'form': form})
#     else:
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             trade = Trade()
#             trade.created_time = datetime.datetime.now()
#             trade.expected_clearing_date = form.cleaned_data['expected_clearing_date']
#             trade.sell_currency = Currency.objects.get(
#                 symbol=form.cleaned_data['sell_currency'])
#             trade.buy_currency = Currency.objects.get(
#                 symbol=form.cleaned_data['buy_currency'])
#             trade.buy_amount = form.cleaned_data['buy_amount']
#             trade.sell_amount = form.cleaned_data['sell_amount']
#             trade.rate = form.cleaned_data['client_rate']
#             trade.client = request.user
#             trade.save()
#             return redirect(index)
#         else:
#             return render(request, 'new_trade.html', {'form': form})


def register_view(request):
    from fake_bos.forms import RegistrationForm
    if request.method == 'GET':
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})
    else:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            profile = Profile()
            # trade.created_time = datetime.datetime.now()
            profile.birth_date = form.cleaned_data['birth_date']
            profile.gender = form.cleaned_data['gender']
            profile.level_study = form.cleaned_data['level_study']
            profile.name = form.cleaned_data['name']
            profile.status = form.cleaned_data['status']
            email = form.cleaned_data['email']
            password = User.objects.make_random_password()
            user = User.objects.create(username=email,
                                       email=email, password=password)
            profile.user = user
            profile.save()

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
    js = requests.get('http://api.fixer.io/latest?base={}'.format(request.GET.get('sell_currency', ''))).text
    d = json.loads(js)
    data = {
        'rate': d['rates'][request.GET.get('buy_currency', '')],
    }
    return JsonResponse(data)
