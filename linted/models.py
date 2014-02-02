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


class Linter(models.Model):
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=8)
    language = models.ForeignKey(Language)


class RepositoryLinter(models.Model):
    repository = models.ForeignKey(Repository)
    linter = models.ForeignKey(Linter)
    settings = models.TextField() #Linter settings are encoded as JSON