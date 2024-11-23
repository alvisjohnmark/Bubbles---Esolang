def interpret(code):
    memory = [0] * 30000 
    pointer = 0          

    #map token
    commands = {
        'OoOo': 'increment',       # Increment current cell value
        'OOo': 'decrement',        # Decrement current cell value
        'OoO0': 'output_number',   # Output the current cell as ASCII number
        '00oO': 'output_character',# Output the current cell as ASCII character
        'Oo0O': 'add',             # Add values from two cells
        'O0oO': 'subtract',        # Subtract values from two cells
        'O0Oo': 'multiply',        # Multiply values from two cells
        'OO0O': 'divide',          # Divide values from two cells
        '0o0': 'next_cell',        # Move to the next memory cell
        'OooO': 'prev_cell',       # Move to the previous memory cell
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

    #print tokens
    print("Tokens:", tokens)

    pc = 0
    loop_stack = []
    output = []

    while pc < len(tokens):
        command = tokens[pc]

        if command == 'increment':
            memory[pointer] = (memory[pointer] + 1) % 256

        elif command == 'decrement':
            memory[pointer] = (memory[pointer] - 1) % 256

        elif command == 'output_number':
            ascii_value = memory[pointer]
            output.append(str(ascii_value)) 
            
        elif command == 'output_character':
            ascii_value = memory[pointer]  
            output.append(chr(ascii_value)) 

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

        elif command == 'add':
            #add values from the current cell and the next cell
            next_cell = (pointer + 1) % len(memory)
            memory[pointer] = (memory[pointer] + memory[next_cell]) % 256

        elif command == 'subtract':
            #subtract values from the current cell and the next cell
            next_cell = (pointer + 1) % len(memory)
            memory[pointer] = (memory[pointer] - memory[next_cell]) % 256

        elif command == 'multiply':
            #multiply values from the current cell and the next cell
            next_cell = (pointer + 1) % len(memory)
            memory[pointer] = (memory[pointer] * memory[next_cell]) % 256

        elif command == 'divide':
            #divide values from the current cell by the next cell
            next_cell = (pointer + 1) % len(memory)
            if memory[next_cell] == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            memory[pointer] = (memory[pointer] // memory[next_cell]) % 256


        pc += 1


    print("Output:", ''.join(output))


with open('bubbles.eso', 'r') as file:
    code = file.read()

interpret(code)
