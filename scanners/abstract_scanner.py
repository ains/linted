from linted.models import ScanViolation

import os
import textwrap


class AbstractScanner(object):
    def __init__(self, repository_scan, scanner, path):
        self.repository_scan = repository_scan
        self.scanner = scanner
        self.path = path

    def get_relative_path(self, abs_path):
        return os.path.relpath(abs_path, self.path)

    @staticmethod
    def get_snippet(file_lines, start_line, end_line):
        snippet_content = '\n'.join(file_lines[(start_line - 1):end_line])
        return textwrap.dedent(snippet_content)

    def save_all_violations(self, file_violations):
        for file_path, violation_list in file_violations.items():
            with open(file_path) as f:
                rel_path = self.get_relative_path(file_path)

                file_contents = f.read()
                file_lines = file_contents.split('\n')

                for (start_line, end_line, error_group, message) in violation_list:
                    snippet = self.get_snippet(file_lines, start_line, end_line)
                    self.save_violation(rel_path, start_line, end_line, error_group, snippet, message)

    def save_violation(self, rel_path, start_line, end_line, error_group, snippet, message):
        scan_violation = ScanViolation()

        scan_violation.scanner = self.scanner
        scan_violation.scan = self.repository_scan

        scan_violation.file = rel_path
        scan_violation.start_line = start_line
        scan_violation.end_line = end_line
        scan_violation.error_group = error_group
        scan_violation.snippet = snippet
        scan_violation.message = message

        scan_violation.save()
