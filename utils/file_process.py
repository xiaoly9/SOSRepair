__author__ = 'afsoona'

import difflib
import subprocess

def number_of_lines(filename):
    proc = subprocess.Popen(["wc", "-l", filename], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()
    return int(out.strip(' ').split(' ')[0])

def compare_files(file1, file2):
    with open(file1, 'r') as hosts0:
        with open(file2, 'r') as hosts1:
            diff = difflib.unified_diff(
                hosts0.readlines(),
                hosts1.readlines(),
                fromfile='hosts0',
                tofile='hosts1',
            )
            for line in diff:
                return False
    return True