from django import forms
from django.forms import ModelForm

import delve.models as models
TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]    
class Upload_Form(ModelForm, forms.Form, forms.ChoiceField):
    
    # experiment_data = forms.FileField(required=False)

    class Meta:
        model = models.Combo
        # stephanie duham
        # Miss Duham
        
        # Method 1 of adding html attributes
        name = forms.CharField(widget=forms.TextInput(attrs={'class': 'mt-4 d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm'}))
        # 

        fields = ['name','drug_1', 'drug_2', 'CellLine', 'Scientist']
        
        # Method 2 of adding html attributes
        # widgets = {
        #     'drug_1': Textarea(attrs={'class': 'mt-4 d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm'}),
        # }
        # 

class Calc_Form(forms.Form):
    text = forms.CharField()
    experiment_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Experiment Name'}))
