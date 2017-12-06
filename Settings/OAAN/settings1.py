# 463-C-bug-7679531-7679553
__author__ = 'Afsoon Afzal'

import logging

# LIBCLANG_PATH = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib'
LIBCLANG_PATH = '/home/afsoon/llvm/build/lib/libclang.so'
# LIBCLANG_PATH = '/Users/afsoona/llvm/build/lib/libclang.dylib'

GENERATE_DB_PATH = '/home/ahill6/codeflaws/463-C-bug-7679531-7679553'

Z3_COMMAND = '/home/afsoon/z3/build/z3'

LARGEST_SNIPPET = 7
SMALLEST_SNIPPET = 3

TIMEOUT = 7500

DATABASE = {
    'db_name': 'andy-test2', # switch back
    'user': 'ahill6',
    'password': None
}

ALL_PATCHES = False

LOGGING = {
    'filename': 'logs/repair.log',
    'level': logging.DEBUG
}

logging.basicConfig(**LOGGING)

MAX_SUSPICIOUS_LINES = 10

VALID_TYPES = ['int', 'short', 'long', 'char', 'float', 'double', 'long long', 'size_t']

TESTS_LIST = "/home/ahill6/codeflaws/463-C-bug-7679531-7679553/tests_list.txt"
TEST_SCRIPT = "/home/ahill6/codeflaws/463-C-bug-7679531-7679553/test-searchrepair.sh "
TEST_SCRIPT_TYPE = "/bin/bash"
COMPILE_SCRIPT = "cd /home/ahill6/codeflaws/463-C-bug-7679531-7679553/ && make clean; make -f Makefile"
FAULTY_CODE = "/home/ahill6/codeflaws/463-C-bug-7679531-7679553/463-C-7679531.c"
BUG_TYPE = "OAAN"

COMPILE_EXTRA_ARGS = []

MAKE_OUTPUT = "/home/ahill6/codeflaws/463-C-bug-7679531-7679553/makeout"

METHOD_RANGE = (1, 50)

SOSREPAIR = False
