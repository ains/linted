#Importer for PHP_MD rulesets
#Files to import located at https://github.com/phpmd/phpmd/tree/master/src/main/resources/rulesets

import sys
import os
import glob
import json
import xml.etree.ElementTree as ElementTree


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linted.settings")

namespaces = {'pmd': 'http://pmd.sf.net/ruleset/1.0.0'}
prefix = "phpmd"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please call the script with the directory containing the PHPMD rulesets")
        exit(0)

    output_data = {
        'error_groups': []
    }

    for ruleset_file in glob.glob(os.path.join(sys.argv[1], '*.xml')):
        tree = ElementTree.parse(ruleset_file)
        root = tree.getroot()

        for rule_node in root.findall('pmd:rule', namespaces=namespaces):
            rule_name = rule_node.get('name')
            rule_description = rule_node.find('pmd:description', namespaces=namespaces).text

            error_group = {
                'name': rule_name,
                'description': rule_description.strip()
            }
            output_data['error_groups'].append(error_group)

    print (json.dumps(output_data))
