from django.contrib import admin
from linted.models import Repository, Language, Scanner, RepositoryScanner, RepositoryKey, ErrorGroup, ScanViolation, \
    RepositoryScan


admin.site.register(Repository)
admin.site.register(RepositoryScan)
admin.site.register(Language)
admin.site.register(Scanner)
admin.site.register(RepositoryScanner)
admin.site.register(RepositoryKey)
admin.site.register(ErrorGroup)
admin.site.register(ScanViolation)