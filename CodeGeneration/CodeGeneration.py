class CodeGeneration:

    @staticmethod
    def generate_target_code(intermediate_code):

        # intermediate_code = "#L1:\ngoto #L3\n#L2:\n#L3:\n#L4:\n#L8:\ngoto #L4\ngoto #L8\nhello"
        goto_labels = set()
        for line in intermediate_code.splitlines():
            if 'goto' in line:
                goto_labels.add(line.split(' ')[-1])

        # print(goto_labels)

        optimized_code1 = ""
        for line in intermediate_code.splitlines():
            if line.startswith('#L') and line.split(':')[0] not in goto_labels:
                pass
            else:
                optimized_code1 += line + '\n'

        optimized_code2 = ""
        redundant_labels = {}
        optimized_code_list = optimized_code1.splitlines()
        i = 0
        while i < len(optimized_code_list):
            line = optimized_code_list[i]
            if line.startswith('#L'):
                optimized_code2 += line + '\n'
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
                optimized_code2 += line + '\n'
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
            line = optimized_code_list[i]
            if line.startswith('goto'):
                optimized_code3 += line+'\n'
                k = i
                for j in range(i+1, len(optimized_code_list)):
                    if optimized_code_list[j].startswith('goto'):
                        k = j
                    else:
                        k += 1
                        break
                i = k
            else:
                optimized_code3 += line+'\n'
                i += 1

        optimized_code4 = ""
        optimized_code_list = optimized_code3.splitlines()
        i = 0
        while i < len(optimized_code_list):
            line = optimized_code_list[i]
            if line.startswith('goto'):
                label = line.split(' ')[-1]
                if optimized_code_list[i+1].startswith('#L') and optimized_code_list[i+1].split(':')[0] == label:
                    i += 1
                else:
                    optimized_code4 += line+'\n'
            else:
                optimized_code4 += line+'\n'
            i += 1

        # print(optimized_code4)
        intermediate_code_final = optimized_code4

        blocks = []
        block_line = ""
        prev = False
        first_label_seen = False
        for line in intermediate_code_final.splitlines():
            if not first_label_seen and line.endswith(':'):
                first_label_seen = True
                blocks.append(block_line)
                block_line += line+'\n'
            elif prev == True:
                blocks.append(block_line)
                block_line = line+'\n'
                prev = False
            elif ':' in line and line[0] != '#':
                blocks.append(block_line)
                block_line = ""
                block_line += line+'\n'
            elif line.startswith('#L') and line.split(':')[0] in goto_labels:
                blocks.append(block_line)
                block_line = ""
                block_line += line+'\n'
            elif 'goto' in line:
                block_line += line+'\n'
                prev = True
            else:
                block_line += line+'\n'
        if block_line != "":
            blocks.append(block_line)

        print(len(blocks))
        for x in blocks:
            print(x)
            print('----------------------------------------------------------------')
