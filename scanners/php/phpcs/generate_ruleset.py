#Generates json config from PHPCS standards
#Files to import located at https://github.com/squizlabs/PHP_CodeSniffer/tree/master/CodeSniffer/Standards

import sys
import os
import xml.etree.ElementTree as ElementTree
import glob
import collections
import json


def get_rule_data():
    #Allows us to silently handle non documented sniffs by returning empty strings
    rule_data = collections.defaultdict(lambda: collections.defaultdict(lambda: ""))

    for doc_file in glob.glob(os.path.join(sys.argv[1], '*', 'Docs', '*', '*.xml')):
        #Get rule from doc path
        rel_path = os.path.relpath(doc_file, standards_path)
        rule_ref = rel_path \
            .replace('/Docs', '') \
            .replace('.xml', '') \
            .replace('Standard', '') \
            .replace('/', '.')

        #Get documentation data
        tree = ElementTree.parse(doc_file)
        root = tree.getroot()
        rule_name = root.get('title')
        rule_description = root.find('standard').text.strip()

        rule_data[rule_ref] = {
            'name': rule_name,
            'description': rule_description
        }

    return rule_data


def get_defined_sniffs(standard_dir, rule_data):
    defined_sniffs = {}
    for doc_file in glob.glob(os.path.join(standard_dir, 'Sniffs', '*', '*.php')):
        #Get rule from doc path
        rel_path = os.path.relpath(doc_file, standards_path)
        rule_name = rel_path \
            .replace('/Sniffs', '') \
            .replace('.php', '') \
            .replace('Sniff', '') \
            .replace('/', '.')

        defined_sniffs[rule_name] = {
            'name': rule_data[rule_name]['name'],
            'enabled': True,
            'description': rule_data[rule_name]['description'],
            'properties': {}
        }

    return defined_sniffs


def get_imported_rules(standard_dir, rule_data):
    imported_rules = {}

    ruleset_file = os.path.join(standard_dir, 'ruleset.xml')
    tree = ElementTree.parse(ruleset_file)
    root = tree.getroot()

    for rule_node in root.findall('rule'):
        rule_name = rule_node.get('ref')

        #Only pick "top-level" rules
        if rule_name.count('.') == 2:
            imported_rules[rule_name] = {
                'name': rule_data[rule_name]['name'],
                'enabled': True,
                'description': rule_data[rule_name]['description'],
                'properties': {}
            }

    return imported_rules


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please call the script with the directory containing the PHPCS standards')
        exit(0)

    standards_path = sys.argv[1]
    ruleset = {}

    rule_data = get_rule_data()

    EXCLUDED_STANDARDS = ['Generic', 'MySource', 'PHPCS']
    standard_list = os.walk(standards_path).next()[1]

    for standard in standard_list:
        if standard not in EXCLUDED_STANDARDS:
            standard_dir = os.path.join(standards_path, standard)

            defined_sniffs = get_defined_sniffs(standard_dir, rule_data)
            imported_rules = get_imported_rules(standard_dir, rule_data)

            rules = {}
            rules.update(defined_sniffs)
            rules.update(imported_rules)

            ruleset[standard] = {
                'name': standard,
                'rules': rules
            }

    print(json.dumps(ruleset))