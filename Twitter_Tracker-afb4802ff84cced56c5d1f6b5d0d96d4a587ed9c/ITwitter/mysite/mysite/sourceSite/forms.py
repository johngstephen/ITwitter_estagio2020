from django import forms


class searchForm(forms.Form):
     keyword = forms.CharField(label='Texto de Pesquisa', widget=forms.TextInput(
          attrs = {
          'width' : '100%',
          }
     ))
