def interpret(code):
    memory = [0] * 30000
    pointer = 0

    commands = {
        'Oo': 'increment',    
        'OOo': 'decrement',     
        '0O': 'output',        
        '0o0': 'next_cell',    
        'OooO': 'prev_cell',   
        'OoOo': 'start_loop',  
        'oooO': 'end_loop'    
    }

    tokens = []
    i = 0
    while i < len(code):
        if code[i:i+4] in commands:
            tokens.append(commands[code[i:i+4]])
            i += 4
        elif code[i:i+3] in commands:
            tokens.append(commands[code[i:i+3]])
            i += 3
        elif code[i:i+2] in commands:
            tokens.append(commands[code[i:i+2]])
            i += 2
        else:
            i += 1

    pc = 0
    loop_stack = []
    while pc < len(tokens):
        command = tokens[pc]

        if command == 'increment':
            memory[pointer] = (memory[pointer] + 1) % 256
            print(f"Incremented cell {pointer}: {memory[pointer]}")
        elif command == 'decrement':
            memory[pointer] = (memory[pointer] - 1) % 256
            print(f"Decremented cell {pointer}: {memory[pointer]}")
        elif command == 'output':
            print(chr(memory[pointer]), end='')
        elif command == 'next_cell':
            pointer = (pointer + 1) % len(memory)
            print(f"Moved to next cell: {pointer}")
        elif command == 'prev_cell':
            pointer = (pointer - 1) % len(memory)
            print(f"Moved to previous cell: {pointer}")
        elif command == 'start_loop':
            if memory[pointer] == 0:
                depth = 1
                while depth > 0:
                    pc += 1
                    if pc >= len(tokens):
                        raise SyntaxError("Loop start has no matching  ")
                    if tokens[pc] == 'start_loop':
                        depth += 1
                    elif tokens[pc] == 'end_loop':
                        depth -= 1
            else:
                loop_stack.append(pc)  
        elif command == 'end_loop':
            if memory[pointer] != 0:
                pc = loop_stack[-1]  #
            else:
                loop_stack.pop()  

        pc += 1

with open('BUBBLES.eso', 'r') as file:
    code = file.read()

interpret(code)
