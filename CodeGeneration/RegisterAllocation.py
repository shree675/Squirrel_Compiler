
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
default_float_reg_des = {
    # cannot use $f0, $f2 -> reserved
    # '$f1': None,
    '$f3': None,
    '$f4': None,
    '$f5': None,
    '$f6': None,
    '$f7': None,
    '$f8': None,
    '$f9': None,
    '$f10': None,
    '$f11': None,
    '$f20': None,
    '$f21': None,
    '$f22': None,
    '$f23': None,
    '$f24': None,
    '$f25': None,
    '$f26': None,
    '$f27': None,
    '$f28': None,
    '$f29': None,
    '$f30': None,
    '$f31': None,
}


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

    # registers_map = {
    #     '$t0': 'r0',
    #     '$t1': 'r1',
    #     '$t2': 'r2',
    #     '$t3': 'r3'
    # }

    reserved_registers = {'$ra', '$s8', '$v0', '$f12', '$f1'}

    # 22 registers are available for use
    # floating_point_registers_map = {
    #     '$f1': '$f1',
    #     '$f3': '$f3',
    #     '$f4': '$f4',
    #     '$f5': '$f5',
    #     '$f6': '$f6',
    #     '$f7': '$f7',
    #     '$f8': '$f8',
    #     '$f9': '$f9',
    #     '$f10': '$f10',
    #     '$f11': '$f11',
    #     '$f20': '$f20',
    #     '$f21': '$f21',
    #     '$f22': '$f22',
    #     '$f23': '$f23',
    #     '$f24': '$f24',
    #     '$f25': '$f25',
    #     '$f26': '$f26',
    #     '$f27': '$f27',
    #     '$f28': '$f28',
    #     '$f29': '$f29',
    #     '$f30': '$f30',
    #     '$f31': '$f31',
    # }

    # datatype_sizes = {
    #     'int': 4,
    #     'float': 4,
    #     'char': 1,
    #     'bool': 1,
    # }

    # The set of all valid arithmetic operators
    arithmetic_operators = set("+ - * / % && || > < >= <= ! != = ==".split())

    def __init__(self):
        # TODO: change the structure of register_descriptor
        # We should add float registers as well
        self.register_descriptor = default_reg_des.copy()
        self.float_register_descriptor = default_float_reg_des.copy()
        # self.address_descriptor = {}
        self.address_descriptor = {
            "~": {
                "offset": None,
                "registers": ["$f1"]
            }
        }
        self.offset = 4
        self.text_segment = ''
        self.num_input_strings = 0

    def isfloat(self, num):
        if num.isdigit():
            return False
        try:
            float(num)
            return True
        except ValueError:
            return False

    def get_data_type(self, variable, symbol_table):

        if self.is_constant(variable):
            if "'" in variable:
                return 'char'
            elif self.isfloat(variable):
                return 'float'
            elif '"' in variable:
                return 'string'
            else:
                return 'int'
        # In case of temporary variable, we directly use the naming convention to infer type
        # In case of user defined variable, we use the symbol table passed form the parser to infer the datatype
        print('VARIABLE in get_DT: ' + variable)
        variable_type = None
        if variable.startswith("__"):
            # temp variable
            print("TEMP VARIABLE")
            if 'f' in variable:
                variable_type = "float"
            else:
                variable_type = "int"
        else:
            # user variable
            variable_name = variable.split('__')[0]
            print("foooo", variable_name)
            variable_scope = variable.split('__')[1]
            variable_type = list(filter(
                lambda var: var["identifier_name"] == variable_name +
                "`"+variable_scope,
                symbol_table
            ))[0]["type"]
        return variable_type

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
        # print("instruction : " , instruction)
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

    def is_assignment_instruction_with_typecast(self, instruction):
        # The case of a simple assignment statement with typecast like a=(int)b or f=(float)10
        flag = False
        if '(' in instruction:
            flag = True
        # In case the type casting is mentioned, replace it with '' using the following regex
        instruction = re.sub(r'\(.+\)', '', instruction)
        if '=' in instruction and len(instruction.split()) == 3 and flag:
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

    def is_input(self, instruction):
        if instruction and instruction.split()[0] == 'input':
            return True
        return False

    def is_input_string(self, instruction, data_segment):
        return instruction.startswith('input_string')

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

    def is_constant(self, value):
        # check character
        if value[0] == '\'':
            return True
        # check int
        if value.isdigit():
            return True
        # check float
        if self.isfloat(value):
            return True
        # check string
        if value[0] == '\"' and value[-1] == '\"':
            return True

        # not a constant
        return False

    def free_all(self):
        # Reinitialize the register_descriptor and address_descriptor
        # We should add float registers as well
        self.register_descriptor = default_reg_des.copy()
        self.float_register_descriptor = default_float_reg_des.copy()
        # self.address_descriptor = {}
        self.address_descriptor = {
            "~": {
                "offset": None,
                "registers": ["$f1"]
            }
        }
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
        # Depending on whether an integer or float register is required, we choose the register descriptor map accordingly
        register_descriptor = None
        if is_float:
            register_descriptor = self.float_register_descriptor
        else:
            register_descriptor = self.register_descriptor

        print('variable', variable, is_float)
        # if the variable is already contained in some register
        # No need to spill. Just return that register
        if is_float:
            for reg in register_descriptor:
                if 'f' in reg and self.address_descriptor.get(variable) != None and reg in self.address_descriptor[variable]['registers']:
                    return (reg, 0, 0)
        else:
            for reg in register_descriptor:
                if variable in self.address_descriptor and reg in self.address_descriptor[variable]['registers']:
                    return (reg, 0, 0)

        # if there is an empty register available
        # No need to spill, just return that register

        if is_float:
            for reg in default_float_reg_des:
                if reg in register_descriptor and register_descriptor[reg] == None:
                    return (reg, 0, 1)
        else:
            for reg in default_reg_des:
                if reg in register_descriptor and register_descriptor[reg] == None:
                    return (reg, 0, 1)

        """ The Remaining cases are the ones that involves SPILL"""
        # otherwise choose the register occupied by a temporary variable with no next use
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if (var[0] == '~' or var[0] == '_') and record[var]['next_use'] == -1:
                    # -1 indicates no next use
                    temp_var = var
                    for reg in register_descriptor:
                        if is_float and 'f' in reg:
                            if temp_var == register_descriptor[reg]:
                                # register_descriptor[reg].remove(temp_var)
                                return (reg, 1, 1)
                        else:
                            if temp_var == register_descriptor[reg]:
                                # register_descriptor[reg].remove(temp_var)
                                return (reg, 1, 1)
                    # return (reg,1,1) # Not sure if I need to return temp_ var

        # else choose the register occupied by a non-temporary variable with no next use
        # spill the register
        for record in live_and_next_use_blocks[index]:
            for var in record:
                if record[var]['next_use'] == -1:
                    temp_var = var
                    # TODO: Check the naming convention - inconsistent for variable in register_descriptor
                    for reg in register_descriptor:
                        if is_float and 'f' in reg:
                            if reg in register_descriptor and temp_var == register_descriptor[reg]:
                                # register_descriptor[reg].remove(temp_var)
                                # self.address_descriptor[temp_var]['registers'].append(reg)
                                return (reg, 1, 1)
                        else:
                            if reg in register_descriptor and temp_var == register_descriptor[reg]:
                                # register_descriptor[reg].remove(temp_var)
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
            for reg in register_descriptor:
                if is_float and 'f' in reg:
                    if temp_with_farthest_next_use == register_descriptor[reg]:
                        # register_descriptor[reg].remove(
                        #     temp_with_farthest_next_use)
                        return (reg, 1, 1)
                else:
                    if temp_with_farthest_next_use == register_descriptor[reg]:
                        # register_descriptor[reg].remove(
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
            for reg in register_descriptor:
                if is_float and 'f' in reg:
                    if temp_with_farthest_next_use == register_descriptor[reg]:
                        # register_descriptor[reg].remove(
                        #     temp_with_farthest_next_use)
                        return (reg, 1, 1)
                else:
                    if temp_with_farthest_next_use == register_descriptor[reg]:
                        # register_descriptor[reg].remove(
                        #     temp_with_farthest_next_use)
                        return (reg, 1, 1)
        return ('$t9', 1, 1) if not is_float else ('$f31', 1, 1)

    def spill_reg(self,  register):

        if register in self.reserved_registers:
            self.offset -= 4
            self.text_segment += f"addi $sp, $sp, -4\n"
            self.text_segment += f"sw {register}, 4($sp)\n"

            return

        register_descriptor = None
        if 'f' in register:
            register_descriptor = self.float_register_descriptor
        else:
            register_descriptor = self.register_descriptor

        var = register_descriptor[register]
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
        # register_descriptor[register] = []

    def print_descriptors(self):
        # UNCOMMENT
        # print()
        # for var in self.address_descriptor:
        #     print(var)
        #     print("offset   :  ", self.address_descriptor[var]['offset'])
        #     print("registers:  ", self.address_descriptor[var]['registers'])

        # # print("address_descriptor",self.address_descriptor)
        # print()
        # for reg in self.register_descriptor:
        #     if self.register_descriptor[reg]:
        #         print(reg, "  :   ", self.register_descriptor[reg])
        # # print("register_descriptor",self.register_descriptor)
        # print()
        # print(
        #     "----------------------------------------------------------------------------")
        pass

    def update_descriptors(self, protocol, params):

        # Assumption - paramns[0] exists and is a register
        """
        Update the register descriptor and address descriptor
        :param protocol: The various cases of updates required ('spill', 'nospill', 'load')
        :param params: The corresponding requirements for the updates (list)
        :return: nothing
        """

        # Depending on whether an integer or float register is required, we choose the register descriptor map accordingly
        register_descriptor = None
        register = params[0]
        if 'f' in register:
            register_descriptor = self.float_register_descriptor
        else:
            register_descriptor = self.register_descriptor

        # TODO: Think about - do we need to have a  store case as well
        if protocol == 'load':
            # Load a value from memory into the register
            # address_descriptor will always be available for this case

            register = params[0]
            variable = params[1]
            register_descriptor[register] = variable

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
            variable = register_descriptor[register]

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

            # The Reg is empty
            # Var is already available in the register

            register = params[0]
            variable = params[1]

            # if register_descriptor[register] != None:
            #     # Var is already available in the register
            #     return

            register_descriptor[register] = variable

            # TODO : Remove this ???
            # Remove the register from the variable descriptor of variables
            # which were using this register before it got overwritten
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

    def allocate_registers(self, blocks, live_and_next_use_blocks, data_segment, array_addresses, symbol_table, data_segment_dict):
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

                print("Line: ", line)

                if self.is_array_initialization(line):
                    # Extract the datatype of the initialized array: int arr`2[24]
                    data_type, size = line.split()[0], line.split()[
                        1].split('[')[1].split(']')[0]
                    num_of_elements = int(
                        size)//4  # this was previously datatype_sizes[data_type] but in our case everything is size 4
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
                        # self.offset = 0
                        self.free_all()
                        line += f"\nmove $s8, $sp\n"

                    self.text_segment += line+'\n'

                    print("FUNCTION STARTED ", line+'\n')
# --------------------------------------------------------------------------------------------------
                elif line.startswith('goto'):
                    self.text_segment += f'j {line.split()[1]}\n'

                elif self.is_array_assignment(line):
                    array_name = line.split()[0].split('[')[0]
                    # var_index will never be a constant in the TAC
                    var_index = line.split()[0].split('[')[1][:-1]
                    data_type = self.get_data_type(array_name, symbol_table)

                    data_type_of_rhs = self.get_data_type(
                        line.split()[-1], symbol_table)

                    reg0, spill0, _ = self.get_reg(False,
                                                   live_and_next_use_blocks, blocks.index(block), var_index)
                    reg1, spill1, _ = self.get_reg(data_type_of_rhs == 'float',
                                                   live_and_next_use_blocks, blocks.index(block), line.split()[-1])

                    if spill0 == 1:
                        self.spill_reg(reg0)
                        self.update_descriptors('spill', [reg0])

                        offset = self.address_descriptor[var_index]['offset']
                        self.text_segment += f"lw {reg0}, {offset}($s8)\n"
                        self.update_descriptors('load', [reg0, var_index])

                    if spill1 == 1:
                        self.spill_reg(reg1)
                        self.update_descriptors('spill', [reg1])

                        if self.is_constant(line.split()[-1]):
                            if not self.isfloat(line.split()[-1]):
                                self.text_segment += f"li {reg1}, {line.split()[-1]}\n"
                            else:
                                self.text_segment += f"li.s {reg1}, {line.split()[-1]}\n"
                        else:
                            offset = self.address_descriptor[line.split(
                            )[-1]]['offset']
                            if data_type_of_rhs == 'float':
                                self.text_segment += f"l.s {reg1}, {offset}($s8)\n"
                            else:
                                self.text_segment += f"lw {reg1}, {offset}($s8)\n"
                        self.update_descriptors(
                            'load', [reg1, line.split()[-1]])

                    if data_type == 'float':
                        self.text_segment += f"s.s {reg1}, {array_name}({reg0})\n"
                    else:
                        self.text_segment += f"sw {reg1}, {array_name}({reg0})\n"
# -------------------------------------------------------------------------------------------------
                elif self.is_assignment_instruction_with_typecast(line):
                    subject, operand, cast_type, subject_type, operand_type = [
                        None]*5
                    subject, operand, cast_type = line.split()[0], line.split()[
                        3], line.split()[2]

                    # Extracting subject_type
                    if '[' in subject:
                        subject = subject.split('[')[0]
                    subject_type = self.get_data_type(subject, symbol_table)

                    # ---------------------------------------------------------------------------------------
                    # The operand could be a literal or a variable
                    # Literal -> int, char, float, bool, string
                    # Variable -> temporary or user defined (should not make a difference to code generation)

                    if cast_type == 'int' or cast_type == 'char' or cast_type == 'bool':
                        # if operand is char and cast type is int, do nohting because mips will take care of it
                        # here, we just need to check if the operand is a float or not
                        # if the operand is not float, do nothing

                        pass

                    elif cast_type == 'float':
                        pass
                    pass
                    # ---------------------------------------------------------------------------------------
                    """There are 4 cases possible where the subject and operand can be of different types
                    int type: int, char, bool (no need to explicitly mention it)
                    float type: float

                    Case 1: Subject: int type, Operand: int type
                            move $t0, $t1
                    Case 2: Subject: float type, Operand: float type
                            move $f0, $f1
                    Case 3: Subject: int type, Operand: float type
                            cvt.w.s $f0, $f1
                    Case 4: Subject: float type, Operand: int type
                            cvt.s.w $f0, $f1
                    """
                    # ---------------------------------------------------------------------------------------
                    if operand.isnumeric() or operand[0] == '\'':
                        # Since operand is int type -> Only Case 1 and Case 4 are possible
                        # the operand is an integer or char (bool need not be handled because it would
                        # already have been converted to integer just before code generation)
                        operand_type = None
                        if operand.isnumeric():
                            operand_type = 'int'
                            # operand = int(operand)
                        else:
                            operand_type = 'char'
                            operand = operand[1]
                            operand = ord(operand)
                        # Get reg for subject ================================================
                        # reg0, spill0, update0 = self.get_reg(subject_type == 'float', live_and_next_use_blocks, blocks.index(block), subject)
                        reg0, spill0, update0 = self.get_reg(cast_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        # print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])
                            # create the address descriptor entry for subject

                        if cast_type == 'float':
                            # Case 4: Subject: float type, Operand: int type
                            self.text_segment += f"li.s {reg0}, {operand}\n"
                        else:
                            # Case 1: Subject: int type, Operand: int type
                            self.text_segment += f"li {reg0}, {operand}\n"

                        # loading an immediate into a register -> nospill protocol
                        self.update_descriptors(
                            'nospill', [reg0, subject])
                    # ---------------------------------------------------------------------------------------
                    elif self.isfloat(operand):
                        # the operand is a float - although isfloat also returns true for int
                        # we have already caught int in a previous elif so this will still be correct
                        # Since operand is float type -> Only Case 2 and Case 3 are possible
                        operand = float(operand)

                        # Get reg for subject ================================================
                        # TODO : here get_reg is returning "int" register instead of "float"
                        # TODO : Check the above comment, it should be fine now
                        # reg0, spill0, update0 = self.get_reg(subject_type == 'float',
                        #                                      live_and_next_use_blocks, blocks.index(block), subject)
                        reg0, spill0, update0 = self.get_reg(cast_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        # print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])
                        # ===========================================================================

                        if cast_type == 'float':
                            # Case 2: Subject: float type, Operand: float type
                            self.text_segment += f"li.s {reg0}, {operand}"
                        else:
                            # Case 3: Subject: int type, Operand: float type
                            self.text_segment += f"li {reg0}, {operand}\n"
                            self.text_segment += f"cvt.w.s {reg0}, {reg0}\n"

                        # loading an immediate into a register -> nospill protocol
                        self.update_descriptors(
                            'nospill', [reg0, subject])

                    else:
                        # if it is a variable
                        operand_type = self.get_data_type(
                            operand, symbol_table)

                        register_descriptor = None
                        if operand_type == 'float':
                            register_descriptor = self.float_register_descriptor
                        else:
                            register_descriptor = self.register_descriptor

                        # First get the register for the operand

                        reg1, spill1, update1 = self.get_reg(operand_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), operand)

                        # get register for subject
                        reg0, spill0, update0 = self.get_reg(subject_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])

                        if spill1 == 1:
                            self.spill_reg(reg1)
                            self.update_descriptors('spill', [reg1])

                            offset = self.address_descriptor[operand]['offset']

                            if operand_type == "float":
                                self.text_segment += f"l.s {reg0}, {offset}($s8)\n"
                            else:
                                self.text_segment += f"lw {reg0}, {offset}($s8)\n"
                            self.update_descriptors(
                                "load", [reg0, operand])

                        else:
                            # if the register in not empty (it already has the value)
                            # then use the register
                            # else load the value into reg0 directly from the
                            # memory (handled below)

                            if register_descriptor[reg1] == None:
                                # if the reg1 is empty
                                # load the value into reg0 directly from the memory
                                offset = self.address_descriptor[operand]['offset']
                                if operand_type == "float":
                                    self.text_segment += f"l.s {reg0}, {offset}($s8)\n"
                                else:
                                    self.text_segment += f"lw {reg0}, {offset}($s8)\n"
                                self.update_descriptors(
                                    "load", [reg0, operand])
                            else:
                                # reg1 already has the value of operand
                                if reg0 in default_float_reg_des and reg1 in default_reg_des:
                                    self.text_segment += f"mtc1 {reg1}, $f1\n"
                                    self.text_segment += f"cvt.s.w {reg0}, $f1\n"

                                elif reg0 in default_reg_des and reg1 in default_float_reg_des:
                                    self.text_segment += f"cvt.w.s $f1, {reg1}\n"
                                    self.text_segment += f"mfc1 {reg0}, $f1\n"
                                elif reg0 in default_float_reg_des and reg1 in default_float_reg_des:
                                    self.text_segment += f"mov.s {reg0}, {reg1}\n"
                                else:
                                    self.text_segment += f"addi {reg0}, {reg1}, 0\n"

                                self.update_descriptors(
                                    'nospill', [reg0, subject])


# -------------------------------------------------------------------------------------------------
                elif self.is_assignment_instruction(line):
                    # TODO !!!!: Anything related to arrays are not handled in this case
                    subject, operand, subject_type, operand_type = [
                        None]*4

                    subject, operand = line.split()[0], line.split()[2]
                    # Extracting subject_type
                    if '[' in subject:
                        subject = subject.split('[')[0]

                    subject_type = self.get_data_type(subject, symbol_table)

                    print("Subject TYPE assignment : ", subject,  subject_type)

                    # ---------------------------------------------------------------------------------------
                    # The operand could be a literal or a variable
                    # Literal -> int, char, float, bool, string
                    # Variable -> temporary or user defined (should not make a difference to code generation)

                    if operand.isnumeric() or operand[0] == '\'':
                        # the operand is an integer or char (bool need not be handled because it would
                        # already have been converted to integer just before code generation)
                        operand_type = None
                        if operand.isnumeric():
                            operand_type = 'int'
                            # operand = int(operand)
                        else:
                            operand_type = 'char'
                            operand = operand[1]
                            operand = ord(operand)
                            # In case of character we convert it to ascii value
                        # Get reg for subject ================================================
                        reg0, spill0, update0 = self.get_reg(subject_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), subject)
                        # print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])
                            # create the address descriptor entry for subject

                        self.text_segment += f"li {reg0}, {operand}\n"

                        # loading an immediate into a register -> nospill protocol
                        self.update_descriptors(
                            'nospill', [reg0, subject])

                    # ------------------------------------------------------------
                    elif self.isfloat(operand):
                        # the operand is a float - although isfloat also returns true for int
                        # we have already caught int in a previous elif so this will still be correct
                        operand = float(operand)

                        # Get reg for subject ================================================
                        # TODO : here get_reg is returning "int" register instead of "float"
                        # TODO : Check the above comment, it should be fine now
                        reg0, spill0, update0 = self.get_reg(subject_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        # print("subject reg : ", subject, reg0)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])
                        # ===========================================================================

                        self.text_segment += f"li.s {reg0}, {operand}\n"
                        # loading an immediate into a register -> nospill protocol
                        self.update_descriptors(
                            'nospill', [reg0, subject])

                    elif operand[0] == '\"':
                        print("STRING OPERAND", operand)
                        reg0, spill0, _ = self.get_reg(
                            subject_type == 'float', live_and_next_use_blocks, blocks.index(block), subject)

                        if spill0:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])

                        self.text_segment += f"la {reg0}, {subject}\n"
                        # TODO : Update descriptors for load from data segment
                        self.update_descriptors("load", [reg0, subject])
                        print("STRING", self.register_descriptor)

                    else:
                        # if it is a variable
                        if '[' in operand:
                            operand = operand.split('[')[0]

                        operand_type = self.get_data_type(
                            operand, symbol_table)

                        register_descriptor = None
                        if operand_type == 'float':
                            register_descriptor = self.float_register_descriptor
                        else:
                            register_descriptor = self.register_descriptor

                        # First get the register for the operand

                        reg1, spill1, update1 = self.get_reg(operand_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), operand)

                        # get register for subject
                        reg0, spill0, update0 = self.get_reg(subject_type == 'float',
                                                             live_and_next_use_blocks, blocks.index(block), subject)

                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])

                        if spill1 == 1:
                            self.spill_reg(reg1)
                            self.update_descriptors('spill', [reg1])

                            offset = self.address_descriptor[operand]['offset']

                            if operand_type == "float":
                                self.text_segment += f"l.s {reg0}, {offset}($s8)\n"
                            else:
                                self.text_segment += f"lw {reg0}, {offset}($s8)\n"
                            self.update_descriptors(
                                "load", [reg0, operand])

                        else:
                            # if the register in not empty (it already has the value)
                            # then use the register
                            # else load the value into reg0 directly from the
                            # memory (handled below)
                            if register_descriptor[reg1] == None:
                                # if the reg1 is empty
                                # load the value into reg0 directly from the memory
                                offset = self.address_descriptor[operand]['offset']
                                if operand_type == "float":
                                    self.text_segment += f"l.s {reg0}, {offset}($s8)\n"
                                else:
                                    self.text_segment += f"lw {reg0}, {offset}($s8)\n"
                                self.update_descriptors(
                                    "load", [reg0, operand])
                            else:
                                # reg1 already has the value of operand
                                if reg0 in default_float_reg_des and reg1 in default_float_reg_des:
                                    self.text_segment += f"mov.s {reg0}, {reg1}\n"
                                else:
                                    self.text_segment += f"addi {reg0}, {reg1}, 0\n"

                                self.update_descriptors(
                                    'nospill', [reg0, subject])

# -------------------------------------------------------------------------------------------------
                elif self.is_arithmetic_instruction_binary(line):
                    # Same as reg = [0,1,2] -> We just need to initialize the list with 3 elements
                    reg = [None] * 3
                    spill = [None] * 3  # Same as spill = [0,1,2]

                    subject, operand1, operand2 = line.split()[0], line.split()[
                        2], line.split()[4]
                    operator = line.split()[3]

                    subject_type = self.get_data_type(subject, symbol_table)

                    reg[0], spill[0], _ = self.get_reg(subject_type == 'float',
                                                       live_and_next_use_blocks, blocks.index(block), subject)
                    if spill[0] == 1:
                        self.spill_reg(reg[0])
                        self.update_descriptors('spill', [reg[0]])

                    operand1_type = self.get_data_type(operand1, symbol_table)

                    if reg[1] is None:
                        reg[1], spill[1], _ = self.get_reg(operand1_type == 'float',
                                                           live_and_next_use_blocks, blocks.index(block), operand1)
                        if spill[1] == 1:
                            self.spill_reg(reg[1])
                            self.update_descriptors('spill', [reg[1]])
                            if self.is_constant(operand1):
                                if not self.isfloat(operand1):
                                    self.text_segment += f"li {reg[1]}, {operand1}\n"
                                else:
                                    self.text_segment += f"li.s {reg[1]}, {operand1}\n"
                            else:
                                offset = self.address_descriptor[operand1]['offset']
                                self.text_segment += f"lw {reg[1]}, {offset}($s8)\n"
                        self.update_descriptors("load", [reg[1], operand1])

                    operand2_type = self.get_data_type(operand2, symbol_table)

                    if reg[2] is None:
                        reg[2], spill[2], _ = self.get_reg(operand2_type == 'float',
                                                           live_and_next_use_blocks, blocks.index(block), operand2)
                        if spill[2] == 1:
                            self.spill_reg(reg[2])
                            self.update_descriptors('spill', [reg[2]])
                            if self.is_constant(operand2):
                                if not self.isfloat(operand2):
                                    self.text_segment += f"li {reg[2]}, {operand2}\n"
                                else:
                                    self.text_segment += f"li.s {reg[2]}, {operand2}\n"
                            else:
                                offset = self.address_descriptor[operand2]['offset']
                                self.text_segment += f"lw {reg[2]}, {offset}($s8)\n"
                        self.update_descriptors("load", [reg[2], operand2])

                    operand_type = self.get_data_type(
                        operand1, symbol_table)

                    if operand_type == 'float':
                        if operator == '+':
                            self.text_segment += f"add.s {reg[0]}, {reg[1]}, {reg[2]}\n"
                        elif operator == '-':
                            self.text_segment += f"sub.s {reg[0]}, {reg[1]}, {reg[2]}\n"
                        elif operator == '*':
                            self.text_segment += f"mul.s {reg[0]}, {reg[1]}, {reg[2]}\n"
                        elif operator == '/':
                            self.text_segment += f"div.s {reg[0]}, {reg[1]}, {reg[2]}\n"

                        continue

                    if operator == '+':
                        self.text_segment += f"add {reg[0]}, {reg[1]}, {reg[2]}\n"
                    elif operator == '-':
                        self.text_segment += f"sub {reg[0]}, {reg[1]}, {reg[2]}\n"
                    elif operator == '*':
                        self.text_segment += f"mult {reg[1]}, {reg[2]}\n"
                        self.text_segment += f"mflo {reg[0]}\n"
                    elif operator == '/':
                        self.text_segment += f"div {reg[1]}, {reg[2]}\n"
                        self.text_segment += f"mflo {reg[0]}\n"
                    elif operator == '%':
                        self.text_segment += f"div {reg[1]}, {reg[2]}\n"
                        self.text_segment += f"mfhi {reg[0]}\n"

                    self.update_descriptors("nospill", [reg[0], subject])
# -------------------------------------------------------------------------------------------------
                elif self.is_if_statement(line):
                    # the operands are never constants
                    if_stmt, left, operator, right, label = line.split()[0], line.split(
                    )[1], line.split()[2], line.split()[3], line.split()[-1]

                    reg = [i for i in range(3)]
                    spill = [0, 0, 0]

                    reg[0], spill[0], _ = self.get_reg(False,
                                                       live_and_next_use_blocks, blocks.index(block), left)
                    reg[1], spill[1], _ = self.get_reg(False,
                                                       live_and_next_use_blocks, blocks.index(block), right)
                    reg[2], spill[2], _ = self.get_reg(False,
                                                       live_and_next_use_blocks, blocks.index(block), "~")

                    if spill[0] == 1:
                        self.spill_reg(reg[0])
                        self.update_descriptors('spill', [reg[0]])

                        offset = self.address_descriptor[left]['offset']
                        self.text_segment += f"lw {reg[0]}, {offset}($s8)\n"
                        self.update_descriptors("load", [reg[0], left])

                    if spill[1] == 1:
                        self.spill_reg(reg[1])
                        self.update_descriptors('spill', [reg[1]])

                        offset = self.address_descriptor[right]['offset']
                        self.text_segment += f"lw {reg[1]}, {offset}($s8)\n"
                        self.update_descriptors("load", [reg[1], right])

                    if spill[2] == 1:
                        self.spill_reg(reg[2])
                        self.update_descriptors('spill', [reg[2]])

                    operand_type = self.get_data_type(left, symbol_table)

                    # TODO !!!: Check nop for floats while testing

                    if operand_type == "float":
                        if if_stmt == 'if':
                            if operator == '<=':
                                self.text_segment += f"c.le.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1t {label}\n"
                            elif operator == '>=':
                                self.text_segment += f"c.lt.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1f {label}\n"
                            elif operator == '<':
                                self.text_segment += f"c.lt.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1t {label}\n"
                            elif operator == '>':
                                self.text_segment += f"c.le.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1f {label}\n"
                            elif operator == '==':
                                self.text_segment += f"c.eq.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1t {label}\n"
                            elif operator == '!=':
                                self.text_segment += f"c.eq.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1f {label}\n"

                        else:

                            # ifFalse
                            if operator == '>':
                                self.text_segment += f"c.le.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1t {label}\n"
                            elif operator == '<':
                                self.text_segment += f"c.lt.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1f {label}\n"
                            elif operator == '>=':
                                self.text_segment += f"c.lt.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1t {label}\n"
                            elif operator == '<=':
                                self.text_segment += f"c.le.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1f {label}\n"
                            elif operator == '!=':
                                self.text_segment += f"c.eq.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1t {label}\n"
                            elif operator == '==':
                                self.text_segment += f"c.eq.s {reg[0]}, {reg[1]}\n"
                                self.text_segment += f"bc1f {label}\n"
                        continue

                    if if_stmt == 'if':
                        if operator == '<=':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '>=':
                            self.text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            self.text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '<':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '>':
                            self.text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            self.text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '==':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"beq {reg[2]}, $zero, {label}\n"
                        elif operator == '!=':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"bne {reg[2]}, $zero, {label}\n"

                    else:
                        # ifFalse
                        if operator == '>':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '<':
                            self.text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            self.text_segment += f"ble {reg[2]}, $zero, {label}\n"
                        elif operator == '>=':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '<=':
                            self.text_segment += f"sub {reg[2]}, {reg[1]}, {reg[0]}\n"
                            self.text_segment += f"blt {reg[2]}, $zero, {label}\n"
                        elif operator == '!=':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"beq {reg[2]}, $zero, {label}\n"
                        elif operator == '==':
                            self.text_segment += f"sub {reg[2]}, {reg[0]}, {reg[1]}\n"
                            self.text_segment += f"bne {reg[2]}, $zero, {label}\n"
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
                        # for reg in register_descriptor
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
# -------------------------------------------------------------------------------------------------

                elif self.is_function_call_with_return(line):

                    self.text_segment += "\n# -------------------------------- \n"
                    # SPILL all the registers including a0, a1, a2, a3
                    # TODO : spill all the float registers also!
                    for reg in self.register_descriptor:
                        if self.register_descriptor[reg] != None:
                            # spill
                            self.spill_reg(reg)
                            self.update_descriptors('spill', [reg])
                    # Spill $ra and $fp
                    self.spill_reg(False, "$ra")
                    self.spill_reg(False, "$s8")

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

                elif self.is_input_string(line, data_segment):
                    syscall_number = 8
                    _, variable, length = line.split()
                    variable = variable[:-1]
                    data_segment_dict[variable] = (
                        ".space", int(length) + 1, "")

                    self.text_segment += f"li $v0, {syscall_number}\n"
                    self.text_segment += f"la $a0, {variable}\n"
                    self.text_segment += f"syscall\n"

                    self.num_input_strings += 1

                elif self.is_output(line):
                    # TODO: Test Float, String
                    syscall_number = {
                        'int': 1,
                        'float': 2,
                        'string': 4,
                        'char': 11,
                    }
                    _, data_type, variable = line.split()
                    data_type = data_type[:-1]
                    if data_type == 'string':
                        self.text_segment += f"li $v0, {syscall_number[data_type]}\n"
                        self.text_segment += f"la $a0, {variable}\n"
                        self.text_segment += f"syscall\n"

                        continue

                    else:
                        # For regular variables
                        print("OUTPUT Variable", variable)
                        print(self.address_descriptor)
                        print(self.register_descriptor)

                        reg0, spill0, _ = self.get_reg(
                            data_type == 'float', live_and_next_use_blocks, blocks.index(block), variable)
                        if spill0 == 1:
                            self.spill_reg(reg0)
                            self.update_descriptors('spill', [reg0])
                            if self.is_constant(variable):
                                if not self.isfloat(variable):
                                    self.text_segment += f"li {reg0}, {variable}\n"
                                else:
                                    self.text_segment += f"li.s {reg0}, {variable}\n"
                            else:
                                offset = self.address_descriptor[variable]['offset']
                                if data_type == 'float':
                                    self.text_segment += f"l.s {reg0}, {offset}($s8)\n"
                                else:
                                    self.text_segment += f"lw {reg0}, {offset}($s8)\n"
                            self.update_descriptors(
                                'load', [reg0, variable])
                        self.text_segment += f"li $v0, {syscall_number[data_type]}\n"
                        if data_type == 'float':
                            self.text_segment += f"mov.s $f12, {reg0}\n"
                        else:
                            self.text_segment += f"move $a0, {reg0}\n"
                        self.text_segment += f"syscall\n"

        for var, (type, space, value) in data_segment_dict.items():
            if space:
                data_segment += f"{var}:\n\t{type} {space}\n"
            else:
                data_segment += f"{var}:\n\t{type} {value}\n"

        assembly_code = f"{data_segment}.text\n.globl main\n\n{self.text_segment}\n"
        assembly_code = re.sub('start:', 'main:\n', assembly_code)

        return assembly_code
