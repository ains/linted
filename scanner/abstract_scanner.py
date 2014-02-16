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
    def get_snippet(file_path, start_line, end_line):
        with open(file_path) as f:
            file_contents = f.read()
            file_lines = file_contents.split('\n')

            snippet_content = '\n'.join(file_lines[(start_line - 1):end_line])
            return textwrap.dedent(snippet_content)

    def save_violation(self, error_group, file_path, start_line, end_line):
        scan_violation = ScanViolation()

        scan_violation.scanner = self.scanner
        scan_violation.scan = self.repository_scan
        scan_violation.snippet = self.get_snippet(file_path, start_line, end_line)

        scan_violation.error_group = error_group
        scan_violation.file = self.get_relative_path(file_path)
        scan_violation.start_line = start_line
        scan_violation.end_line = end_line

        scan_violation.save()
