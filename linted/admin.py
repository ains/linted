from django.contrib import admin
from linted.models import Repository, Language, Linter, RepositoryLinter, RepositoryKey


admin.site.register(Repository)
admin.site.register(Language)
admin.site.register(Linter)
admin.site.register(RepositoryLinter)
admin.site.register(RepositoryKey)