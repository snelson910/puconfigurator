from django import forms


class CustNumberForm(forms.Form):
    custNum = forms.CharField(max_length=7)
