from django.forms import ModelForm

from .models import Commit



class CommitForm(ModelForm):
    class Meta:
        model = Commit
        fields = ['message']

