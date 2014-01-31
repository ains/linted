#Importer for PHP_MD rulesets
#Files to import located at https://github.com/phpmd/phpmd/tree/master/src/main/resources/rulesets

import sys
import os
import glob
import re
import xml.etree.ElementTree as et


#Convert an error message to it's equivalent Regex pattern
def message_to_pattern(message):
    escaped_message = re.escape(message)
    return re.sub(r'\\{[0-9]+\\}\\', '(.*)', escaped_message)


namespaces = {'pmd': 'http://pmd.sf.net/ruleset/1.0.0'}
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please call the script with the directory containing the PHPMD rulesets")
        exit(0)

    for ruleset_file in glob.glob(os.path.join(sys.argv[1], '*.xml')):
        tree = et.parse(ruleset_file)
        root = tree.getroot()

        for rule_node in root.findall('pmd:rule', namespaces=namespaces):
            rule_name = rule_node.get('name')
            rule_message = rule_node.get('message')
            rule_description = rule_node.find('pmd:description', namespaces=namespaces).text

            print(message_to_pattern(rule_message))
