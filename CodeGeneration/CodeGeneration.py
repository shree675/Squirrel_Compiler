from operator import indexOf
import re
from collections import defaultdict
import os


class CodeGeneration:

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

    # 22 registers are available for use
    floating_point_registers_map = {
        '$f1': '$f1',
        '$f3': '$f3',
        '$f4': '$f4',
        '$f5': '$f5',
        '$f6': '$f6',
        '$f7': '$f7',
        '$f8': '$f8',
        '$f9': '$f9',
        '$f10': '$f10',
        '$f11': '$f11',
        '$f20': '$f20',
        '$f21': '$f21',
        '$f22': '$f22',
        '$f23': '$f23',
        '$f24': '$f24',
        '$f25': '$f25',
        '$f26': '$f26',
        '$f27': '$f27',
        '$f28': '$f28',
        '$f29': '$f29',
        '$f30': '$f30',
        '$f31': '$f31',
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

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    # started
    def is_arithmetic_instruction_binary(self, instruction):
        instruction_set = set(instruction.split())
        # instruction_set contains all the operators and operands of the given line
        intersection = instruction_set.intersection(self.arithmetic_operators)
        # intersection has only the operands as the set of arithmetic operators
        # In our TAC, only binary arithmetic type instrucitons have more than 2 operands
        if len(intersection) == 2:
            return True
        return False

    # started
    def is_arithmetic_instruction_unary(self, instruction):
        instruction_set = set(instruction.split())
        difference = instruction_set.difference(self.arithmetic_operators)
        # Using similar logic as the previous function, unary arithmetic instructions have exactly 2 operands
        if len(difference) == 2:
            return True
        return False

    def is_function_call_with_return(self, instruction):
        words = instruction.split()
        if words[1] == "=" and words[2] == 'call':
            return True
        return False

    def is_function_call_without_return(self, instruction):
        words = instruction.split()
        if words[0] == "call":
            return True
        return False

    # started
    def is_assignment_instruction(self, instruction):
        # The case of a simple assignment statement like a=b or f=10
        # In case the type casting is mentioned, replace it with '' using the following regex
        instruction = re.sub(r'\(.+\)', '', instruction)
        if '=' in instruction and len(instruction.split()) == 3:
            return True
        return False

    # started
    def is_if_statement(self, instruction):
        if instruction and (instruction.split()[0] == 'if' or instruction.split()[0] == 'ifFalse'):
            return True
        return False

    def is_return_statement(self, instruction):
        if instruction and instruction.split()[0] == 'return':
            return True
        return False

    def is_param_instruction(self, instruction):
        if instruction and instruction.split()[0] == 'param':
            return True
        return False

    def is_input(self, instruction):
        if instruction and instruction.split()[0] == 'input':
            return True
        return False

    # started
    def is_output(self, instruction):
        if instruction and instruction.split()[0] == 'output':
            return True
        return False

    # started
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

    # started
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

    def get_reg(self, is_float, live_and_next_use_blocks, index, variable):
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
        if is_float:
            for reg in self.register_descriptor:
                if 'f' in reg and reg in self.address_descriptor[variable]:
                    return (reg, 0)
        else:
            for reg in self.register_descriptor:
                if reg in self.address_descriptor[variable]:
                    return (reg, 0)

        # if there is an empty register available
        # No need to spill, just return that register
        if is_float:
            for reg in self.floating_point_registers_map:
                if self.register_descriptor[reg] == []:
                    return (reg, 0)
        else:
            for reg in self.registers_map:
                if not self.register_descriptor[reg]:
                    return (reg, 0)

        # otherwise choose the register occupied by a temporary variable with no next use
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if var[0] == '~' and record[var]['next_use'] == -1:
                    # -1 indicates no next use
                    temp_var = var
                    for reg in self.register_descriptor:
                        if is_float and 'f' in reg:
                            if temp_var in self.register_descriptor[reg]:
                                self.register_descriptor[reg].remove(temp_var)
                                return (reg, 0)
                        else:
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
                    for reg in self.register_descriptor:
                        if is_float and 'f' in reg:
                            if temp_var in self.register_descriptor[reg]:
                                self.register_descriptor[reg].remove(temp_var)
                                self.address_descriptor[temp_var].append(reg)
                                return (reg, 1)
                        else:
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
                if is_float and 'f' in reg:
                    if temp_with_farthest_next_use in self.register_descriptor[reg]:
                        self.register_descriptor[reg].remove(
                            temp_with_farthest_next_use)
                        return (reg, 1)
                else:
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
                if is_float and 'f' in reg:
                    if temp_with_farthest_next_use in self.register_descriptor[reg]:
                        self.register_descriptor[reg].remove(
                            temp_with_farthest_next_use)
                        return (reg, 1)
                else:
                    if temp_with_farthest_next_use in self.register_descriptor[reg]:
                        self.register_descriptor[reg].remove(
                            temp_with_farthest_next_use)
                        return (reg, 1)

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
                line = re.sub(r'#', '_', line)

                if self.is_array_initialization(line):
                    # Extract the datatype of the initialized array: int arr`2[24]
                    data_type, size = line.split()[0], line.split()[
                        1].split('[')[1].split(']')[0]
                    num_of_elements = int(
                        size)//int(self.datatype_sizes[data_type])
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

                # there will be no type casting involved here
                elif self.is_arithmetic_instruction_binary(line):
                    # Same as reg = [0,1,2] -> We just need to initialize the list with 3 elements
                    reg = [i for i in range(3)]
                    spill = [i for i in range(3)]  # Same as spill = [0,1,2]

                    subject, operand1, operand2 = line.split()[0], line.split()[
                        2], line.split()[4]
                    operator = line.split()[3]

                    if '[' in operand1:
                        array_name = operand1.split('[')[0]
                        var_index = operand1.split('[')[1].split(']')[0]
                        reg[1], spill[1] = self.get_reg(False,
                                                        live_and_next_use_blocks, blocks.index(block), var_index)
                        if spill[1] == 1:
                            for var in self.register_descriptor[reg[1]]:
                                text_segment += f"sw {reg[1]}, {var}\n"
                                if reg[1] in self.address_descriptor[var]:
                                    self.address_descriptor[var].remove(reg[1])
                            self.register_descriptor[reg[1]] = []
                            text_segment += f"lw {reg[1]}, {var_index}\n"
                            self.address_descriptor[var_index].append(
                                reg[1])
                            self.register_descriptor[reg[1]].append(
                                var_index)
                        text_segment += f"lw {reg[1]}, {array_name}({reg[1]})\n"

                    if '[' in operand2:
                        array_name = operand2.split('[')[0]
                        var_index = operand2.split('[')[1].split(']')[0]
                        reg[2], spill[1] = self.get_reg(False,
                                                        live_and_next_use_blocks, blocks.index(block), var_index)
                        if spill[2] == 1:
                            for var in self.register_descriptor[reg[2]]:
                                text_segment += f"sw {reg[2]}, {var}\n"
                                if reg[2] in self.address_descriptor[var]:
                                    self.address_descriptor[var].remove(reg[2])
                            self.register_descriptor[reg[2]] = []
                            text_segment += f"lw {reg[2]}, {var_index}\n"
                            self.address_descriptor[var_index].append(
                                reg[2])
                            self.register_descriptor[reg[2]].append(
                                var_index)
                        text_segment += f"lw {reg[2]}, {array_name}({reg[2]})\n"

                    reg[0], spill[0] = self.get_reg(False,
                                                    live_and_next_use_blocks, blocks.index(block), subject)
                    flag = False
                    if reg[1] == 1:
                        reg[1], spill[1] = self.get_reg(False,
                                                        live_and_next_use_blocks, blocks.index(block), operand1)
                        flag = True
                    if reg[2] == 2:
                        reg[2], spill[2] = self.get_reg(False,
                                                        live_and_next_use_blocks, blocks.index(block), operand2)
                        flag = True

                        # If any of the registers is spilled, then spill the register
                        # Updating the address and rigister descriptors accordingly

                    # TODO: check and fix this part
                    if flag:
                        for i in range(3):
                            if spill[i] == 1:
                                for var in self.register_descriptor[reg[i]]:
                                    text_segment += f"sw {reg[i]}, {var}\n"
                                    if reg[i] in self.address_descriptor[var]:
                                        self.address_descriptor[var].remove(
                                            reg[i])
                                self.register_descriptor[reg[i]] = []
                                if i == 1:
                                    text_segment += f"lw {reg[i]}, {operand1}\n"
                                    self.address_descriptor[operand1].append(
                                        reg[i])
                                    self.register_descriptor[reg[i]].append(
                                        operand1)
                                elif i == 2:
                                    text_segment += f"lw {reg[i]}, {operand2}\n"
                                    self.address_descriptor[operand1].append(
                                        reg[i])
                                    self.register_descriptor[reg[i]].append(
                                        operand1)

                    if operand1.isdigit():
                        text_segment += f"addi {reg[1]}, $zero, {operand1}\n"
                    if operand2.isdigit():
                        text_segment += f"addi {reg[2]}, $zero, {operand2}\n"

                    if operator == '+':
                        text_segment += f"add {reg[0]}, {reg[1]}, {reg[2]}\n"
                    elif operator == '-':
                        text_segment += f"sub {reg[0]}, {reg[1]}, {reg[2]}\n"
                    elif operator == '*':
                        text_segment += f"mult {reg[1]}, {reg[2]}\n"
                        text_segment += f"mflo {reg[0]}\n"
                    elif operator == '/':
                        text_segment += f"div {reg[1]}, {reg[2]}\n"
                        text_segment += f"mflo {reg[0]}\n"
                    elif operator == '%':
                        text_segment += f"div {reg[1]}, {reg[2]}\n"
                        text_segment += f"mfhi {reg[0]}\n"

                    # TODO: check and fix this for arrays
                    self.register_descriptor[reg[0]].append(subject)
                    self.address_descriptor[subject].append(reg[0])
                    self.register_descriptor[reg[1]].append(operand1)
                    self.register_descriptor[reg[2]].append(operand2)

                elif self.is_array_assignment(line):
                    array_name = line.split()[0].split('[')[0]
                    # var_index will never be a constant in the TAC
                    var_index = line.split()[0].split('[')[1][:-1]
                    data_type = self.array_addresses[array_name][1]

                    reg0, spill0 = self.get_reg(False,
                                                live_and_next_use_blocks, blocks.index(block), var_index)
                    reg1, spill1 = self.get_reg(False,
                                                live_and_next_use_blocks, blocks.index(block), line.split()[-1])

                    if spill0 == 1:
                        for var in self.register_descriptor[reg0]:
                            text_segment += f"sw {reg0}, {var}\n"
                            if reg0 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg0)
                        self.register_descriptor[reg0] = []
                        text_segment += f"lw {reg0}, {var_index}\n"
                        self.register_descriptor[reg0].append(var_index)
                        self.address_descriptor[var_index].append(reg0)

                    if spill1 == 1:
                        for var in self.register_descriptor[reg1]:
                            text_segment += f"sw {reg1}, {var}\n"
                            if reg1 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg1)
                        self.register_descriptor[reg1] = []
                        text_segment += f"lw {reg1}, {line.split()[1]}\n"
                        self.register_descriptor[reg1].append(line.split()[1])
                        self.address_descriptor[line.split()[1]].append(reg1)

                    if data_type == 'float':
                        pass

                    else:
                        self.address_descriptor[var_index].append(reg0)
                        self.register_descriptor[reg0].append(var_index)
                        text_segment += f"sw {reg1}, {array_name}({reg0})\n"

                elif self.is_assignment_instruction(line):
                    # TODO: check for type casting
                    subject, operand = 0, 0

                    if '(' in line:
                        subject, operand, cast_type = line.split()[0], line.split()[
                            3], line.split()[2]

                        if cast_type == 'int':
                            # if operand is char and cast type is int, do nohting because mips will take care of it

                            # here, we just need to check if the operand is a float or not
                            # if the operand is not float, do nothing
                            pass

                        elif cast_type == 'float':
                            pass

                    else:
                        subject, operand = line.split()[0], line.split()[2]

                    reg0, spill0 = self.get_reg(False,
                                                live_and_next_use_blocks, blocks.index(block), subject)

                    # TODO: spill correctly
                    if spill0 == 1:
                        for var in self.register_descriptor[reg0]:
                            text_segment += f"sw {reg0}, {var}\n"
                            if reg0 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg0)
                        self.register_descriptor[reg0] = []

                    if self.isfloat(operand):
                        # the operand is a float constant
                        freg0, spill0 = self.get_reg(
                            True, live_and_next_use_blocks, blocks.index(block), subject)
                        if spill0 == 1:
                            for var in self.register_descriptor[freg0]:
                                text_segment += f"s.s {freg0}, {var}\n"
                                if freg0 in self.address_descriptor[var]:
                                    self.address_descriptor[var].remove(freg0)
                            self.register_descriptor[freg0] = []
                        text_segment += f"li.s {freg0}, {operand}\n"
                        self.register_descriptor[freg0].append(subject)
                        self.address_descriptor[subject].append(freg0)
                    elif operand.isdigit():
                        # the operand is an integer
                        operand = int(operand)
                        text_segment += f"li {reg0}, {operand}\n"
                        self.address_descriptor[subject].append(reg0)
                        self.register_descriptor[reg0].append(subject)
                    elif "'" in operand:
                        # The operand is a character
                        text_segment += f"li {reg0}, {operand}\n"
                        self.address_descriptor[subject].append(reg0)
                        self.register_descriptor[reg0].append(subject)
                    elif '"' in operand:
                        # The operand is a string
                        pass
                    else:
                        # if it is a variable
                        reg1, spill1 = self.get_reg(False,
                                                    live_and_next_use_blocks, blocks.index(block), operand)

                        if spill1 == 1:
                            for var in self.register_descriptor[reg1]:
                                text_segment += f"sw {reg1}, {var}\n"
                                if reg1 in self.address_descriptor[var]:
                                    self.address_descriptor[var].remove(reg1)
                            self.register_descriptor[reg1] = []
                            text_segment += f"lw {reg1}, {operand}\n"
                            self.address_descriptor[operand].append(reg1)
                            self.register_descriptor[reg1].append(operand)

                        self.address_descriptor[subject].append(reg0)
                        self.register_descriptor[reg0].append(subject)
                        self.address_descriptor[operand].append(reg1)
                        self.register_descriptor[reg1].append(operand)

                        text_segment += f"addi {reg0}, {reg1}, 0\n"

                elif self.is_arithmetic_instruction_unary(line):
                    # TODO: check for type casting
                    print("line : ", line)
                    subject, operand = line.split()[0], line.split()[2]

                    reg0, spill0 = self.get_reg(False,
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
                        self.register_descriptor[reg0].append(subject)
                    else:
                        # float
                        pass

                elif self.is_if_statement(line):
                    # TODO: check if left, right are floats
                    # the operands are never constants
                    if_stmt, left, operator, right, label = line.split()[0], line.split(
                    )[1], line.split()[2], line.split()[3], line.split()[-1]

                    reg = [i for i in range(3)]
                    spill = [0, 0, 0]

                    reg[0], spill[0] = self.get_reg(False,
                                                    live_and_next_use_blocks, blocks.index(block), left)
                    reg[1], spill[1] = self.get_reg(False,
                                                    live_and_next_use_blocks, blocks.index(block), right)
                    reg[2], spill[2] = self.get_reg(False,
                                                    live_and_next_use_blocks, blocks.index(block), "~")

                    for i in range(3):
                        if spill[i] == 1:
                            for var in self.register_descriptor[reg[i]]:
                                text_segment += f"sw {reg[i]}, {var}\n"
                                if reg[i] in self.address_descriptor[var]:
                                    self.address_descriptor[var].remove(
                                        reg[i])
                            self.register_descriptor[reg[i]] = []
                            text_segment += f"lw {reg[i]}, {left}\n" if i == 0 else f"lw {reg[i]}, {right}\n" if i == 1 else f""
                            self.address_descriptor[left].append(reg[i]) if i == 0 else self.address_descriptor[
                                right].append(reg[i]) if i == 1 else None
                            self.register_descriptor[reg[i]].append(left) if i == 0 else self.register_descriptor[
                                reg[i]].append(right) if i == 1 else None

                    self.address_descriptor[left].append(reg[0])
                    self.register_descriptor[reg[0]].append(left)

                    self.address_descriptor[right].append(reg[1])
                    self.register_descriptor[reg[1]].append(right)

                    if if_stmt == 'if':
                        if operator == '<=':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '>=':
                            text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '<':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '>':
                            text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '==':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"beq {reg[2]}, $zero, {label}\n"
                        elif operator == '!=':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"bne {reg[2]}, $zero, {label}\n"

                    else:
                        if operator == '>':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '<':
                            text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '>=':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '<=':
                            text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '!=':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"beq {reg[2]}, $zero, {label}\n"
                        elif operator == '==':
                            text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            text_segment += f"bne {reg[2]}, $zero, {label}\n"

                elif self.is_return_statement(line):
                    num_words = len(line.split())
                    var_name = line.split()[-1]

                    # reg: [set of variables]
                    # var: [list of reigsters]

                    if num_words > 1:
                        # return with value
                        # TODO : get the register from the variable descriptor
                        # for reg in self.register_descriptor
                        text_segment += f"lw $v0, {line.split()[1]}\n"
                        pass

                    text_segment += f"jr $ra\n"

                elif self.is_output(line):
                    data_type, variable = line.split()[1][:-1], line.split()[2]
                    array_name = None

                    if '[' in variable:
                        array_name = variable.split('[')[0]
                        variable = variable.split('[')[1][:-1]

                    reg0, spill0 = self.get_reg(False,
                                                live_and_next_use_blocks, blocks.index(block), variable)

                    if spill0 == 1:
                        for var in self.register_descriptor[reg0]:
                            text_segment += f"sw {reg0}, {var}\n"
                            if reg0 in self.address_descriptor[var]:
                                self.address_descriptor[var].remove(reg0)
                        self.register_descriptor[reg0] = []
                        text_segment += f"lw {reg0}, {variable}\n"

                    if data_type == 'int':
                        text_segment += f"li $v0, 1\n"
                        if array_name == None:
                            text_segment += f"la $a0, 0({reg0})\n"
                        else:
                            text_segment += f"lw $a0, {array_name}({reg0})\n"
                        text_segment += f"syscall\n"
                        text_segment += f"addi $a0, $0, 0xA\n"
                        text_segment += f"addi $v0, $0, 0xB\n"
                        text_segment += f"syscall\n"

            # for reg in self.register_descriptor:
            #     for var in self.register_descriptor[reg]:
            #         if '~' not in var:
            #             text_segment += f"sw {reg}, {var}\n"
            #             if reg in self.address_descriptor[var]:
            #                 self.address_descriptor[var].remove(reg)

        assembly_code = f".text\n.globl main\n\n{text_segment}\n"
        assembly_code = re.sub('start:', 'main:', assembly_code)

        return assembly_code

    def preamble(self, intermediate_code_final):

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

        self.free_all()

        assembly_code = f".data\n{array_initializations}{string_constants}\n"

        return assembly_code

    def generate_target_code(self, intermediate_code, optimization_level):

        if not intermediate_code:
            return

        # intermediate_code = "#L1:\ngoto #L3\n#L2:\n#L3:\n#L4:\n#L8:\ngoto #L4\ngoto #L8\nhello"
        # intermediate_code = "abc:\n\n\nif a == 5 goto L5\n"
        # intermediate_code = f"x = 5\narr[x] = 0\n"
        # intermediate_code = f"abc true\n iftrue\ntruecy"

        intermediate_code = re.sub(r'\btrue\b', '1', intermediate_code)
        intermediate_code = re.sub(r'\bfalse\b', '0', intermediate_code)
        intermediate_code = re.sub(r'`', '__', intermediate_code)
        intermediate_code = re.sub(r'~', '__', intermediate_code)

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
        f = open("Output/test.asm", "w")
        f.write(data_segment+code_segment)
        f.close()
        return code_segment
