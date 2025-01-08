from django import forms

class PostSearchForm(forms.Form):
    query = forms.CharField(label='検索', max_length=100, required=False)