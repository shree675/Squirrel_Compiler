from operator import indexOf
import re
from collections import defaultdict


class CodeGeneration:

    registers_map = {
        'r0': '$t0',
        'r1': '$t1',
        'r2': '$t2',
        'r3': '$t3',
        'r4': '$t4',
        'r5': '$t5',
        'r6': '$t6',
        'r7': '$t7',
        'r8': '$s0',
        'r9': '$s1',
        'r10': '$s2',
        'r11': '$s3',
        'r12': '$s4',
        'r13': '$s5',
        'r14': '$s6',
        'r15': '$s7',
        'r16': '$t8',
        'r17': '$t9',
    }

    datatype_sizes = {
        'int': 4,
        'float': 4,
        'char': 1,
        'bool': 1,
    }

    def __init__(self):
        self.register_descriptor = defaultdict(list)
        self.address_descriptor = defaultdict(list)
        self.return_string_count = 0
        self.array_addresses = defaultdict()

    def allocate_registers(self, blocks, live_and_next_use_blocks, intermediate_code_final):

        array_initializations = ''
        string_constants = ''
        text_segment = ''
        data_types = "int float char bool string"

        intermediate_code_generator = (
            i for i in intermediate_code_final.splitlines())

        for line in intermediate_code_generator:
            if "\"" in line:
                tokens = line.split()
                string_const = ""
                string_var = ""
                if '=' in tokens:
                    string_const = tokens[-1]
                    string_var = tokens[tokens.index('=') - 1]
                else:
                    string_var = 'return'+str(self.return_string_count)
                    self.return_string_count += 1
                    string_const = tokens[-1]
                string_constants += f'{string_var}:\n\t.asciiz {string_const}\n'

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
                        array, tokens[0])

        for array_var in self.array_addresses:
            array_initializations += f'\t{array_var}:\n'
            if self.array_addresses[array_var][1] == 'int' or self.array_addresses[array_var][1] == 'float':
                array_initializations += f'\t\t.word '
            elif self.array_addresses[array_var][1] == 'char' or self.array_addresses[array_var][1] == 'bool':
                array_initializations += f'\t\t.byte '
            for i in range(len(self.array_addresses[array_var][0])):
                if self.array_addresses[array_var][1] == 'bool':
                    array_initializations += f'1, ' if self.array_addresses[array_var][0][i].strip(
                    ) == 'true' else f'0, '
                else:
                    array_initializations += f'{self.array_addresses[array_var][0][i].strip()}, '
            array_initializations = array_initializations[:-2] + '\n'

        assembly_code = f".data\n{array_initializations}\n\n{string_constants}\n\n.text\n.globl start\n\n{text_segment}\n"

        print(assembly_code)

    @ staticmethod
    def generate_target_code(intermediate_code):

        if not intermediate_code:
            return

        # intermediate_code = "#L1:\ngoto #L3\n#L2:\n#L3:\n#L4:\n#L8:\ngoto #L4\ngoto #L8\nhello"
        # intermediate_code = "abc:\n\n\nif a == 5 goto L5\n"

        goto_labels = set()
        for lines in intermediate_code.splitlines():
            if 'goto' in lines:
                goto_labels.add(lines.split(' ')[-1])

        # print(goto_labels)

        optimized_code1 = ""
        for lines in intermediate_code.splitlines():
            if lines.startswith('#L') and lines.split(':')[0] not in goto_labels:
                pass
            else:
                optimized_code1 += lines + '\n'

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

        # print(redundant_labels)
        for label in redundant_labels.keys():
            for l in redundant_labels[label]:
                optimized_code2 = optimized_code2.replace(l+':', '')
                optimized_code2 = optimized_code2.replace(l, label)

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

        optimized_code4 = ""
        optimized_code_list = optimized_code3.splitlines()
        i = 0
        while i < len(optimized_code_list):
            lines = optimized_code_list[i]
            if lines.startswith('goto'):
                label = lines.split(' ')[-1]
                if optimized_code_list[i+1].startswith('#L') and optimized_code_list[i+1].split(':')[0] == label:
                    i += 1
                else:
                    optimized_code4 += lines+'\n'
            else:
                optimized_code4 += lines+'\n'
            i += 1

        # print(optimized_code4)
        intermediate_code_final = optimized_code4

        blocks = []
        block_line = ""
        prev = False
        first_label_seen = False
        for lines in intermediate_code_final.splitlines():
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
            else:
                block_line += lines+'\n'
        if block_line != "":
            blocks.append(block_line)

        # print(len(blocks))
        # for x in blocks:
        #     print(x)
        #     print('----------------------------------------------------------------')

        """
        -1 -> either dead or no next use
        1 -> live
        """
        reserved_operators_pattern = r"\+|\-|\*|\/|%|&&|\|\||>|<|>=|<=|\!|\!=|=|=="
        reserved_operators = "+ - * / % && || > < >= <= ! != = =="
        reserved_all_live_keywords = "if return ifFalse input output call param"
        reserved_all_dead_keywords = "int float string bool char"
        reserved_words = set(reserved_operators.split())
        live_and_next_use_blocks = []

        for block in blocks:
            num_lines = len(block.split('\n'))
            lines = re.sub(r"\(.+\)", '', block).split('\n')
            live_and_next_use = []

            for i in range(num_lines-1, -1, -1):

                if lines[i].startswith('goto') or ':' in lines[i] or len(lines[i].strip()) == 0:
                    continue

                temp = lines[i].split(' ')
                for index, word in enumerate(temp):
                    if ']' in word:
                        temp[index] = re.sub(r'.*\[(.+)\]', r'\1', word)

                lines[i] = ' '.join(temp)

                variables = set(lines[i].split())-reserved_words
                # print(variables)
                operators = set(lines[i].split())-variables
                # print(operators)

                var_dict = {}

                if len(operators) == 2 and len(variables) == 3:
                    line_variables = re.sub(
                        reserved_operators_pattern, '', lines[i]).split()
                    right_variables = line_variables[1:]
                    left_variable = line_variables[0]
                    var_dict = {left_variable: {'live': -1, 'next_use': -1}, right_variables[0]: {
                        'live': 1, 'next_use': i}, right_variables[1]: {'live': 1, 'next_use': i}}

                elif len(operators) == 2 and len(variables) == 2:
                    line_variables = re.sub(
                        reserved_operators_pattern, '', lines[i]).split()
                    right_variable = line_variables[1]
                    left_variable = line_variables[0]
                    var_dict = {left_variable: {'live': -1, 'next_use': -1}, right_variable: {
                        'live': 1, 'next_use': i}}

                elif len(operators) == 1 and len(variables) == 4:
                    left_variable = lines[i].split(" ")[0]
                    right_variable = lines[i].split(" ")[-1]
                    var_dict = {left_variable: {'live': -1, 'next_use': -1}, right_variable: {
                        'live': 1, 'next_use': i}}

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

        # for x in live_and_next_use_blocks:
        #     for y in x:
        #         print(y)
        #     print()
        return blocks, live_and_next_use_blocks, intermediate_code_final
