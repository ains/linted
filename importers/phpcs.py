#Importer for PHP_CodeSniffer rulesets
#Files to import located at https://github.com/squizlabs/PHP_CodeSniffer/tree/master/CodeSniffer/Standards

import sys
import os
import re


#Convert an error message to it's equivalent Regex pattern
def message_to_pattern(message):
    escaped_message = re.escape(message)
    return re.sub(r'\\{[0-9]+\\}\\', '(.*)', escaped_message)


error_variable_regex = r"error\s+=\s+['\"](.*)['\"];"
error_literal_regex = r"phpcsFile->addError\('(.*?)',"

warning_variable_regex = r"warning\s+=\s+['\"](.*)['\"];"
warning_literal_regex = r"phpcsFile->addWarning\('(.*?)',"


def process_ruleset_file(file_name):
    ruleset_violations = []

    with open(file_name, 'r', encoding='utf-8') as f:
        ruleset_contents = f.read()

        error_variables = re.findall(error_variable_regex, ruleset_contents)
        error_strings = re.findall(error_literal_regex, ruleset_contents)

        warning_variables = re.findall(warning_variable_regex, ruleset_contents)
        warning_strings = re.findall(warning_literal_regex, ruleset_contents)

        ruleset_violations.extend(error_variables)
        ruleset_violations.extend(error_strings)
        ruleset_violations.extend(warning_variables)
        ruleset_violations.extend(warning_strings)

    print(ruleset_violations)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please call the script with the directory containing the PHPCS rulesets")
        exit(0)

    for root, _, files in os.walk(sys.argv[1]):
        for file in files:
            if file.endswith('.php'):
                process_ruleset_file(os.path.join(root, file))