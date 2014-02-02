from django.forms import ModelForm
from linted.models import Repository


class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'clone_url']