
from atexit import register
from ctypes import addressof
import re
from collections import defaultdict
import os

default_reg_des = {
    '$t0': None,
    '$t1': None,
    '$t2': None,
    '$t3': None,
    '$t4': None,
    '$t5': None,
    '$t6': None,
    '$t7': None,
    '$s0': None,
    '$s1': None,
    '$s2': None,
    '$s3': None,
    '$s4': None,
    '$s5': None,
    '$s6': None,
    '$s7': None,
    '$t8': None,
    '$t9': None,
}


class RegisterAllocation:

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

    # registers_map = {
    #     '$t0': 'r0',
    #     '$t1': 'r1',
    #     '$t2': 'r2',
    #     '$t3': 'r3'
    # }

    reserved_registers = {'$ra', '$s8', '$v0'}

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
        # We should add float registers as well
        self.register_descriptor = default_reg_des.copy()
        self.address_descriptor = {}
        self.offset = 4
        self.text_segment = ''

    def isfloat(self, num):
        try:
            float(num)

        except ValueError:
            return False
        return True

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
        #print("instruction : " , instruction)
        words = instruction.split()
        if len(words) < 5:
            return False
        if words[1] == "=" and words[2] == 'call':
            return True
        return False

    def is_function_call_without_return(self, instruction):
        words = instruction.split()
        if len(words) < 3:
            return False
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
        # We should add float registers as well
        self.register_descriptor = default_reg_des.copy()
        self.address_descriptor = {}
        self.offset = 4

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

        # return  -> (reg, spill?, update_des?)

        # if the variable is already contained in some register
        # No need to spill. Just return that register
        if is_float:
            for reg in self.register_descriptor:
                if 'f' in reg and reg in self.address_descriptor[variable]['registers']:
                    return (reg, 0, 0)
        else:
            for reg in self.register_descriptor:
                if variable in self.address_descriptor and reg in self.address_descriptor[variable]['registers']:
                    return (reg, 0, 0)

        # if there is an empty register available
        # No need to spill, just return that register

        if is_float:
            for reg in self.floating_point_registers_map:
                if reg in self.register_descriptor and self.register_descriptor[reg] == None:
                    return (reg, 0, 1)
        else:
            for reg in self.registers_map:
                if reg in self.register_descriptor and self.register_descriptor[reg] == None:
                    return (reg, 0, 1)

        """ The Remaining cases are the ones that involves SPILL"""
        # otherwise choose the register occupied by a temporary variable with no next use
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if (var[0] == '~' or var[0] == '_') and record[var]['next_use'] == -1:
                    # -1 indicates no next use
                    temp_var = var
                    for reg in self.register_descriptor:
                        if is_float and 'f' in reg:
                            if temp_var == self.register_descriptor[reg]:
                                # self.register_descriptor[reg].remove(temp_var)
                                return (reg, 1, 1)
                        else:
                            if temp_var == self.register_descriptor[reg]:
                                # self.register_descriptor[reg].remove(temp_var)
                                return (reg, 1, 1)
                    # return (reg,1,1) # Not sure if I need to return temp_ var

        # else choose the register occupied by a non-temporary variable with no next use
        # spill the register
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if record[var]['next_use'] == -1:
                    temp_var = var
                    # TODO: Check the naming convention - inconsistent for variable in self.register_descriptor
                    for reg in self.register_descriptor:
                        if is_float and 'f' in reg:
                            if reg in self.register_descriptor and temp_var == self.register_descriptor[reg]:
                                # self.register_descriptor[reg].remove(temp_var)
                                # self.address_descriptor[temp_var]['registers'].append(reg)
                                return (reg, 1, 1)
                        else:
                            if reg in self.register_descriptor and temp_var == self.register_descriptor[reg]:
                                # self.register_descriptor[reg].remove(temp_var)
                                return (reg, 1, 1)

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
                    if temp_with_farthest_next_use == self.register_descriptor[reg]:
                        # self.register_descriptor[reg].remove(
                        #     temp_with_farthest_next_use)
                        return (reg, 1, 1)
                else:
                    if temp_with_farthest_next_use == self.register_descriptor[reg]:
                        # self.register_descriptor[reg].remove(
                        #     temp_with_farthest_next_use)
                        return (reg, 1, 1)

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
                    if temp_with_farthest_next_use == self.register_descriptor[reg]:
                        # self.register_descriptor[reg].remove(
                        #     temp_with_farthest_next_use)
                        return (reg, 1, 1)
                else:
                    if temp_with_farthest_next_use == self.register_descriptor[reg]:
                        # self.register_descriptor[reg].remove(
                        #     temp_with_farthest_next_use)
                        return (reg, 1, 1)
        return ('$t9', 1, 1)

    def spill_reg(self, register):

        if register in self.reserved_registers:
            self.offset -= 4
            self.text_segment += f"addi $sp, $sp, -4\n"
            self.text_segment += f"sw {register}, 4($sp)\n"

            return

        var = self.register_descriptor[register]
        print('Printing in spill', register, var)
        if var != None:
            if self.address_descriptor[var]['offset'] != None:
                # if the memory space is already allocated
                offset = self.address_descriptor[var]['offset']
                self.text_segment += f"sw {register}, {offset}($s8)\n"
                # self.address_descriptor[var]['registers'].remove(register)
            else:
                # Allocate stack space and push the variable to the stack
                self.offset -= 4
                self.text_segment += f"addi $sp, $sp, -4\n"
                self.text_segment += f"sw {register}, 4($sp)\n"
                # self.address_descriptor.push({
                #     var: {
                #         'offset': self.offset,
                #         'registers': []
                #     }
                # })
        # self.register_descriptor[register] = []

    """ def update_descriptors(self, register, variable):
        self.register_descriptor[register] = [variable]

        try:
            self.address_descriptor[variable] = {
                variable: {
                    'offset': self.address_descriptor[variable]['offset'],
                    'registers': self.address_descriptor[variable]['registers'].append(register)
                }
            }
        except KeyError:
            # self.offset -= 4
            # Create the entry
            self.address_descriptor.push({
                variable: {
                    'offset': "",
                    'registers': [register]
                }
            }) """

    def print_descriptors(self):
        print()
        for var in self.address_descriptor:
            print(var)
            print("offset   :  ", self.address_descriptor[var]['offset'])
            print("registers:  ", self.address_descriptor[var]['registers'])

        # print("address_descriptor",self.address_descriptor)
        print()
        for reg in self.register_descriptor:
            if self.register_descriptor[reg]:
                print(reg, "  :   ", self.register_descriptor[reg])
        # print("register_descriptor",self.register_descriptor)
        print()
        print(
            "----------------------------------------------------------------------------")

    def update_descriptors(self, protocol, params):
        """
        Update the register descriptor and address descriptor
        :param protocol: The various cases of updates required ('spill', 'nospill', 'load')
        :param params: The corresponding requirements for the updates (list)
        :return: nothing
        """
        # TODOD: Think about - do we need to have a  store case as well
        if protocol == 'load':
            # Load a value from memory into the register
            # address_descriptor will always be available for this case

            register = params[0]
            variable = params[1]
            self.register_descriptor[register] = variable

            # Remove the register from the variable descriptor of variables
            # which were using this register before is got overwritten
            for var in self.address_descriptor:
                if register in self.address_descriptor[var]['registers']:
                    self.address_descriptor[var]['registers'].remove(register)

            try:
                self.address_descriptor[variable]['registers'].append(register)

            except KeyError:
                # This exception will never happen
                self.address_descriptor[variable] = {
                    'offset': self.offset,
                    'registers': [register]
                }

        elif protocol == 'spill':

            register = params[0]
            variable = self.register_descriptor[register]

            if self.address_descriptor[variable]['offset'] == None:
                # Memory not allocated for the variable
                self.address_descriptor[variable]['offset'] = self.offset
                # TODO: CHeck -> No need to update registers field of address descriptor
                # self.address_descriptor[variable]['registers'].append(register)
            else:
                # Already memory is allocated
                # Do nothing
                pass

        elif protocol == 'nospill':
            # The register is empty. We will just have to load the variable into the register
            # and then update the register and address descriptors
            # if you already have the value inside the register, then don't update anything

            # TODO !!! : Reconsider this implementation ?
            # The Reg is empty
            # Var is already available in the register

            register = params[0]
            variable = params[1]

            # if self.register_descriptor[register] != None:
            #     # Var is already available in the register
            #     return

            self.register_descriptor[register] = variable

            # TODO : Remove this ???
            # Remove the register from the variable descriptor of variables
            # which were using this register before is got overwritten
            for var in self.address_descriptor:
                if register in self.address_descriptor[var]['registers']:
                    self.address_descriptor[var]['registers'].remove(register)

            try:
                self.address_descriptor[variable]['registers'].append(register)

            except KeyError:
                # If the variable is loaded for the FIRST time into the register
                self.address_descriptor[variable] = {
                    'offset': None,
                    'registers': [register]
                }

        #     self.
        # elif protocol == "new_var":

        print('end of update : ', protocol)
        self.print_descriptors()

    def allocate_registers(self, blocks, live_and_next_use_blocks, data_segment, array_addresses):
        """
        allocate_registers function allocates registers and generates the MIPS code that is stored in the text_segment
        Note: The cases, i.e., the different types of statements are identified as using elifs in this function, 
        but this function is called inside generate_target_code() function
        """
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
                # Start of a function
                elif ':' in line:
                    if line[0] == '_':
                        pass
                    else:
                        #self.offset = 0
                        self.free_all()
                        line += f"\nmove $s8, $sp\n"

                    self.text_segment += line+'\n'

                    print("FUNCTION STARTED ", line+'\n')
# --------------------------------------------------------------------------------------------------
                elif line.startswith('goto'):
                    self.text_segment += f'j {line.split()[1]}\n'
# -------------------------------------------------------------------------------------------------
                elif self.is_assignment_instruction(line):
                    subject, operand = 0, 0
                    # TODO: Check and handle typecasting
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
                    # Typecaseting end -----------------------------------------
                    else:
                        subject, operand = line.split()[0], line.split()[2]
                    # TODO: Change this block and index passing

                    # Temporarily assuming it is a variable or number

                    if operand.isnumeric():
                        print("NUMEBR")
                        # the operand is an integer
                        operand = int(operand)

                        # Get reg from subject ================================================
                        reg0, spill0, update0 = self.get_reg(False,
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            print(521)
                            self.update_descriptors('spill', [reg0])
                            # create the address descriptor entry for subject
                            # loading an immediate into a register -> nospill protocol
                            self.update_descriptors('nospill', [reg0, subject])
                        else:
                            print(524)
                            self.update_descriptors('nospill', [reg0, subject])

                        # ===========================================================================

                        self.text_segment += f"li {reg0}, {operand}\n"

                    elif operand[0] == '\'':
                        # the operand is a character
                        operand = operand[1]

                        # Get reg from subject ================================================
                        reg0, spill0, update0 = self.get_reg(False,
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])
                            # create the address descriptor entry for subject
                            # TODO : what are we doing here?
                            self.update_descriptors('nospill', [reg0, subject])
                        else:
                            print(524)
                            self.update_descriptors('nospill', [reg0, subject])

                        # ===========================================================================

                        self.text_segment += f"li {reg0}, {ord(operand)}\n"

                    elif self.isfloat(operand):
                        # the operand is a float
                        operand = float(operand)

                        print("FLOAT")

                        # Get reg from subject ================================================
                        # TODO : here get_reg is returning "int" register instead of "float"
                        reg0, spill0, update0 = self.get_reg(True,
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])
                            # create the address descriptor entry for subject
                            # TODO : what are we doing here?
                            self.update_descriptors('nospill', [reg0, subject])
                        else:
                            print(524)
                            self.update_descriptors('nospill', [reg0, subject])

                        # ===========================================================================

                        self.text_segment += f"li.s {reg0}, {operand}\n"

                    else:
                        # if it is a variable
                        reg1, spill1, update1 = self.get_reg(False,
                                                             live_and_next_use_blocks, blocks.index(block), operand)
                        if spill1 == 1:
                            self.spill_reg(reg1)
                            print(538)
                            self.update_descriptors('spill', [reg1])
                            offset = self.address_descriptor[operand]['offset']
                            # TODO : Test this!
                            self.text_segment += f"lw {reg1}, {offset}($s8)\n"
                            self.update_descriptors("load", [reg1, operand])
                            # load the variable into the register
                        else:
                            print(543)
                            self.update_descriptors('nospill', [reg1, operand])

                            # check here if the register has nothing
                            # if it has nothing, load the variable into the register

                            # Get reg from subject ================================================

                        reg0, spill0, update0 = self.get_reg(False,
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            print(521)
                            self.update_descriptors('spill', [reg0])

                        # ===========================================================================

                        var = self.register_descriptor[reg1]

                        if var == None:
                            self.text_segment += f"lw {reg0}, {self.address_descriptor[operand]['offset']}($s8)\n"
                            self.update_descriptors("load", [reg0, operand])
                        else:
                            self.text_segment += f"addi {reg0}, {reg1}, 0\n"
                            self.update_descriptors('nospill', [reg0, subject])

                    # if self.isfloat(operand):
                    #     # the operand is a float constant
                    #     freg0, spill0, update0 = self.get_reg(
                    #         True, live_and_next_use_blocks, blocks.index(block), subject)
                    #     if spill0 == 1:
                    #         var = self.register_descriptor[freg0]
                    #         if var != None:
                    #             self.text_segment += f"s.s {freg0}, {var}\n"
                    #             if freg0 in self.address_descriptor[var]:
                    #                 self.address_descriptor[var].remove(freg0)
                    #         self.register_descriptor[freg0] = None
                    #     self.text_segment += f"li.s {freg0}, {operand}\n"

                    #     # self.update_descriptors(freg0, subject)

                    #     self.register_descriptor[freg0] = subject
                    #     self.address_descriptor[subject]['registers'].append(
                    #         freg0)

                    # elif operand.isdigit():
                    #     # the operand is an integer
                    #     operand = int(operand)
                    #     self.text_segment += f"li {reg0}, {operand}\n"
                    #     self.update_descriptors(reg0, subject)
                    # elif "'" in operand:
                    #     # The operand is a character
                    #     self.text_segment += f"li {reg0}, {operand}\n"
                    #     self.address_descriptor[subject]['registers'].append(
                    #         reg0)
                    #     self.register_descriptor[reg0] = subject
                    # elif '"' in operand:
                    #     # The operand is a string
                    #     pass
                    # else:
                    #     # if it is a variable
                    #     reg1, spill1, update1 = self.get_reg(False,
                    #                                          live_and_next_use_blocks, blocks.index(block), operand)
                    #     if spill1 == 1:
                    #         self.spill_reg(reg1)
                    #         self.update_descriptors('spill', [reg1])

                    #         # load the variable into the register
                    #     else:
                    #         self.update_descriptors('nospill', [reg1, operand])

                    #         # check here if the register has nothing
                    #         # if it has nothing, load the variable into the register
                    #         var = self.register_descriptor[reg1]
                    #         if var == None:
                    #             self.text_segment += f"lw {reg0}, {self.address_descriptor[operand]['offset']}($s8)\n"

                    # if spill1 == 1:
                    #     var = self.register_descriptor[reg1]
                    #     if var != None:
                    #         self.text_segment += f"sw {reg1}, {var}\n"
                    #         if reg1 in self.address_descriptor[var]:
                    #             self.address_descriptor[var].remove(reg1)
                    #     self.register_descriptor[reg1] = None
                    #     self.text_segment += f"lw {reg1}, {operand}\n"
                    #     self.address_descriptor[operand].append(reg1)
                    #     self.register_descriptor[reg1] = operand

                    # self.address_descriptor[subject]['registers'].append(
                    #     reg0)
                    # self.register_descriptor[reg0] = subject
                    # self.address_descriptor[operand]['registers'].append(
                    #     reg1)
                    # self.register_descriptor[reg1] = operand

# -------------------------------------------------------------------------------------------------

                elif self.is_return_statement(line):
                    num_words = len(line.split())
                    return_var = line.split()[-1]

                    # reg: [set of variables]
                    # var: [list of reigsters]
                    self.text_segment += f"move $sp, $s8\n"
                    if num_words > 1:
                        # return with value
                        # TODO : get the register from the variable descriptor
                        # for reg in self.register_descriptor
                        reg0, spill0, update0 = self.get_reg(
                            False, live_and_next_use_blocks, blocks.index(block), return_var)

                        if spill0 == 1:
                            # load from memory to $v0
                            offset = self.address_descriptor[return_var]['offset']
                            self.text_segment += f"lw $v0, {offset}($s8)\n"
                            self.update_descriptors('load', [reg0, return_var])
                        else:
                            self.text_segment += f"move $v0, {reg0}\n"
                            self.update_descriptors(
                                'nospill', [reg0, return_var])

                        self.text_segment += f"jr $ra\n"

                        # self.text_segment += f"lw $v0, {line.split()[1]}\n"

                    self.text_segment += f"jr $ra\n"

                elif self.is_function_call_with_return(line):

                    self.text_segment += "\n# -------------------------------- \n"
                    # SPILL all the registers including a0, a1, a2, a3
                    for reg in self.register_descriptor:
                        if self.register_descriptor[reg] != None:
                            # spill
                            self.spill_reg(reg)
                            self.update_descriptors('spill', [reg])
                    # Spill $ra and $fp
                    self.spill_reg("$ra")
                    self.spill_reg("$s8")

                    # ------------------------------------------------------------
                    # Generate the code for function call
                    print(line)
                    words = line.split()
                    number_of_params = int(words[-1])
                    index = number_of_params - 1
                    current_index = lines.index(line)

                    # Code for loading the parameters
                    for i in range(number_of_params):
                        j = current_index - i - 1
                        print(lines[j])

                        param_var = lines[j].split()[1]

                        for reg in self.register_descriptor:
                            if self.register_descriptor[reg] == param_var:
                                self.text_segment += f"move $a{index}, {reg}\n"
                                break
                        else:
                            offset = self.address_descriptor[param_var]['offset']
                            self.text_segment += f"lw $a{index}, {offset}($s8)\n"

                        index -= 1

                    # code for function call
                    function_name = words[3][:-1]
                    self.text_segment += f"jal {function_name}\n"

                    # get_reg for the subject
                    subject = words[0]
                    reg0, spill0, update0 = self.get_reg(
                        False, live_and_next_use_blocks, blocks.index(block), subject)

                    print("subject reg : ", subject, reg0)

                    if spill0 == 1:
                        self.spill_reg(reg0)
                        self.update_descriptors('spill', [reg0])

                    # move the value from $v0 to reg0

                    self.text_segment += f"move {reg0}, $v0\n"
                    self.update_descriptors("nospill", [reg0, subject])

                    # ---------------------------------
                    # Load $fp and $ra
                    # Load $fp from the top of the stack
                    self.text_segment += f"lw $s8, 4($sp)\n"
                    self.text_segment += f"lw $ra, 8($sp)\n"

                    # Load all spilled registers

                    for reg in self.register_descriptor:
                        var = self.register_descriptor[reg]
                        if var != None:
                            offset = self.address_descriptor[var]['offset']
                            if offset != None:
                                self.text_segment += f"lw {reg}, {offset}($s8)\n"
                                self.update_descriptors('load', [reg, var])

                    # ---------------------------------------

                elif self.is_function_call_without_return(line):

                    self.text_segment += "\n# -------------------------------- \n"
                    # SPILL all the registers including a0, a1, a2, a3
                    for reg in self.register_descriptor:
                        if self.register_descriptor[reg] != None:
                            # spill
                            self.spill_reg(reg)
                            self.update_descriptors('spill', [reg])
                    # Spill $ra and $fp
                    self.spill_reg("$ra")
                    self.spill_reg("$s8")

                    # ------------------------------------------------------------
                    # Generate the code for function call
                    print(line)
                    words = line.split()
                    number_of_params = int(words[-1])
                    index = number_of_params - 1
                    current_index = lines.index(line)

                    # Code for loading the parameters
                    for i in range(number_of_params):
                        j = current_index - i - 1
                        print(lines[j])

                        param_var = lines[j].split()[1]

                        for reg in self.register_descriptor:
                            if self.register_descriptor[reg] == param_var:
                                self.text_segment += f"move $a{index}, {reg}\n"
                                break
                        else:
                            offset = self.address_descriptor[param_var]['offset']
                            self.text_segment += f"lw $a{index}, {offset}($s8)\n"

                        index -= 1

                    # code for function call
                    function_name = words[1][:-2]
                    self.text_segment += f"jal {function_name}\n"

                    # ---------------------------------
                    # Load $fp and $ra
                    # Load $fp from the top of the stack
                    self.text_segment += f"lw $s8, 4($sp)\n"
                    self.text_segment += f"lw $ra, 8($sp)\n"

                    # Load all spilled registers

                    for reg in self.register_descriptor:
                        var = self.register_descriptor[reg]
                        if var != None:
                            offset = self.address_descriptor[var]['offset']
                            if offset != None:
                                self.text_segment += f"lw {reg}, {offset}($s8)\n"
                                self.update_descriptors('load', [reg, var])

                    # ---------------------------------------

                elif self.is_input(line):
                    syscall_number = {
                        'int': 5,
                        'float': 6,
                        'char': 12,
                    }
                    _, data_type, variable = line.split()
                    # since it's a reserved register, we don't have to
                    # spill or update the descriptors

                    data_type = data_type[:-1]
                    self.text_segment += f"li $v0, {syscall_number[data_type]}\n"
                    self.text_segment += f"syscall\n"
                    reg0, spill0, update0 = self.get_reg(
                        data_type == 'float', live_and_next_use_blocks, blocks.index(block), variable)
                    if spill0 == 1:
                        self.spill_reg(reg0)
                        self.update_descriptors('spill', [reg0])
                    else:
                        self.update_descriptors(
                            'nospill', [reg0, variable])

                    self.text_segment += f"move {reg0}, $v0\n"

        assembly_code = f".text\n.globl main\n\n{self.text_segment}\n"
        assembly_code = re.sub('start:', 'main:\n', assembly_code)

        return assembly_code
