from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from bos.choices import *
from django.contrib.auth.models import User
from django.db.models import Sum

class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    created_time = models.DateTimeField(default=timezone.now)
    autor = models.ForeignKey('auth.User', null=True)
    symbol = models.TextField(max_length=3)
    name = models.TextField(max_length=100)


class Trade(models.Model):
    id = models.AutoField(primary_key=True)
    deal_id = models.TextField(max_length=40, blank=True, null=True, unique=True)
    client = models.ForeignKey('auth.User', null=True)
    created_time = models.DateTimeField(default=timezone.now)
    expected_clearing_date = models.DateTimeField(default=timezone.now)
    sell_currency = models.ForeignKey('bos.Currency', related_name="sell_currency", blank=False, null=False)
    buy_currency = models.ForeignKey('bos.Currency', related_name="buy_currency", blank=False, null=False)
    sell_amount = models.FloatField()
    buy_amount = models.FloatField()
    rate = models.FloatField()


class CompanyPartner(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=40, null=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    # survey = models.OneToOneField('Survey')
    question_text = models.TextField(max_length=40)
    question_choice = models.ManyToManyField('Choice')
    point_reward = models.FloatField(null=True)

    @property
    def get_question_choices(self):
        return self.question_choice.all().values_list('choice_text', flat=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    id = models.AutoField(primary_key=True)
    # survey = models.OneToOneField('Survey')
    choice_text = models.TextField(max_length=40)
    choice_value = models.TextField(max_length=40)

    # question = models.OneToOneField('Question')

    def __str__(self):
        return self.choice_text


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(max_length=25, null=True)
    company = models.OneToOneField('CompanyPartner')
    questions = models.ManyToManyField('Question')
    profiles = models.ManyToManyField('Profile', null=True)

    @property
    def get_number_responses(self):
        number_user_respond = Response.objects.filter(question__survey=self).values_list('user__id').\
            distinct().count()
        return number_user_respond

    @property
    def get_points_rewarded(self):
        points_rewarded = Response.objects.filter(question__survey=self).aggregate(Sum('point_rewarded'))['point_rewarded__sum']
        return points_rewarded

    @property
    def get_profiles(self):
        return self.profiles.all()

    def __str__(self):
        return "%d %s" % (self.id, self.title)


class Response(models.Model):
    user = models.ForeignKey('auth.User', null=True)
    response_text = models.TextField(max_length=40)
    question = models.OneToOneField('Question')
    point_rewarded = models.FloatField(null=True, default=10)
    response_date = models.DateTimeField(default=timezone.now)

    @property
    def get_company(self):
        return self.question.survey_set.first().company

    def __str__(self):
        return self.response_text


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(choices=STATUS_CHOICES,
                                 default=2)

    gender = models.IntegerField(choices=GENDER_CHOICES,
                                 default=1)

    level_study = models.IntegerField(choices=LEVEL_STUDY_CHOICES,
                                      default=1)
    etnicity = models.IntegerField(choices=ETNICITY_CHOICES,
                                   default=1)
    birth_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey('auth.User', null=True, blank=True)
    #surveys = models.ManyToManyField('Profile', blank=True, null=True)

    def __str__(self):
        return self.get_gender_display() + ' ' + self.get_etnicity_display() + \
               ' ' + self.get_level_study_display() + ' ' + self.get_status_display()