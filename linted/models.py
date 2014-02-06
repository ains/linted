from django.db import models
from django.contrib.auth import get_user_model
import uuid


class Repository(models.Model):
    name = models.CharField(max_length=64)
    uuid = models.CharField(max_length=40, unique=True, default=lambda: str(uuid.uuid4()))
    owner = models.ForeignKey(get_user_model())
    clone_url = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Repositories"


class RepositoryUser(models.Model):
    repository = models.ForeignKey(Repository)
    user = models.ForeignKey(get_user_model())


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


class RepositoryScanner(models.Model):
    repository = models.ForeignKey(Repository)
    scanner = models.ForeignKey(Scanner)

    #Scanner settings are encoded as JSON
    settings = models.TextField()


class RepositoryScan(models.Model):
    repository = models.ForeignKey(Repository)

    created_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True)


class ErrorGroup(models.Model):
    parent = models.ForeignKey("ErrorGroup", null=True)
    
    name = models.TextField(max_length=512)
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