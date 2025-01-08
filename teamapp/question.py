from django import forms

class PoatSearchForm(forms.Form):
    query = forms.CharField(label='検索', max_length=100, required=False)