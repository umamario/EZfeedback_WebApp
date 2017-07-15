from django import forms
from django.core.exceptions import ValidationError
from bos.models import Trade, Currency


class TradeForm(forms.ModelForm):
    expected_clearing_date = forms.DateField(required=True, widget=forms.DateInput(format='%d/%m/%Y', attrs={'class':'datepicker'}),
                                             input_formats=('%d/%m/%Y',), label='Value Date')
    buy_amount = forms.DecimalField(max_digits=19, decimal_places=4, initial='0.0', label='Buy Amount',
                                    widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    sell_amount = forms.DecimalField(max_digits=19, decimal_places=4, initial='0.0', label='Sell Amount',
                                     widget=forms.TextInput(attrs={'onchange': 'setBuyAmount()'}))
    client_rate = forms.DecimalField(max_digits=19, decimal_places=6, label='Rate',
                                     widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    sell_currency = forms.CharField(required=True, label='Sell Currency',
                                    widget=forms.TextInput(attrs={'maxlength': 3, 'onchange': 'setRate()'}))
    buy_currency = forms.CharField(required=True, label='Buy Currency',
                                   widget=forms.TextInput(attrs={'maxlength': 3, 'onchange': 'setRate()'}))

    def clean_sell_currency(self):
        sc = self.cleaned_data['sell_currency']
        if not Currency.objects.filter(symbol=sc).exists():
            raise ValidationError("The currency {} has not been created yet in our system".format(sc))
        return sc

    def clean_buy_currency(self):
        bc = self.cleaned_data['buy_currency']
        if not Currency.objects.filter(symbol=bc).exists():
            raise ValidationError("The currency {} has not been created yet in our system".format(bc))
        return bc

    class Meta:
        model = Trade
        fields = (
            'sell_amount',
            'buy_amount',
            'expected_clearing_date',
            'client_rate',
        )
