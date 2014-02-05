from __future__ import absolute_import
from cStringIO import StringIO
from celery import shared_task
from linted.models import Repository
from gittle import Gittle, GittleAuth
from scanner.phpmd import Phpmd

import os
import tempfile
import shutil
import paramiko


@shared_task
def add(x, y):
    return x + y


@shared_task(bind=True)
def scan_repository(self, repository_id):
    repository = Repository.objects.get(pk=repository_id)
    if repository is not None:
        repository_keys = repository.repositorykey_set.all()

        auth_success = False
        for key_pair in repository_keys:
            try:
                working_dir = os.path.join(tempfile.gettempdir(), self.request.id)
                private_key_file = StringIO(key_pair.private_key)
                auth = GittleAuth(pkey=private_key_file)
                Gittle.clone(repository.clone_url, working_dir, auth=auth)

                phpmd_scanner = Phpmd(working_dir)
                phpmd_scanner.run()

                shutil.rmtree(working_dir)
                auth_success = True
            except paramiko.AuthenticationException:
                pass