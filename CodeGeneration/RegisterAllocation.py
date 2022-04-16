
import re
from collections import defaultdict
import os


class RegisterAllocation:

    # registers_map = {
    #     '$t0': 'r0',
    #     '$t1': 'r1',
    #     '$t2': 'r2',
    #     '$t3': 'r3',
    #     '$t4': 'r4',
    #     '$t5': 'r5',
    #     '$t6': 'r6',
    #     '$t7': 'r7',
    #     '$s0': 'r8',
    #     '$s1': 'r9',
    #     '$s2': 'r10',
    #     '$s3': 'r11',
    #     '$s4': 'r12',
    #     '$s5': 'r13',
    #     '$s6': 'r14',
    #     '$s7': 'r15',
    #     '$t8': 'r16',
    #     '$t9': 'r17',
    # }

    registers_map = {
        '$t0': 'r0',
        '$t1': 'r1',
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
        # TODO: change the structure of register_descriptor
        self.register_descriptor = defaultdict(list)
        self.address_descriptor = {}
        self.offset = 4

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
        self.address_descriptor = {}

    def get_reg(self, is_float, live_and_next_use_blocks, index, variable):
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
                if 'f' in reg and reg in self.address_descriptor[variable]['registers']:
                    return (reg, 0)
        else:
            for reg in self.register_descriptor:
                if reg in self.address_descriptor[variable]['registers']:
                    return (reg, 0)

        # if there is an empty register available
        # No need to spill, just return that register
        # TODO: handle the case when the register is not available
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
                if (var[0] == '~' or var[0] == '_') and record[var]['next_use'] == -1:
                    # -1 indicates no next use
                    temp_var = var
                    for reg in self.register_descriptor:
                        if is_float and 'f' in reg:
                            if temp_var in self.register_descriptor[reg]:
                                self.register_descriptor[reg].remove(temp_var)
                                return (reg, 1)
                        else:
                            if temp_var in self.register_descriptor[reg]:
                                self.register_descriptor[reg].remove(temp_var)
                                return (reg, 1)

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
                                self.address_descriptor[temp_var]['registers'].append(
                                    reg)
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
                if (var[0] == '~' or var[0] == '_') and record[var]['next_use'] > farthest_next_use:
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

    def spill_reg(self, register):
        for var in self.register_descriptor[register]:
            try:
                offset = self.address_descriptor[var]['offset']
                text_segment += f"sw {register}, {offset}($s8)\n"
                self.address_descriptor[var]['registers'].remove(register)
            except KeyError:
                self.offset -= 4
                text_segment += f"addi $sp, $sp, -4\n"
                text_segment += f"sw {register}, 4($sp)\n"
                self.address_descriptor.push({
                    var: {
                        'offset': self.offset,
                        'registers': []
                    }
                })
        self.register_descriptor[register] = []

    def update_descriptors(self, register, variable):
        self.register_descriptor[register].append(variable)
        try:
            self.address_descriptor[variable] = {
                variable: {
                    'offset': self.address_descriptor[variable]['offset'],
                    'registers': self.address_descriptor[variable]['registers'].append(register)
                }
            }
        except KeyError:
            self.offset -= 4
            self.address_descriptor.push({
                variable: {
                    'offset': self.offset,
                    'registers': [register]
                }
            })

    def allocate_registers(self, blocks, live_and_next_use_blocks, data_segment, array_addresses):
        """
        allocate_registers function allocates registers and generates the MIPS code that is stored in the text_segment
        Note: The cases, i.e., the different types of statements are identified as using elifs in this function, 
        but this function is called inside generate_target_code() function
        """
        text_segment = ''

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
                    if line[0] == '_':
                        pass
                    else:
                        self.offset = 0
                        line += f"mov $s8, $sp\n"

                    text_segment += line+'\n'

                elif line.startswith('goto'):
                    text_segment += f'j {line.split()[1]}\n'

                elif self.is_assignment_instruction(line):
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

                    if spill0 == 1:
                        self.spill_reg(reg0)

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
                        self.address_descriptor[subject]['registers'].append(
                            freg0)
                    elif operand.isdigit():
                        # the operand is an integer
                        operand = int(operand)
                        text_segment += f"li {reg0}, {operand}\n"
                        self.update_descriptors(reg0, subject)
                    elif "'" in operand:
                        # The operand is a character
                        text_segment += f"li {reg0}, {operand}\n"
                        self.address_descriptor[subject]['registers'].append(
                            reg0)
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

                        self.address_descriptor[subject]['registers'].append(
                            reg0)
                        self.register_descriptor[reg0].append(subject)
                        self.address_descriptor[operand]['registers'].append(
                            reg1)
                        self.register_descriptor[reg1].append(operand)

                        text_segment += f"addi {reg0}, {reg1}, 0\n"

        assembly_code = f".text\n.globl main\n\n{text_segment}\n"
        assembly_code = re.sub('start:', 'main:', assembly_code)

        return assembly_code
