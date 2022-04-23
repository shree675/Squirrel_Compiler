from operator import indexOf
import re
from collections import defaultdict
import os
from CodeGeneration import RegisterAllocation


class Node:
    def __init__(self, index, code_block):
        self.index = index
        self.code_block = code_block
        self.next = set()
        self.leading_label = None
        if ':' in code_block.split('\n')[0]:
            self.leading_label = code_block.split('\n')[0].split(':')[0]
        self.function_next = None  # In case the block contains a


class CodeGen:

    arithmetic_operators = set("+ - * / % && || > < >= <= ! != = ==".split())

    datatype_sizes = {
        'int': 4,
        'float': 4,
        'char': 1,
        'bool': 4,
    }

    def __init__(self):
        self.register_descriptor = defaultdict(list)
        self.address_descriptor = defaultdict(list)
        # We store non-mutable strings that are retured from functions in the data segment
        # Naming convention for these strings is return_0, return_1 and so on
        # self.return_string_count is used to keep track of these names
        self.return_string_count = 0
        self.array_addresses = defaultdict()
        self.string_addresses = defaultdict()
        # This is the fixed starting address of data segment on QTSPIM
        self.memory_pointer = 0x10010000

    def get_node(self, graph, index):
        for node in graph:
            if node.index == index:
                return node

    def DFS(self, visited=None, graph=[], node=None):  # function for dfs
        if node not in visited:
            visited.add(node)
            for neighbour_index in node.next:
                neighbour = self.get_node(graph, neighbour_index)
                self.DFS(visited, graph, neighbour)

    def eliminate_dead_code(self, blocks, symbol_table, optimization_level):
        # print("calling eliminate_dead_code")
        # print("================================================")
        # print("Initial Block Structure")
        full_code = '\n'.join(blocks)
        all_lines = full_code.split('\n')

        return_map = []
        return_pointer = 0
        for index, line in enumerate(all_lines):
            if 'return' in line:
                return_map.append(index)

        CFG = []
        blocks_current = []
        for block in blocks:
            block = block.strip('\n')
            if block.isspace() or len(block) == 0:
                continue
            else:
                # while len(block.split('\n')) > 2 and 'return' in block.split('\n')[-1] and 'return' in block.split('\n')[-2]:
                #     block = '\n'.join(block.split('\n')[:-1])
                blocks_current.append(block)
        for block in blocks_current:
            # print(block)
            # print("----------------------------------------------")
            new_node = Node(blocks_current.index(block), block)
            CFG.append(new_node)
            # print("leading label: ", new_node.leading_label)
            # print(new_node.index, len(new_node.code_block), new_node.code_block)

        # Find all the function calls and
        for i in range(1, len(CFG)):
            block = CFG[i-1].code_block
            # print('before call check')
            last_line = block.split('\n')[-1]
            # print(last_line)
            if len(last_line.split(' ')) >= 3 and last_line.split(' ')[-3] == 'call':
                # print("Enter call check")
                funct = last_line.split(' ')[-2].split(',')[0]
                CFG[i].function_next = funct

        # print("================================================")

        # Start creating Control Flow Graph connections
        for node in CFG:
            last_line = node.code_block.split('\n')[-1]
            # last_line = node.code_block.rstrip('\n').split('\n')[-1]
            words = last_line.split(' ')
            # print(last_line)
            if (len(words) >= 1 and (words[0] == 'goto' or words[0] == 'return')) or 'call' in words:
                # The direct goto statements (without condition)
                if words[0] == 'goto':
                    label = words[1]
                    for search_node in CFG:
                        if search_node.leading_label is not None and search_node.leading_label == label:
                            node.next.add(search_node.index)
            else:
                # Add a connection from current block to the next block in sequence as there is no break of control flow
                if node.index < (len(blocks_current)-1):
                    node.next.add(node.index+1)

            if len(words) > 2 and words[-2] == 'goto':
                # For the gotos that accompany an if or ifFalse statement (with condition)
                label = words[-1]
                for search_node in CFG:
                    if search_node.leading_label is not None and search_node.leading_label == label:
                        node.next.add(search_node.index)
            # Identify the return statements and connect them to the points where they are called
            if len(words) >= 1 and words[0] == 'return':
                index = return_map[return_pointer]
                # Returns the location of the current return statement in the list of all code lines
                # we go upwards and search for the first functin label -> This is the function that this return statement belongs to
                # Hence we need to find all calls to this functin and make a connection going from this return statement to the next line after the specific function call
                while index >= 0:
                    words = all_lines[index].split(' ')
                    word = None
                    if len(words) < 1:
                        index -= 1
                        continue
                    else:
                        word = words[0]

                    if not word.startswith('#L') and word.endswith(':'):
                        word = word.split(':')[0]
                        # print("Function label found", word)
                        for search_node in CFG:
                            if search_node.function_next is not None and search_node.function_next == word:
                                node.next.add(search_node.index)
                        break
                    index -= 1

                return_pointer += 1
            # print('current line', words)
            if (len(words) > 2 and words[0] == 'call') or (len(words) > 4 and words[2] == 'call'):
                # print("call found")
                funct = words[-2].split(',')[0]
                # print('index of this block: ', node.index)
                for search_node in CFG:
                    if search_node.leading_label is not None and search_node.leading_label == funct:
                        node.next.add(search_node.index)

            """ print("Current node index", node.index)
            print('Current node code\n', node.code_block)
            print('in case of a call -> Function next stores: ', node.function_next)
            print('Next blocks', node.next)
            print("================================================") """

        # The CFG is now completed - we now perform a depth first search to identify the dead code blocks
        # And block unfreachable from the start block is dead code

        # Step 1: Find the start block, i.e., the one that contains 'start' as the leading label
        start_block = None
        for node in CFG:
            if node.leading_label == 'start':
                start_block = node
                break
        # print('start_block', start_block, type(start_block))
        visited = set()
        # Call DFS and obtin the visited blocks
        self.DFS(visited=visited, graph=CFG, node=start_block)
        list_of_visited_blocks = list(visited)
        list_of_visited_blocks.sort(key=lambda x: x.index)
        # COnvert the visited set to a list and append only the code blocks to blocks and then return it
        blocks = []
        for node in list_of_visited_blocks:
            blocks.append(node.code_block)
            # print(node.index)

        # print(*blocks, sep = '\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')

        return blocks

    def preamble(self, intermediate_code_final):

        # storing all the string constants
        self.data_segment_dict = {}
        self.global_dict = {}

        array_initializations = ''
        string_constants = ''
        data_types = "int float char bool string"

        # for line in intermediate_code_final:
        # if ":" in line:
        # break
        # line = line.split('=')
        # if line.index('=') == 2:
        # data_type = line[0]
        # variable = line[1]

        intermediate_code_generator = (
            i for i in intermediate_code_final.splitlines())

        for line in intermediate_code_generator:
            if "\"" in line:
                tokens = line.split()
                string_const = ""
                string_var = ""
                if '=' in tokens:
                    string_const = re.match(r".*(\".*\")", line).group(1)
                    string_var = tokens[tokens.index('=') - 1]
                    self.data_segment_dict[string_var] = (
                        ".asciiz", 0, string_const)
                else:
                    string_var = 'return'+str(self.return_string_count)
                    self.return_string_count += 1
                    string_const = re.match(r".*(\".*\")", line).group(1)
                string_constants += f'{string_var}:\n\t.asciiz {string_const}\n'
                self.string_addresses[string_var] = self.memory_pointer
                self.memory_pointer += len(string_const) + 1

            else:
                tokens = line.split()
                if tokens and tokens[0] in data_types and ']' in tokens[-1] and '=' not in tokens and len(tokens) == 2:
                    size = int(tokens[-1].split('[')[1][:-1])
                    num_of_elements = size//self.datatype_sizes[tokens[0]]
                    variable_name = tokens[-1].split('[')[0]
                    array = []
                    for _ in range(num_of_elements):
                        next_line = next(intermediate_code_generator)
                        array.append(next_line.split('=')[-1])
                    self.array_addresses[variable_name] = (
                        array, tokens[0], self.memory_pointer)
                    self.memory_pointer += size

        for array_var in self.array_addresses:
            array_initializations += f'\t{array_var}:\n'
            if self.array_addresses[array_var][1] == 'int':
                array_initializations += f'\t\t.word '
            elif self.array_addresses[array_var][1] == 'float':
                array_initializations += f'\t\t.float '
            elif self.array_addresses[array_var][1] == 'char' or self.array_addresses[array_var][1] == 'bool':
                array_initializations += f'\t\t.byte '
            for i in range(len(self.array_addresses[array_var][0])):
                if self.array_addresses[array_var][1] == 'bool':
                    array_initializations += f'1, ' if self.array_addresses[array_var][0][i].strip(
                    ) == 'true' else f'0, '
                else:
                    array_initializations += f'{self.array_addresses[array_var][0][i].strip()}, '
            array_initializations = array_initializations[:-2] + '\n'

        assembly_code = f".data\n{array_initializations}\n"

        return assembly_code

    def generate_target_code(self, intermediate_code, symbol_table, optimization_level):

        # print("Generate target code starts here...")
        # print('initial intermediate code--------------------------------------------------')
        # print(intermediate_code)
        # print("------------------------------------------------------------------------------")
        if not intermediate_code:
            # handle it more elegantly
            return ""

        intermediate_code = re.sub(r'\btrue\b', '1', intermediate_code)
        intermediate_code = re.sub(r'\bfalse\b', '0', intermediate_code)
        intermediate_code = re.sub(r'`', '__', intermediate_code)
        intermediate_code = re.sub(r'~', '__', intermediate_code)
        intermediate_code = re.sub(r'\bbool\b', 'int', intermediate_code)

        global_vars = re.findall(
            r"@[^@]*@", intermediate_code)

        print("global_vars: ", global_vars)

        intermediate_code = re.sub(r"@[^@]*@", '', intermediate_code)

        for var_code in global_vars:
            var_code = var_code[1:-1]
            intermediate_code = var_code + intermediate_code

        print("intermediate code : ", intermediate_code)

        """ The compiler allows 3 levels of optimization. O1, O2 and O3
        We associate 2 kinds of optimization with each level. """
        intermediate_code_final = ''  # initialise it with the original code

        # O1 level optimization starts here----------------------------------------------------------------
        # Create a set of labels that are used as targets of goto statements
        if optimization_level >= 1:
            goto_labels = set()
            for lines in intermediate_code.splitlines():
                if 'goto' in lines:
                    goto_labels.add(lines.split(' ')[-1])

            optimized_code0 = ""
            for lines in intermediate_code.splitlines():
                if lines.startswith('#L') and lines.split(':')[0] not in goto_labels:
                    pass
                else:
                    optimized_code0 += lines + '\n'
            # optimized_codde0 contains all the intermediate code except for labels that have no goto statements pointing to them
            # ----------------------------------------------------------------

            intermediate_code_list = optimized_code0.splitlines()
            optimized_code1 = intermediate_code_list[0] + '\n'
            i = 1
            while i < len(intermediate_code_list):
                if 'return' in intermediate_code_list[i-1] and 'return' in intermediate_code_list[i]:
                    pass
                else:
                    optimized_code1 += intermediate_code_list[i] + '\n'
                i += 1
            # print('optimized 0 code', optimized_code0)
            # ----------------------------------------------------------------
            # At the end of optimization level 1, redundant return statements are removed

            # print("**********************************************************")
            # print("optimized code 1", optimized_code1)
            intermediate_code_final = optimized_code1

        if optimization_level >= 2:
            # O2 Optimization level starts here ----------------------------------------------------------------
            # ----------------------------------------------------------------
            # Optimization Level 2 remives labels in consecutive lines and replaces all the occurences of the label with the first one
            optimized_code2 = ""
            redundant_labels = {}
            optimized_code_list = optimized_code1.splitlines()
            i = 0
            while i < len(optimized_code_list):
                lines = optimized_code_list[i]
                if lines.startswith('#L'):
                    optimized_code2 += lines + '\n'
                    k = i
                    for j in range(i+1, len(optimized_code_list)):
                        if optimized_code_list[j].startswith('#L'):
                            try:
                                redundant_labels[optimized_code_list[i].split(
                                    ':')[0]].append(optimized_code_list[j].split(':')[0])
                            except KeyError:
                                redundant_labels[optimized_code_list[i].split(
                                    ':')[0]] = [optimized_code_list[j].split(':')[0]]
                            k = j
                        else:
                            k += 1
                            break
                    i = k
                else:
                    optimized_code2 += lines + '\n'
                    i += 1

            for label in redundant_labels.keys():
                for l in redundant_labels[label]:
                    optimized_code2 = optimized_code2.replace(l+':', '')
                    optimized_code2 = optimized_code2.replace(l, label)

            # print(optimized_code2)
            # print("**********************************************************")
            # print("optimized code 2", optimized_code2)
            # ----------------------------------------------------------------
            # Optimization Level 3 removes all the goto statements that occur in consecutive statements,
            # retains only the first one
            optimized_code3 = ""
            optimized_code_list = optimized_code2.splitlines()
            i = 0
            while i < len(optimized_code_list):
                lines = optimized_code_list[i]
                if lines.startswith('goto'):
                    optimized_code3 += lines+'\n'
                    k = i
                    for j in range(i+1, len(optimized_code_list)):
                        if optimized_code_list[j].startswith('goto'):
                            k = j
                        else:
                            k += 1
                            break
                    i = k
                else:
                    optimized_code3 += lines+'\n'
                    i += 1
            intermediate_code_final = optimized_code3

        if optimization_level >= 3:
            # -------------------------------
            # O3 Optimization level starts here ----------------------------------------------------------------
            # Optimization Level 4 removes goto X and label X statements if they occur in consecutive lines
            # We remove the label only if no other goto points to it
            optimized_code4 = ""
            optimized_code_list = optimized_code3.splitlines()
            i = 0
            while i < len(optimized_code_list):
                lines = optimized_code_list[i]
                if lines.startswith('goto'):
                    label = lines.split(' ')[-1]
                    k = 0
                    flag = True
                    for k in range(len(optimized_code_list)):
                        if k != i and optimized_code_list[k].startswith('goto') and optimized_code_list[k].split(' ')[-1] == label:
                            flag = False
                            break
                    if optimized_code_list[i+1].startswith('#L') and optimized_code_list[i+1].split(':')[0] == label and flag:
                        i += 1
                    else:
                        optimized_code4 += lines+'\n'
                else:
                    optimized_code4 += lines+'\n'
                i += 1

            intermediate_code_final = optimized_code4
        print('*******************************************************************')
        print(intermediate_code_final)
        print('*******************************************************************')

        blocks = []
        block_line = ""
        prev = False
        first_label_seen = False
        for lines in intermediate_code_final.splitlines():
            # while len(block.split('\n')) > 2 and 'return' in block.split('\n')[-1] and 'return' in block.split('\n')[-2]:
            #         block = '\n'.join(block.split('\n')[:-1])
            if not first_label_seen and lines.endswith(':'):
                first_label_seen = True
                blocks.append(block_line)
                block_line += lines+'\n'
            elif prev == True:
                blocks.append(block_line)
                block_line = lines+'\n'
                prev = False
            elif ':' in lines and lines[0] != '#':
                blocks.append(block_line)
                block_line = ""
                block_line += lines+'\n'
            elif lines.startswith('#L') and lines.split(':')[0] in goto_labels:
                blocks.append(block_line)
                block_line = ""
                block_line += lines+'\n'
            elif 'goto' in lines:
                block_line += lines+'\n'
                prev = True
            elif 'return' in lines:
                block_line += lines+'\n'
                prev = True
            elif 'call' in lines:
                block_line += lines+'\n'
                prev = True
            else:
                block_line += lines+'\n'
        if block_line != "":
            blocks.append(block_line)

        reserved_operators_pattern = r"\+|\-|\*|\/|%|&&|\|\||>|<|>=|<=|\!|\!=|=|=="
        reserved_operators = "+ - * / % && || > < >= <= ! != = =="
        reserved_all_live_keywords = "if return ifFalse input output call param"
        reserved_all_dead_keywords = "int float string bool char"
        reserved_words = set(reserved_operators.split())
        live_and_next_use_blocks = []

        print("Printing all the blocks")
        # for block in blocks:
        #     print(block)
        print('-----------------------------------------------------------------')

        if optimization_level >= 3:
            blocks = self.eliminate_dead_code(
                blocks, symbol_table, optimization_level)
            print("Dead code elimination done --------------------------------------------------------------------------")
        print(*blocks, sep='\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n')
        # All optimizations are completed and Live Analysis of the blocks starts here

        for block in blocks:
            num_lines = len(block.split('\n'))
            lines = re.sub(r"\(.+\)", '', block).split('\n')
            live_and_next_use = []

            for i in range(num_lines-1, -1, -1):

                if lines[i].startswith('goto') or ':' in lines[i] or len(lines[i].strip()) == 0:
                    continue
                # for arrays arr[i] -> i is dead implies arr[i] is dead and i is alive implies arr[i] is alive
                # for arrays we are removing the arr and proceeding with i for the live analysis
                temp = lines[i].split(' ')
                for index, word in enumerate(temp):
                    if ']' in word:
                        temp[index] = re.sub(r'.*\[(.+)\]', r'\1', word)

                lines[i] = ' '.join(temp)

                variables = set(lines[i].split())-reserved_words
                operators = set(lines[i].split())-variables

                var_dict = {}

                # binary arithmetic expression
                # live and dead is decided based on rigth side or left side of the equality sign
                # we store line number for next use of the variable
                if len(operators) == 2 and len(variables) == 3:
                    line_variables = re.sub(
                        reserved_operators_pattern, '', lines[i]).split()
                    right_variables = line_variables[1:]
                    left_variable = line_variables[0]
                    var_dict = {left_variable: {'live': -1, 'next_use': -1}, right_variables[0]: {
                        'live': 1, 'next_use': i}, right_variables[1]: {'live': 1, 'next_use': i}}

                # for unary assignment and NOT operator
                elif len(operators) == 2 and len(variables) == 2:
                    line_variables = re.sub(
                        reserved_operators_pattern, '', lines[i]).split()
                    right_variable = line_variables[1]
                    left_variable = line_variables[0]
                    var_dict = {left_variable: {'live': -1, 'next_use': -1}, right_variable: {
                        'live': 1, 'next_use': i}}

                # for function call with equality sign
                elif len(operators) == 1 and len(variables) == 4:
                    left_variable = lines[i].split(" ")[0]
                    right_variable = lines[i].split(" ")[-1]
                    var_dict = {left_variable: {'live': -1, 'next_use': -1}, right_variable: {
                        'live': 1, 'next_use': i}}

                # simple assignment eg. a=b
                elif len(operators) == 1 and len(variables) == 2:
                    line_variables = re.sub(
                        reserved_operators_pattern, '', lines[i]).split()
                    right_variable = line_variables[1]
                    left_variable = line_variables[0]
                    var_dict = {left_variable: {'live': -1, 'next_use': -1}, right_variable: {
                        'live': 1, 'next_use': i}}

                else:
                    line = lines[i].split()
                    # print(line)
                    if line[0] == 'if' or line[0] == 'ifFalse':
                        right_variables = [line[1], line[3]]
                        var_dict = {right_variables[0]: {
                            'live': 1, 'next_use': i}, right_variables[1]: {'live': 1, 'next_use': i}}

                    elif line[0] == 'return' and len(line) > 1:
                        right_variables = [line[1]]
                        var_dict = {right_variables[0]: {
                            'live': 1, 'next_use': i}}

                    elif line[0] == 'input':
                        right_variables = [line[2]]
                        var_dict = {right_variables[0]: {
                            'live': 1, 'next_use': i}}

                    elif line[0] == 'output' or line[0] == 'call':
                        right_variables = [line[2]]
                        var_dict = {right_variables[0]: {
                            'live': 1, 'next_use': i}}

                    elif line[0] == 'param':
                        right_variables = [line[1]]
                        var_dict = {right_variables[0]: {
                            'live': 1, 'next_use': i}}

                    elif line[0] in reserved_all_dead_keywords.split():
                        left_variable = line[1]
                        var_dict = {left_variable: {
                            'live': -1, 'next_use': -1}}

                live_and_next_use.append(var_dict)
                live_and_next_use = list(reversed(live_and_next_use))

            live_and_next_use_blocks.append(live_and_next_use)

        data_segment = self.preamble(intermediate_code_final)

        code_segment = RegisterAllocation.RegisterAllocation().allocate_registers(
            blocks, live_and_next_use_blocks, data_segment, self.array_addresses, symbol_table, self.data_segment_dict)
        return code_segment
