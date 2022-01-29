from django.forms import ModelForm, widgets, HiddenInput

from .models import Repository
from .models import Branch



class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = ['name']

class EditBranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'is_default',]
        