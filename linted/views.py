from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.core.urlresolvers import reverse

from linted.tasks import add, scan_repository
from linted.models import Repository, RepositoryKey
from linted.forms import RepositoryForm

from Crypto.PublicKey import RSA


def index(request):
    add.delay(1, 100)
    return HttpResponse("Hello, world. You're at the polls index.")


class ViewRepository(DetailView):
    model = Repository
    template_name = 'view_repository.html'


def run_scan(request, pk):
    repository = get_object_or_404(Repository, pk=pk)

    scan_repository.delay(repository.id)

    return HttpResponse("Queued repo scan")


def create_repository(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repo_name = form.cleaned_data['name']
            repo_clone_url = form.cleaned_data['clone_url']

            #Generate keypair for repo
            keypair = RSA.generate(2048)
            private_key = keypair.exportKey('PEM')
            public_key = keypair.publickey().exportKey('OpenSSH')

            repository = Repository()
            repository.name = repo_name
            repository.clone_url = repo_clone_url
            repository.save()

            repository_key = RepositoryKey()
            repository_key.repository = repository
            repository_key.private_key = private_key
            repository_key.public_key = public_key
            repository_key.save()

            return HttpResponseRedirect(reverse('view_repository', args=(repository.id,)))
    else:
        form = RepositoryForm()

    return render(request, 'create_repository.html', {
        'form': form,
    })