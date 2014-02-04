from django.contrib import admin
from linted.models import Repository, Language, Linter, RepositoryLinter, RepositoryKey, ErrorGroup


admin.site.register(Repository)
admin.site.register(Language)
admin.site.register(Linter)
admin.site.register(RepositoryLinter)
admin.site.register(RepositoryKey)
admin.site.register(ErrorGroup)