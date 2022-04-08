class CodeGeneration:

    @staticmethod
    def generate_target_code(intermediate_code):
        goto_labels = set()
        for line in intermediate_code.splitlines():
            if 'goto' in line:
                goto_labels.add(line.split(' ')[-1])

        print(goto_labels)
        blocks = []
        block_line = ""
        prev = False
        first_label_seen = False
        for line in intermediate_code.splitlines():
            if not first_label_seen and line.endswith(':'):
                first_label_seen = True
                blocks.append(block_line)
                block_line += line+'\n'
            elif prev == True:
                blocks.append(block_line)
                block_line = line
                prev = False
            elif ':' in line and line[0] != '#':
                blocks.append(block_line)
                block_line = ""
                block_line += line+'\n'
            elif line.startswith('#L') and line[-1] in goto_labels:
                blocks.append(block_line)
                block_line = ""
                block_line += line+'\n'
            elif 'goto' in line:
                block_line += line+'\n'
                prev = True
            else:
                block_line += line+'\n'

        print(len(blocks))
        for x in blocks:
            print(x)
            print('----------------------------------------------------------------')
