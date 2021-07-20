from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
import delve.models as models
TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]    
class Combos_Form(ModelForm, forms.Form, forms.ChoiceField):
    drug_1 = forms.FileField(required=False)
    drug_2 = forms.FileField(required=False)
    combo = forms.FileField(required=False)
    
    class Meta:
        model = models.Combo
        fields = ['drug_1', 'drug_2', 'CellLine', 'Scientist']

        
class Calc_Form(forms.Form):
    text = forms.CharField()
    experiment_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Experiment Name'}))
