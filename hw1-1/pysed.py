#!/usr/bin/python

import sys
import os
import re

REGEX_METHOD_MAPPING = {
    r'(^s\/).*.(\/$)': 'replace',
    r'(^\/).*.(\/d$)': 'delete',
    r'(^\/).*.(\/p$)': 'print',
}


class PySed:
    def __init__(self):
        return

    def validate_file(self, args):
        file = args[-1]
        abs_file = self._absolute(file)
        if not os.path.exists(abs_file):
            print 'File %s does not exist' % file
            sys.exit(2)

    def run(self, args):
        self.validate_file(args)
        sed_type = self.get_sed_type(args)
        self._dispatch(sed_type, args)

    @classmethod
    def get_sed_type(cls, args):
        if len(args) <= 2:
            cls.print_help()
            return

        sed_type = ""
        for regex, action in REGEX_METHOD_MAPPING.items():
            if re.search(regex, args[1]):
                sed_type = action
                break
        if sed_type == "":
            cls.print_regex_err()
            return

        return sed_type

    def _dispatch(self, sed_type, args):
        kargs = args[1].split('/')[1:-1]
        kargs.append(args[2])
        method = 'self.' + sed_type + '_match_pattern(*kargs)'
        eval(method)

    def _absolute(self, filename):
        if filename[0] != '/':
            dirname = os.path.dirname(os.path.abspath(__file__))
            filename = dirname + '/' + filename
        return filename

    def print_match_pattern(self, *kargs):
        pattern = kargs[0]
        matched_lines = []
        file = kargs[-1]
        abs_file = self._absolute(file)
        with open(abs_file) as file_handler:
            for line in file_handler.readlines():
                if re.search(pattern, line):
                    matched_lines.append(line)

        if len(matched_lines) == 0:
            print 'No match found'
        else:
            print 'Found these lines that match the pattern:'
            for line in matched_lines:
                print line

    def delete_match_pattern(self, *kargs):
        pattern = kargs[0]
        new_filelines = []
        file = kargs[-1]
        abs_file = self._absolute(file)
        with open(abs_file) as file_handler:
            for line in file_handler.readlines():
                if not re.search(pattern, line):
                    new_filelines.append(line)

        with open(abs_file, 'w') as file_handler:
            file_handler.writelines(new_filelines)

    def replace_match_pattern(self, *kargs):
        old = kargs[0]
        new = kargs[1]
        new_filelines = []
        file = kargs[-1]
        abs_file = self._absolute(file)
        with open(abs_file) as file_handler:
            for line in file_handler.readlines():
                if re.search(old, line):
                    line = line.replace(old, new)
                new_filelines.append(line)

        with open(abs_file, 'w') as file_handler:
            file_handler.writelines(new_filelines)

    @classmethod
    def print_help(cls):
        print 'usage============'
        print 'pysef {option/pattern} $filename'
        sys.exit(1)

    @classmethod
    def print_regex_err(cls):
        print 'Please provide correct Regular Expressions'
        sys.exit(2)


def main():
    pysed = PySed()
    output = pysed.run(sys.argv)
    return sys.exit(output)

if __name__ == '__main__':
    sys.exit(main())
