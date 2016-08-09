__author__ = 'Afsoon Afzal'

import logging
from clang.cindex import *
from settings import *
from utils.file_process import number_of_lines
from repository.snippet_preparation import CodeSnippetManager

Config.set_library_file(LIBCLANG_PATH)
logger = logging.getLogger(__name__)


class SuspiciousBlock():
    def __init__(self, line_number, line_range, blocks, vars, outputs, functions, filename):
        self.line_number = line_number
        self.line_range = line_range
        self.blocks = blocks
        self.vars = vars
        self.outputs = outputs
        self.functions = functions
        self.filename = filename

    def get_output_names(self):
        if isinstance(self.outputs, dict):
            return [i for i in self.outputs.keys()]
        else:
            return []

    def get_var_names(self):
        return [i[0] for i in self.vars]


class FaultLocalization():
    def __init__(self):
        self.filename = FAULTY_CODE
        self.number_of_lines = number_of_lines(FAULTY_CODE)
        self.root = None

    def line_to_block(self, line_number):
        index = Index.create()
        logger.info("parsing")
        self.root = index.parse(self.filename)
        logger.info("parsing root")
        return self.traverse_tree_suspicious_block(self.root.cursor, self.number_of_lines, line_number)

    def traverse_tree(self, line_number, ast):
        assert (isinstance(ast, Cursor))
        block = (1, 10000000)
        current = ast
        children = ast.get_children()
        function = None
        cond = True
        while cond:
            for child in children:
                cond = True
                if str(child.location.file) != self.filename:
                    continue
                # print block
                # print str(child.spelling) + " " + str(child.location.file)
                # print child.location.line
                if child.location.line > line_number:
                    temp_block = (current.location.line, child.location.line)
                    if current.kind == CursorKind.IF_STMT:
                        cond = False
                    elif temp_block[1] - temp_block[0] < 4:
                        cond = False
                        if block[1] - block[0] > 6:
                            block = (temp_block[1] - 6, temp_block[1])
                        break
                    block = temp_block
                    break
                current = child
                if child.kind == CursorKind.FUNCTION_DECL:
                    function = child
            children = current.get_children()

        return SuspiciousBlock(line_number, block, current, function)

    def traverse_tree_suspicious_block(self, ast, end_of_file, line_number):
        assert (isinstance(ast, Cursor))
        from_line = -1
        blocks = []
        children = list(ast.get_children())
        children.append(end_of_file)
        for child in children:
            cursor = False
            if isinstance(child, Cursor):
                cursor = True
            if cursor and (str(child.location.file) != self.filename or child.kind == CursorKind.DECL_STMT):
                continue
            line = child.location.line if cursor else child
            # print line
            if from_line < 0:
                from_line = line
                blocks.append(child)
                continue
            if line <= line_number:
                blocks.append(child)
                continue
            dist = line - from_line
            generate_block = False
            if dist > LARGEST_SNIPPET:
                while (line - from_line) > LARGEST_SNIPPET:
                    if len(blocks) == 1:  # means it's a large block
                        return self.traverse_tree_suspicious_block(blocks[0], line, line_number)
                    else:
                        if len(blocks) > 1 and blocks[1].location.line <= line_number:
                            blocks.pop(0)
                            from_line = blocks[0].location.line
                        else:
                            generate_block = True
                            break
            if generate_block or (LARGEST_SNIPPET >= (line - from_line) >= SMALLEST_SNIPPET and line >= line_number >= from_line):
                while len(blocks) > 1 and blocks[1].location.line <= line_number and \
                                        LARGEST_SNIPPET >= (line - blocks[1].location.line) >= SMALLEST_SNIPPET:
                    blocks.pop(0)
                    from_line = blocks[0].location.line
                vars = CodeSnippetManager.find_vars(blocks)
                outputs = CodeSnippetManager.find_outputs(blocks)
                if vars != -1 and outputs != -1:
                    func_calls = CodeSnippetManager.find_function_calls(blocks)
                    sb = SuspiciousBlock(line_number, (from_line, line), blocks, vars, outputs, func_calls, self.filename)
                    return sb
                return None
            if cursor:
                blocks.append(child)
                from_line = blocks[0].location.line
        return None

if __name__ == "__main__":
    fl = FaultLocalization('src/fdevent_freebsd_kqueue.c')
    sb = fl.line_to_block(57)
    print str(sb.block) + " " + str(sb.node.kind) + " " + str(sb.node.type.kind) + " " + str(sb.function.spelling)
