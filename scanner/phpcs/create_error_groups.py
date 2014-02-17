#Importer for PHP_CodeSniffer rulesets
#Files to import located at https://github.com/squizlabs/PHP_CodeSniffer/tree/master/CodeSniffer/Standards

import sys
import os
import fnmatch
from linted.models import ErrorGroup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linted.settings")

prefix = "phpcs"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please call the script with the directory containing the PHPCS rulesets")
        exit(0)

    ruleset_path = sys.argv[1]
    for root, _, files in os.walk(ruleset_path):
        for file in files:
            full_path = os.path.join(root, file)
            if fnmatch.fnmatch(full_path, "*/Sniffs/*.php"):
                rule_path = os.path.relpath(full_path, ruleset_path)
                cleaned_rule_path = rule_path.replace("Sniffs/", "").replace(".php", "")
                rule_name = cleaned_rule_path.replace("/", ".")

                error_group = ErrorGroup()
                error_group.name = '{}.{}'.format(prefix, rule_name)
                error_group.description = ""
                error_group.save()