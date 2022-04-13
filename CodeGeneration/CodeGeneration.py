from operator import indexOf
import re
from collections import defaultdict


class CodeGeneration:

    # registers_map = {
    #     'r0': '$t0',
    #     'r1': '$t1',
    #     'r2': '$t2',
    #     'r3': '$t3',
    #     'r4': '$t4',
    #     'r5': '$t5',
    #     'r6': '$t6',
    #     'r7': '$t7',
    #     'r8': '$s0',
    #     'r9': '$s1',
    #     'r10': '$s2',
    #     'r11': '$s3',
    #     'r12': '$s4',
    #     'r13': '$s5',
    #     'r14': '$s6',
    #     'r15': '$s7',
    #     'r16': '$t8',
    #     'r17': '$t9',
    # }

    registers_map = {
        '$t0': 'r0',
        '$t1': 'r1',
        '$t2': 'r2',
        '$t3': 'r3',
        '$t4': 'r4',
        '$t5': 'r5',
        '$t6': 'r6',
        '$t7': 'r7',
        '$s0': 'r8',
        '$s1': 'r9',
        '$s2': 'r10',
        '$s3': 'r11',
        '$s4': 'r12',
        '$s5': 'r13',
        '$s6': 'r14',
        '$s7': 'r15',
        '$t8': 'r16',
        '$t9': 'r17',
    }

    datatype_sizes = {
        'int': 4,
        'float': 4,
        'char': 1,
        'bool': 1,
    }

    # The set of all valid arithmetic operators
    arithmetic_operators = set("+ - * / % && || > < >= <= ! != = ==".split())

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

    def is_arithmetic_instruction_binary(self, instruction):
        instruction_set = set(instruction.split())
        # instruction_set contains all the operators and operands of the given line
        difference = instruction_set - self.arithmetic_operators
        # difference has only the operands as subtracting the set of arithmetic operators
        # i.e., taking the set difference, removes the operators, leaving the set of operands
        # print(difference, 'def')
        # In our TAC, only binary arithmetic type instrucitons have more than 2 operands
        # TODO: I feel slightly shaky about this, in case things go wrong, come back and check this
        if len(difference) > 2:
            return True
        return False

    def is_arithmetic_instruction_unary(self, instruction):
        instruction_set = set(instruction.split())
        difference = instruction_set.difference(self.arithmetic_operators)
        # Using similar logic as the previous function, unary arithmetic instructions have exactly 2 operands
        if len(difference) == 2:
            return True
        return False

    def is_function_call_with_return(self, instruction):
        if '=' in instruction and 'call' in instruction:
            return True
        return False

    def is_function_call_without_return(self, instruction):
        if 'call' in instruction and '=' not in instruction:
            return True
        return False

    def is_assignment_instruction(self, instruction):
        # The case of a simple assignment statement like a=b or f=10
        # In case the type casting is mentioned, replace it with '' using the following regex 
        instruction = re.sub(r'\(.+\)', '', instruction)
        if '=' in instruction and len(instruction.split()) == 3:
            return True
        return False

    def is_if_statement(self, instruction):
        if 'if' in instruction:
            return True
        return False

    def is_return_statement(self, instruction):
        if 'return' in instruction:
            return True
        return False

    def is_param_instruction(self, instruction):
        if 'param' in instruction:
            return True
        return False

    def is_input(self, instruction):
        if 'input' in instruction:
            return True
        return False

    def is_output(self, instruction):
        if 'output' in instruction:
            return True
        return False

    def is_array_initialization(self, instruction):
        data_types = "int float char bool string"
        try:
            # this identifies the pattern of an array initialization: int arr`2[24]
            if instruction.split()[0] in data_types and '[' in instruction.split()[1]:
                return True
            return False
        except IndexError:
            # occurs when you check for some other type of instruction but split()[1] does not exist
            return False

    def is_array_assignment(self, instruction):
        try:
            # this identifies the pattern of an array assignment: arr`2[4] = 2
            if '[' in instruction.split()[0] and instruction.split()[1] == '=':
                return True
            return False
        except IndexError:
            # occurs when you check for some other type of instruction but split()[1] does not exist
            return False

    def free_all(self):
        # Reinitialize the register_descriptor and address_descriptor
        self.register_descriptor = defaultdict(list)
        self.address_descriptor = defaultdict(list)

    def get_reg(self, live_and_next_use_blocks, index, variable):
        # TODO: Consider passing live_and_next_use_blocks[index] (basically just the block) instead of live_and_next_use_blocks, index
        """
        The get_reg function takes the live analysis information of the relevant block in live_and_next_use_blocks
        index is used to identify the block from this list
        variable identifies for which variable we are looking for a register
        returns a tuple (reg,0) or (reg,1) where reg is the name of the returned register that can be used
        and 0 indicates that the register was not spilled
        and 1 indicates that the register was spilled 
        Note: The spill is not handled within this function but needs to be handled in the generated code
        Note: The address descriptor and register descriptors are modified after returning the
        """

        # if the variable is already contained in some register
        # No need to spill. Just return that register
        for reg in self.register_descriptor:
            if reg in self.address_descriptor[variable]:
                return (reg, 0)

        # print(variable)

        # if there is an empty register available
        # No need to spill, just return that register
        for reg in self.registers_map:
            if not self.register_descriptor[reg]:
                return (reg, 0)

        # otherwise choose the register occupied by a temporary variable with no next use
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if var[0] == '~' and record[var]['next_use'] == -1:
                    # -1 indicates no next use
                    temp_var = var
                    for reg in self.register_descriptor[reg]:
                        if temp_var in self.register_descriptor[reg]:
                            self.register_descriptor[reg].remove(temp_var)
                            return (reg, 0)

        # else choose the register occupied by a non-temporary variable with no next use
        # spill the register
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if record[var]['next_use'] == -1:
                    temp_var = var
                    # TODO: Check the naming convention - inconsistent for variable in self.register_descriptor
                    for reg in self.register_descriptor[reg]:
                        if temp_var in self.register_descriptor[reg]:
                            self.register_descriptor[reg].remove(temp_var)
                            return (reg, 1)

        # else choose the register occupied by a temporary variable with the farthest nextuse
        # spill the register
        temp_with_farthest_next_use = ''
        farthest_next_use = -1
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if var[0] == '~' and record[var]['next_use'] > farthest_next_use:
                    farthest_next_use = record[var]['next_use']
                    temp_with_farthest_next_use = var
        if farthest_next_use != -1:
            for reg in self.register_descriptor:
                if temp_with_farthest_next_use in self.register_descriptor[reg]:
                    self.register_descriptor[reg].remove(
                        temp_with_farthest_next_use)
                    return (reg, 1)

        # else choose the register occupied by a non-temporary variable with the farthest nextuse
        # spill the register
        temp_with_farthest_next_use = ''
        farthest_next_use = -1
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if record[var]['next_use'] > farthest_next_use:
                    farthest_next_use = record[var]['next_use']
                    temp_with_farthest_next_use = var
        if farthest_next_use != -1:
            for reg in self.register_descriptor:
                if temp_with_farthest_next_use in self.register_descriptor[reg]:
                    self.register_descriptor[reg].remove(
                        temp_with_farthest_next_use)
                    return (reg, 1)

    # def get_float_reg(self, live_and_next_use_blocks, index, variable):

    def variable_in_register(self, variable):
        for reg in self.register_descriptor:
            for var in self.register_descriptor[reg]:
                if var == variable:
                    return reg
        return None

    def allocate_registers(self, blocks, live_and_next_use_blocks, data_segment):
        """
        allocate_registers function allocates registers and generates the MIPS code that is stored in the text_segment
        Note: The cases, i.e., the different types of statements are identified as using elifs in this function, 
        but this function is called inside generate_target_code() function
        """
        text_segment = ''
        variables_map = defaultdict()

        self.free_all()

        for block in blocks:
            lines = block.splitlines()

            lines_generator = (
                i for i in lines)
            # Just an iterator of the same length as the number of lines

            for line in lines_generator:

                if self.is_array_initialization(line):
                    # Extract the datatype of the initialized array: int arr`2[24]
                    data_type, size = line.split()[0], line.split()[
                        1].split('[')[1].split(']')[0]
                    num_of_elements = size//self.datatype_sizes[data_type]
                    # In our TAC for array initialization, after the declaration, there are num_of_elements lines of initialization
                    # These multiple lines have only constants which do not affect live analysis
                    # Hence we just skip these lines using the following for loop
                    for _ in range(num_of_elements):
                        next(lines_generator)

                # A label is a line that contains a colon
                elif ':' in line:
                    text_segment += line+'\n'

                elif line.startswith('goto'):
                    text_segment += f'j {line.split()[1]}\n'

                elif self.is_arithmetic_instruction_binary(line):
                    # Same as reg = [0,1,2] -> We just need to initialize the list with 3 elements
                    reg = [i for i in range(3)]
                    spill = [i for i in range(3)]  # Same as spill = [0,1,2]

                    subject, operand1, operand2 = line.split()[0], line.split()[
                        2], line.split()[4]
                    operator = line.split()[3]

                    reg[0], spill[0] = self.get_reg(
                        live_and_next_use_blocks, blocks.index(block), subject)
                    reg[1], spill[1] = self.get_reg(
                        live_and_next_use_blocks, blocks.index(block), operand1)
                    reg[2], spill[2] = self.get_reg(
                        live_and_next_use_blocks, blocks.index(block), operand2)

                    # If any of the registers is spilled, then spill the register
                    # Updating the address and rigister descriptors accordingly
                    for i in range(3):
                        if spill[i] == 1:
                            for var in self.register_descriptor[reg[i]]:
                                text_segment += f"sw {reg[i]}, {var}\n"
                                if reg[i] in self.address_descriptor[var]:
                                    self.address_descriptor[var].remove(reg[i])
                            self.register_descriptor[reg[i]] = []

                    # Corresponding MIPS code for the register spills
                    if spill[1] == 1:
                        text_segment += f"lw {reg[1]}, {operand1}\n"

                    if spill[2] == 1:
                        text_segment += f"lw {reg[2]}, {operand2}\n"

                    # TODO: check the operator - can we NOT use match as it requires Python 3.10 or higher
                    match operator:
                        case '+':
                            text_segment += f"add {reg[0]}, {reg[1]}, {reg[2]}\n"
                        case '-':
                            text_segment += f"sub {reg[0]}, {reg[1]}, {reg[2]}\n"
                        case '*':
                            text_segment += f"mult {reg[1]}, {reg[2]}\n"
                            text_segment += f"mflo {reg[0]}\n"
                        case '/':
                            text_segment += f"div {reg[1]}, {reg[2]}\n"
                            text_segment += f"mflo {reg[0]}\n"
                        case '%':
                            text_segment += f"div {reg[1]}, {reg[2]}\n"
                            text_segment += f"mfhi {reg[0]}\n"

                elif self.is_assignment_instruction(line):
                    # TODO: check for type casting
                    subject, operand = line.split()[0], line.split()[2]

                    reg0, spill0 = self.get_reg(
                        live_and_next_use_blocks, blocks.index(block), subject)

                    if spill0 == 1:
                        for var in self.register_descriptor[reg0]:
                            text_segment += f"sw {reg0}, {var}\n"
                            if reg0 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg0)
                        self.register_descriptor[reg0] = []

                    if operand.isdigit():
                        # the operand is an integer
                        operand = int(operand)
                        text_segment += f"li {reg0}, {operand}\n"
                        self.address_descriptor[subject].append(reg0)
                        self.register_descriptor[reg0].append(operand)
                    elif "'" in operand:
                        # The operand is a character
                        text_segment += f"li {reg0}, {operand}\n"
                        self.address_descriptor[subject].append(reg0)
                        self.register_descriptor[reg0].append(operand)
                    elif '"' in operand:
                        # The operand is a string
                        pass
                    else:
                        # float
                        # Need to handle everything differently for float type variables
                        pass

                elif self.is_arithmetic_instruction_unary(line):
                    # TODO: check for type casting
                    subject, operand = line.split()[0], line.split()[2]

                    reg0, spill0 = self.get_reg(
                        live_and_next_use_blocks, blocks.index(block), subject)

                    if spill0 == 1:
                        for var in self.register_descriptor[reg0]:
                            text_segment += f"sw {reg0}, {var}\n"
                            if reg0 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg0)
                        self.register_descriptor[reg0] = []

                    if operand.isdigit():
                        operand = int(operand)
                        text_segment += f"li {reg0}, {operand}\n"
                        text_segment += f"sub {reg0}, $zero, {reg0}\n"
                        self.address_descriptor[subject].append(reg0)
                        self.register_descriptor[reg0].append(operand)
                    else:
                        # float
                        pass

                elif self.is_array_assignment(line):
                    # arr[x] = b
                    array_name = line.split()[0].split('[')[0]
                    var_index = line.split()[0].split('[')[:-1]
                    data_type = self.array_addresses[array_name][1]

                    reg0, spill0 = self.get_reg(
                        live_and_next_use_blocks, blocks.index(block), var_index)
                    reg1, spill1 = self.get_reg(
                        live_and_next_use_blocks, blocks.index(block), line.split()[-1])

                    if spill0 == 1:
                        for var in self.register_descriptor[reg0]:
                            text_segment += f"sw {reg0}, {var}\n"
                            if reg0 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg0)
                        self.register_descriptor[reg0] = []

                    if spill1 == 1:
                        for var in self.register_descriptor[reg1]:
                            text_segment += f"sw {reg1}, {var}\n"
                            if reg1 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg1)
                        self.register_descriptor[reg1] = []

                    if data_type == 'float':
                        pass

                    else:
                        if var_index.isdigit():
                            pass
                        elif "'" in var_index:
                            pass
                        elif '"' in var_index:
                            pass
                        else:
                            # float
                            pass

        print('hello\n', text_segment)

        assembly_code = f"\n.text\n.globl start\n\n{text_segment}\n"
        return assembly_code

    def preamble(self, intermediate_code_final):

        # intermediate_code_final = 'b = 0\nc = 5\na = b + c\n'
        # intermediate_code_final = ''

        array_initializations = ''
        string_constants = ''
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

        self.free_all()

        assembly_code = f".data\n{array_initializations}\n\n{string_constants}\n"
        print(assembly_code)

        return assembly_code

    def generate_target_code(self, intermediate_code, optimization_level):

        if not intermediate_code:
            return

        # intermediate_code = "#L1:\ngoto #L3\n#L2:\n#L3:\n#L4:\n#L8:\ngoto #L4\ngoto #L8\nhello"
        # intermediate_code = "abc:\n\n\nif a == 5 goto L5\n"
        intermediate_code = f"b = 0\nc = 5\na = b + c\nb = a - c\nc = a {'%'} b"
        # intermediate_code = f"abc true\n iftrue\ntruecy"

        intermediate_code = re.sub(r'\btrue\b', '1', intermediate_code)
        intermediate_code = re.sub(r'\bfalse\b', '0', intermediate_code)

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
        # TODO: Check this case again-> what if someone else uses that label
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

        print(len(blocks))
        for x in blocks:
            print(x)
            print('----------------------------------------------------------------')

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
                # for arrays arr[i] -> i is dead implies arr[i] is dead and i is alive implies arr[i] is alive
                # for arrays we are removing the arr and proceeding with i for the live analysis
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

        # for x in live_and_next_use_blocks:
        #     for y in x:
        #         print(y)
        #     print()

        data_segment = self.preamble(intermediate_code_final)
        code_segment = self.allocate_registers(
            blocks, live_and_next_use_blocks, data_segment)

        return code_segment
