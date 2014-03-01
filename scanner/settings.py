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
            self.settings = json.loads(repository_scanner.settings, object_pairs_hook=tree)

        self.repository_scanner = repository_scanner

    def clear_settings(self):
        self.settings = tree()

    def get_property_value(self, ruleset, rule, property):
        custom_property_value = self.get_custom_property_value(ruleset, rule, property)
        if custom_property_value is not None:
            return custom_property_value
        else:
            (default_type, default_value) = self.get_default_rule(ruleset, rule, property)
            return default_value


    def get_default_rule(self, ruleset, rule, property):
        try:
            ruleset_property = self.ruleset[ruleset]['rules'][rule]['properties'][property]
            property_type = ruleset_property['type']
            default_value = ruleset_property['default']

            return property_type, default_value
        except KeyError:
            return None

    def get_custom_property_value(self, ruleset, rule, property):
        custom_rule_property = self.settings[ruleset][rule].get(property)
        return custom_rule_property


    def add_custom_rule(self, ruleset, rule, property, value):
        default_rule = self.get_default_rule(ruleset, rule, property)
        if default_rule is not None:
            property_type, default_value = default_rule

            if property_type == 'bool':
                default_value = (default_value == 'True')

            if value != default_value:
                self.settings[ruleset][rule][property] = value

    def save(self):
        self.repository_scanner.settings = json.dumps(self.settings)
        self.repository_scanner.save()
