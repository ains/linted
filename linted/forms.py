from django import forms
from linted.models import Repository, RepositoryScanner


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ['name', 'clone_url']


class RepositoryScannerForm(forms.ModelForm):
    class Meta:
        model = RepositoryScanner
        fields = ['scanner']