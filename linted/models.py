import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

from scanners.settings import ScannerSettings


class Repository(models.Model):
    name = models.CharField(max_length=64)
    uuid = models.CharField(max_length=40, unique=True, default=lambda: str(uuid.uuid4()))
    owner = models.ForeignKey(get_user_model(), related_name='owned_repository')
    users = models.ManyToManyField(get_user_model())
    clone_url = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Repositories"


class RepositoryKey(models.Model):
    repository = models.ForeignKey(Repository)
    private_key = models.TextField()
    public_key = models.TextField()


class Language(models.Model):
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=8)

    def __unicode__(self):
        return self.name


class Scanner(models.Model):
    name = models.CharField(max_length=256, unique=True)
    short_name = models.CharField(max_length=8, unique=True)
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return self.name

    @property
    def namespaced_name(self):
        return "{}/{}".format(self.language.short_name, self.short_name)

    @property
    def scanner_class(self):
        return settings.ENABLED_SCANNERS.get(self.namespaced_name)


class RepositoryScanner(models.Model):
    repository = models.ForeignKey(Repository)
    scanner = models.ForeignKey(Scanner)

    #Scanner settings are encoded as JSON
    settings = models.TextField()

    def get_settings(self):
        return ScannerSettings(self)

    def __unicode__(self):
        return "{}/{}".format(self.repository, self.scanner)

    class Meta:
        unique_together = ('repository', 'scanner')


class RepositoryScan(models.Model):
    uuid = models.CharField(max_length=40, unique=True, default=lambda: str(uuid.uuid4()))
    repository = models.ForeignKey(Repository)

    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True)


class ErrorGroup(models.Model):
    parent = models.ForeignKey("ErrorGroup", null=True)

    name = models.TextField(max_length=512, unique=True)
    #Formatted as Markdown documents
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ScanViolation(models.Model):
    scan = models.ForeignKey(RepositoryScan)
    scanner = models.ForeignKey(Scanner)
    previous_error = models.ForeignKey("ScanViolation", null=True)
    error_group = models.ForeignKey(ErrorGroup)

    file = models.TextField(max_length=256)
    start_line = models.IntegerField()
    end_line = models.IntegerField()
    snippet = models.TextField()
    message = models.TextField()