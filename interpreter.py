def interpret(code):
    memory = [0] * 30000
    pointer = 0

    commands = {
        'OoOo': 'increment',
        'OOo': 'decrement',
        '0O': 'output',
        '0o0': 'next_cell',
        'OooO': 'prev_cell',
        'Oo': 'start_loop',
        'oooO': 'end_loop',
    }

    #remove spaces and line breaks
    code = code.strip().replace(" ", "").replace("\n", "")

    #tokenize commands
    tokens = []
    i = 0
    while i < len(code):
        for command, name in commands.items():
            if code[i:i + len(command)] == command:
                tokens.append(name)
                i += len(command) - 1
                break
        i += 1

    print("Tokens:", tokens) #tokens if correct

    def validate_syntax(tokens):
        depth = 0
        for token in tokens:
            if token == 'start_loop':
                depth += 1
            elif token == 'end_loop':
                depth -= 1
                if depth < 0:
                    raise SyntaxError("Loop end has no matching start")
        if depth > 0:
            raise SyntaxError("Loop start has no matching end")

    validate_syntax(tokens)

    pc = 0
    loop_stack = []
    output = []

    while pc < len(tokens):
        command = tokens[pc]

        if command == 'increment':
            memory[pointer] = (memory[pointer] + 1) % 256
        elif command == 'decrement':
            memory[pointer] = (memory[pointer] - 1) % 256
        elif command == 'output':
            ascii_value = memory[pointer]   #store ascii value
            output.append(chr(ascii_value))  #store char to output string
        elif command == 'next_cell':
            pointer = (pointer + 1) % len(memory)
        elif command == 'prev_cell':
            pointer = (pointer - 1) % len(memory)
        elif command == 'start_loop':
            if memory[pointer] == 0:
                depth = 1
                while depth > 0:
                    pc += 1
                    if pc >= len(tokens):
                        raise SyntaxError("Loop start has no matching end")
                    if tokens[pc] == 'start_loop':
                        depth += 1
                    elif tokens[pc] == 'end_loop':
                        depth -= 1
            else:
                loop_stack.append(pc)
        elif command == 'end_loop':
            if memory[pointer] != 0:
                pc = loop_stack[-1]
            else:
                loop_stack.pop()
        pc += 1

    #print entire string
    print("Output string:", ''.join(output))

#read file
with open('BUBBLES.eso', 'r') as file:
    code = file.read()

interpret(code)
