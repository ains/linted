#Generates crispyforms template from PHPMD rulesets
#Files to import located at https://github.com/phpmd/phpmd/tree/master/src/main/resources/rulesets

import sys
import os
import glob
import xml.etree.ElementTree as et

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linted.settings")

namespaces = {'pmd': 'http://pmd.sf.net/ruleset/1.0.0'}
prefix = "phpmd"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please call the script with the directory containing the PHPMD rulesets")
        exit(0)

    for ruleset_file in glob.glob(os.path.join(sys.argv[1], '*.xml')):
        tree = et.parse(ruleset_file)
        root = tree.getroot()

        for rule_node in root.findall('pmd:rule', namespaces=namespaces):
            rule_name = rule_node.get('name')
            rule_description = rule_node.find('pmd:description', namespaces=namespaces).text

            for property_node in rule_node.findall('pmd:priorities', namespaces=namespaces):
                property_name = property_node.get('name')
                property_description = property_node.get('description')
                property_default = property_node.get('value')

                if property_default == "true" or property_default == "false":
                    #Create boolean field
                    pass
                else:
                    #Create text field
                    pass

