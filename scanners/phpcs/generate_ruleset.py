#Generates json config from PHPCS standards
#Files to import located at https://github.com/squizlabs/PHP_CodeSniffer/tree/master/CodeSniffer/Standards

import sys
import os
import fnmatch
import xml.etree.ElementTree as ElementTree
import json
import glob
import collections


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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please call the script with the directory containing the PHPCS standards')
        exit(0)

    standards_path = sys.argv[1]
    ruleset = {}

    rule_data = get_rule_data()
    for root, _, filenames in os.walk(sys.argv[1]):
        for ruleset_file in fnmatch.filter(filenames, 'ruleset.xml'):

            tree = ElementTree.parse(os.path.join(root, ruleset_file))
            root = tree.getroot()

            ruleset_file_name = os.path.basename(ruleset_file)
            ruleset_name = root.get('name')
            ruleset_rules = {}

            for rule_node in root.findall('rule'):
                rule_name = rule_node.get('ref')

                #Only pick "top-level" rules
                if rule_name.count('.') == 2:
                    ruleset_rules[rule_name] = {
                        'name': rule_data[rule_name]['name'],
                        'enabled': True,
                        'description': rule_data[rule_name]['description'],
                        'properties': {}
                    }

            ruleset[ruleset_name] = {
                'name': ruleset_name,
                'rules': ruleset_rules
            }

    print(json.dumps(ruleset))