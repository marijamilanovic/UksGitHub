from django.forms import ModelForm

from .models import Repository
from .models import Branch



class BranchForm(ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'repository']