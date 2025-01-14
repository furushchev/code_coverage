#!/usr/bin/env python

# generate_base_coverage.py
# this script lists up all python files in repo and generate base coverage report.
# the base coverage report covers all python files, including non-tested files.
# with the base coverage report, we can calculate coverage with non-tested files, too.

import argparse
import glob
import json
import os

import magic


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_dir', type=str)
    parser.add_argument('--output', '-o', type=str, default='.')
    parser.add_argument('--include-python-directories',
                        '-i',
                        type=str,
                        nargs='*',
                        default=['bin', 'node_scripts', 'src', 'scripts'])
    args = parser.parse_args()

    # python .coverage file is json file with comment at the top.
    # the json structure is like below.
    #
    # # comment at the top
    # !coverage.py: This is a private format, don't read it directly!
    # {
    #   "lines": {
    #     # filepath: [list of hitting lines]
    #     "/home/gitai/gitai/catkin_ws/src/sample_package/scripts/hoge.py": [1, 3, 4, 5],
    #     "/home/gitai/gitai/catkin_ws/src/sample_package/scripts/fuga.py": [],
    #     ...
    #   }
    # }
    #
    # If you want to make .coverage file with no hitting lines,
    # you need to register empty list as the list of hitting lines.
    python_filepaths = list_python_filepaths(os.path.abspath(args.base_dir),
                                             args.include_python_directories)
    coverage_lines = {}
    for python_filepath in python_filepaths:
        coverage_lines[python_filepath] = []
    coverage_dict = {"lines": coverage_lines}
    coverage_txt = '!coverage.py: This is a private format, don\'t read it directly!\n'
    coverage_txt += json.dumps(coverage_dict)
    os.makedirs(args.output, exist_ok=True)
    with open(os.path.join(args.output, '.coverage'), 'w') as coverage_f:
        coverage_f.write(coverage_txt)


def list_python_filepaths(base_dir, python_directories):
    python_filepaths = []
    for python_dir in python_directories:
        for filepath in glob.glob(os.path.join(base_dir, python_dir, '**'),
                                  recursive=True):
            if os.path.isfile(filepath):
                fileext = os.path.splitext(filepath)[1]
                if (fileext == '.py' or
                        (fileext == '' and 'Python' in magic.from_file(filepath))):
                    python_filepaths.append(filepath)
    return sorted(set(python_filepaths))


if __name__ == '__main__':
    main()
