from django.core.management.base import BaseCommand
from scanners.install import install_scanner


class Command(BaseCommand):
    help = 'Installs a chosen scanner'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        scanner_name = args[0]
        install_scanner(scanner_name)
