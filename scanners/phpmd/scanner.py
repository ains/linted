from scanners.abstract_scanner import AbstractScanner
from linted.models import Scanner, ErrorGroup
from django import forms

import collections
import subprocess
import xml.etree.ElementTree as ElementTree
import lxml.builder as builder
import lxml.etree
import os


class PHPMDForm(forms.Form):
    RULE_SETS = (
        ('codesize', 'Code Size'),
        ('naming', 'Naming'),
        ('design', 'Design'),
        ('unusedcode', 'Unused Code')
    )
    selected_rule_sets = forms.MultipleChoiceField(
        choices=RULE_SETS, widget=forms.CheckboxSelectMultiple)


class PHPMDScanner(AbstractScanner):
    def __init__(self, repository_scan, path, excluded_files='', settings=None):
        scanner = Scanner.objects.get(short_name='phpmd')
        super(PHPMDScanner, self).__init__(repository_scan, scanner, path)

        self.excluded_files = excluded_files
        self.settings = settings

    settings_form = PHPMDForm

    @staticmethod
    def get_error_group(error_name):
        error_group_name = 'phpmd.{}'.format(error_name)
        return ErrorGroup.objects.get(name=error_group_name)

    def configure(self):
        config = self.settings.get_scanner_config()
        rule_settings = self.settings.get_scanner_rules()

        root = builder.ElementMaker(namespace='http://pmd.sf.net/ruleset/1.0.0',
                                    nsmap={
                                        None: 'http://pmd.sf.net/ruleset/1.0.0',
                                        'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                                        'schemaLocation': 'http://pmd.sf.net/ruleset_xml_schema.xsd',
                                        'noNamespaceSchemaLocation': 'http://pmd.sf.net/ruleset_xml_schema.xsd'
                                    })
        E = builder.ElementMaker()
        ruleset_xml = root.ruleset(name="Generated Ruleset")

        for rule_set in config['selected_rule_sets']:
            rule_location = "rulesets/{}.xml".format(rule_set)
            ruleset_xml.append(E.rule(ref=rule_location))

        for rule_file, custom_rules in rule_settings.items():
            for rule, properties in custom_rules.items():
                ref = "rulesets/{}/{}".format(rule_file, rule)

                custom_rule = E.rule(ref=ref)
                custom_properties = E.properties(E.priority("1"))
                for property_name, value in properties.items():
                    custom_properties.append(E.property(name=property_name, value=value))

                custom_rule.append(custom_properties)
                ruleset_xml.append(custom_rule)

        settings_file = os.path.join(self.path, 'phpmd_ruleset.xml')
        with open(settings_file, 'w+') as f:
            f.write(lxml.etree.tostring(ruleset_xml, pretty_print=True))

        return settings_file

    def process_results(self, scan_result):
        root = ElementTree.fromstring(scan_result)
        violation_dict = collections.defaultdict(list)

        for file_node in root.findall('file'):
            file_path = file_node.get('name')

            for violation_node in file_node.findall('violation'):
                start_line = int(violation_node.get('beginline'))
                end_line = int(violation_node.get('endline'))

                rule = violation_node.get('rule')
                error_group = self.get_error_group(rule)

                message = violation_node.text.strip()

                #If we recognise this error group
                if error_group is not None:
                    violation_dict[file_path].append((start_line, end_line, error_group, message))

        self.save_all_violations(violation_dict)

    def run(self):
        try:
            docker_cmd = ['docker', 'run', '-v', '{}:{}:ro'.format(self.path, self.path), 'linted/phpmd']
            phpmd_command = ['phpmd', self.path, 'xml']

            if self.settings is not None:
                settings_file = self.configure()
                phpmd_command += [settings_file]
            else:
                phpmd_command += ['codesize,unusedcode,naming']

            subprocess.check_output(docker_cmd + phpmd_command)
        except subprocess.CalledProcessError as e:
            #Exit code 2 means scan completed successfully, but there were rule violations
            if e.returncode == 2:
                scan_result = str(e.output)
                self.process_results(scan_result)
