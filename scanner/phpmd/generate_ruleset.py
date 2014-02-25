#Generates crispyforms template from PHPMD rulesets
#Files to import located at https://github.com/phpmd/phpmd/tree/master/src/main/resources/rulesets

import sys
import os
import glob
import xml.etree.ElementTree as ElementTree
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linted.settings')

namespaces = {'pmd': 'http://pmd.sf.net/ruleset/1.0.0'}
prefix = 'phpmd'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please call the script with the directory containing the PHPMD rulesets')
        exit(0)

    rules_dict = {}
    for ruleset_file in glob.glob(os.path.join(sys.argv[1], '*.xml')):
        tree = ElementTree.parse(ruleset_file)
        root = tree.getroot()

        ruleset_file_name = os.path.basename(ruleset_file)
        ruleset_name = root.get('name')
        ruleset_rules = {}

        for rule_node in root.findall('pmd:rule', namespaces=namespaces):
            rule_name = rule_node.get('name')
            rule_description = rule_node.find('pmd:description', namespaces=namespaces).text

            rule_properties = {}

            for property_node in rule_node.findall('*/pmd:property', namespaces=namespaces):
                property_name = property_node.get('name')
                property_description = property_node.get('description')

                property_default = property_node.get('value')
                if property_default == 'true' or property_default == 'false':
                    property_default_value = (property_default == 'true')
                    property_type = 'bool'
                else:
                    property_default_value = property_default
                    try:
                        int(property_default_value)
                        property_type = 'int'
                    except ValueError:
                        property_type = 'string'

                rule_properties[property_name] = {
                    'description': property_description,
                    'default': property_default_value,
                    'type': property_type
                }
            
            ruleset_rules[rule_name] = {
                'name': rule_name,
                'enabled': True,
                'description': rule_description,
                'properties': rule_properties
            }
        rules_dict[ruleset_file_name] = {
            'name': ruleset_name,
            'rules': ruleset_rules
        }

    print(json.dumps(rules_dict))