import os
import json

from django.conf import settings
from linted.models import tree


class ScannerSettings():
    def __init__(self, repository_scanner):
        scanner_name = repository_scanner.scanner.short_name

        ruleset_file = os.path.join(settings.SCANNER_DIR, scanner_name, 'ruleset.json')
        with open(ruleset_file) as f:
            self.ruleset = json.loads(f.read())

        if repository_scanner.settings == '':
            self.settings = tree()
        else:
            self.settings = json.loads(repository_scanner.settings)

    def clear_settings(self):
        self.settings = tree()

    def get_default_rule(self, ruleset, rule, property):
        try:
            ruleset_property = self.ruleset[ruleset]['rules'][rule]['properties'][property]
            property_type = ruleset_property['type']
            default_value = ruleset_property['default']

            return property_type, default_value
        except KeyError:
            return None

    def add_custom_rule(self, ruleset, rule, property, value):
        default_rule = self.get_default_rule(ruleset, rule, property)
        if default_rule is not None:
            property_type, default_value = default_rule

            if property_type == 'bool':
                default_value = (default_value == 'True')

            if value != default_value:
                self.settings[ruleset][rule][property] = value

