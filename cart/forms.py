from django import forms 


class AddCardForm(forms.Form):
    count = forms.IntegerField(min_value=1, max_value=99)
    