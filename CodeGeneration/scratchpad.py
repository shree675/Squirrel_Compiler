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
                                if reg[1] in self.address_descriptor[var]['registers']:
                                    self.address_descriptor[var]['registers'].remove(
                                        reg[1])
                            self.register_descriptor[reg[1]] = []
                            text_segment += f"lw {reg[1]}, {var_index}\n"
                            self.address_descriptor[var_index]['registers'].append(
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
                    self.address_descriptor[subject]['registers'].append(
                        reg[0])
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
                        self.address_descriptor[var_index]['registers'].append(reg0)
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
                        self.address_descriptor[subject]['registers'].append(freg0)
                    elif operand.isdigit():
                        # the operand is an integer
                        operand = int(operand)
                        text_segment += f"li {reg0}, {operand}\n"
                        self.address_descriptor[subject]['registers'].append(reg0)
                        self.register_descriptor[reg0].append(subject)
                    elif "'" in operand:
                        # The operand is a character
                        text_segment += f"li {reg0}, {operand}\n"
                        self.address_descriptor[subject]['registers'].append(reg0)
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

                        self.address_descriptor[subject]['registers'].append(reg0)
                        self.register_descriptor[reg0].append(subject)
                        self.address_descriptor[operand]['registers'].append(reg1)
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
                        self.address_descriptor[subject]['registers'].append(reg0)
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

                    self.address_descriptor[left]['registers'].append(reg[0])
                    self.register_descriptor[reg[0]].append(left)

                    self.address_descriptor[right]['registers'].append(reg[1])
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