from django import forms
from django.core.exceptions import ValidationError
from bos.models import Profile
from bos.choices import *


class RegistrationForm(forms.ModelForm):
    birth_date = forms.DateField(required=True,
                                 widget=forms.DateInput(format='%m/%d/%Y', attrs={'class': 'datepicker'}),
                                 input_formats=('%m/%d/%Y',), label='Birth Date')
    ethnicity = forms.ChoiceField(choices=ETNICITY_CHOICES, label="ethnicity", initial='',
                                  widget=forms.Select(), required=True)
    level_study = forms.ChoiceField(choices=LEVEL_STUDY_CHOICES, label="level_study", initial='',
                                    widget=forms.Select(), required=True)
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="status", initial='',
                               widget=forms.Select(), required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="gender", initial='',
                               widget=forms.Select(), required=True)
    name = forms.CharField(required=True, label='Name')
    email = forms.EmailField(required=True, label='Email')


    # def clean_sell_currency(self):
    #     sc = self.cleaned_data['sell_currency']
    #     if not Currency.objects.filter(symbol=sc).exists():
    #         raise ValidationError("The currency {} has not been created yet in our system".format(sc))
    #     return sc
    #
    # def clean_buy_currency(self):
    #     bc = self.cleaned_data['buy_currency']
    #     if not Currency.objects.filter(symbol=bc).exists():
    #         raise ValidationError("The currency {} has not been created yet in our system".format(bc))
    #     return bc

    class Meta:
        model = Profile
        fields = (
            'ethnicity',
            'gender',
            'level_study',
            'name',
            'email',
            'status',
            'birth_date',
        )
