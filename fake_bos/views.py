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
    print responses
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

def register_response(request):
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
