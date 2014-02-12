import json
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings

from linted.tasks import add, scan_repository
from linted.models import Repository, RepositoryKey
from linted.forms import RepositoryForm

from Crypto.PublicKey import RSA


def index(request):
    add.delay(1, 100)
    return HttpResponse("Hello, world. You're at the polls index.")


def repository_list(request):
    repositories = Repository.objects.all()
    return render(request, 'repository_list.html', {'repository_list': repositories})


def view_repoository(request, uuid):
    repository = get_object_or_404(Repository, uuid=uuid)
    scan_url = request.build_absolute_uri(reverse('scan_repository', args=(repository.uuid,)))

    render_data = {
        'repository': repository,
        'scan_url': scan_url
    }

    return render(request, 'view_repository.html', render_data)


def run_scan(request, uuid):
    repository = get_object_or_404(Repository, uuid=uuid)

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
            repository.owner = request.user
            repository.save()

            repository_key = RepositoryKey()
            repository_key.repository = repository
            repository_key.private_key = private_key
            repository_key.public_key = public_key
            repository_key.save()

            return HttpResponseRedirect(reverse('view_repository', args=(repository.uuid,)))
    else:
        form = RepositoryForm()

    return render(request, 'create_repository.html', {
        'form': form,
    })


def scanner_settings(request, uuid):
    repository = Repository.objects.get(uuid=uuid)
    ruleset_file = os.path.join(settings.SCANNER_DIR, 'phpmd', 'ruleset.json')

    with open(ruleset_file) as f:
        scanner_rules = json.loads(f.read())

        if request.method == 'POST':
            for field_name, value in request.POST.items():
                if '/' in field_name:
                    ruleset, rule, property = field_name.split('/')
                    print field_name
                    print(ruleset, rule, property)

            return HttpResponse("ok")
        else:
            return render(request, 'scanner_settings.html', {
                "repository": repository,
                "rules": scanner_rules
                })