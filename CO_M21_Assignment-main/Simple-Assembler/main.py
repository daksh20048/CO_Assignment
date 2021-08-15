def addition(a, b, c):
    overflow = False
    a = b + c
    if a > 65535:
        a = a % 65536
        overflow = True
    return [a, overflow]


def subtraction(a, b, c):
    a = b - c
    if a < 0:
        return [0, True]
    return [a, False]


def move(a, b):
    a = b
    return a


def load(mem_add, c):
    c = mem_add
    return c


def store(a, mem_add):
    mem_add = a
    return mem_add


def invert(a, b):
    a = 65535 - (b % 65536)
    return a


def multiplication(a, b, c):
    overflow = False
    a = b * c
    if a > 65535:
        a = a % 65536
        overflow = True
    return [a, overflow]


def division(a, b):
    q = a // b
    r = a % b
    return [q, r]


def right_shift(a, b):
    a = a // (2 ** b)
    return a


def left_shift(a, b):
    a = a * (2 ** b)
    return a % 65536


def XOR(a, b):
    return a ^ b


def OR(a, b):
    return a | b


def AND(a, b):
    return a & b


def compare(a, b):

    if a > b:
        return [False, True, False]
    elif a < b:
        return [True, False, False]
    else:
        return [False, False, True]


def unconditional_jump(mem_addr):
    return mem_addr


def jump_if_less_than(mem_addr):
    return mem_addr


def jump_if_greater_than(mem_addr):
    return mem_addr


def jump_if_equal(mem_addr):
    return mem_addr


def register_flag(v, l, g, e):
    flag = 0
    if v:
        flag += 8
    if l:
        flag += 4
    if g:
        flag += 2
    if e:
        flag += 1
    return flag


def output_A(opcode, reg1, reg2, reg3):
    unused = "0"
    print(opcode + unused*2 + reg1 + reg2 + reg3)
    return


def output_B(opcode, reg1, val):
    unused = "0"
    val_str = str(bin(val))
    val_str = val_str[2:]
    l = len(val_str)
    if l == 8:
        print(opcode + reg1 + val_str)
        return
    else:
        k = 8 - l
        print(opcode + reg1 + unused * k + val_str)
        return


def output_C(opcode, reg1, reg2):
    unused = "0"
    print(opcode + unused * 5 + reg1 + reg2)
    return


def output_D(opcode, reg1, var):
    unused = "0"
    if len(var) == 8:
        print(opcode + reg1 + var)
        return
    else:
        k = 8 - len(var)
        print(opcode + reg1 + unused * k + var)
        return


def output_E(opcode, var):
    unused = "0"
    k = 11 - len(var)
    print(opcode + unused * k + var)
    return


def output_F(opcode):
    unused = "0"
    print(opcode + unused * 11)
    return


def main():
    r0, r1, r2, r3, r4, r5, r6, flag = 0, 0, 0, 0, 0, 0, 0, 0
    opcode = {"add": "00000", "sub": "00001", "mov": "00010", "mov_reg": "00011", "ld": "00100", "st": "00101", "mul": "00110", "div": "00111", "rs": "01000", "ls": "01001",
              "xor": "01011", "or": "01011", "and": "01100", "not": "01101", "cmp": "01110", "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011" }
    list_registers = ["R0", "R1", "R2", "R3", "R4", "R5", "R6","FLAGS"]
    mem_addr = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110","FLAGS":"111"}
    registers = {"R0": r0, "R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6, "FLAGS": flag}
    variables = {}
    lst_variables = []
    lst_input = []
    v, l, g, e = False, False, False, False
    flags = [v, l, g, e]
    while True:
        try:
            ind = input()
            list1 = ind.split()
            # change
            if ind == "hlt":

                break
            lst_input.append(list1)
        except EOFError:
            break

    hlt_error = False
    mem_addr_int = len(lst_input)
    hlt = 0


    # print(lst_input)

    for j in range(0, len(lst_input)):
        if lst_input[j][0] == "var":
            mem_addr_int -= 1
        if lst_input[j][0] == "hlt":
            hlt += 1
        if lst_input[j][0][-1] == ":":
            mem_addr_int-=1

    if hlt > 1:
        hlt_error = True


    i = 0
    error = 0
    errors = []
    for k in range(0,len(lst_input)):
        # Handling Labels
        if lst_input[k][0][-1] == ":":
            list_registers.append(lst_input[k][0][:-1])
            # print(lst_input[k][0][:-1])
            mem_addr_str = str(bin(mem_addr_int))
            mem_addr_str = mem_addr_str[2:]
            mem_addr.update({lst_input[k][0][:-1]: mem_addr_str})
            # print(mem_addr[lst_input[k][0][:-1]])
            mem_addr_int += 1
            lst_input[k].pop(0)

    while i < len(lst_input):

        # Handling Labels
        # if lst_input[i][0][-1] == ":":
        #     list_registers.append(lst_input[i][0][:-1])
        #     mem_addr_str = str(bin(mem_addr_int))
        #     mem_addr_str = mem_addr_str[2:]
        #     mem_addr.update({lst_input[i][0][:-1]: mem_addr_str})
        #     mem_addr_int+=1
        #     lst_input[i].pop(0)

        if len(lst_input[i]) == 0:
            i += 1
            continue

        # "Halt"
        elif lst_input[i][0] == "hlt":
            output_F(opcode[lst_input[i][0]])
            if i != len(lst_input) - 1:
                hlt += 1
                hlt_error = True
            break

        # Creates Variable
        elif lst_input[i][0] == "var" and len(lst_input[i]) == 2:
            mem_addr_int += 1
            locals()[lst_input[i][1]] = 0
            variables.update({lst_input[i][1]: locals()[lst_input[i][1]]})
            lst_variables.append(lst_input[i][1])
            mem_addr_str = str(bin(mem_addr_int))
            mem_addr_str = mem_addr_str[2:]
            mem_addr.update({lst_input[i][1]: mem_addr_str})


        # Addition
        elif lst_input[i][0] == "add" and len(lst_input[i]) == 4:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers and lst_input[i][3] in list_registers:
                k = addition(registers.get(lst_input[i][1]), registers.get(lst_input[i][2]), registers.get(lst_input[i][3]))
                registers[lst_input[i][1]] = k[0]
                v = k[1]
                registers["FLAGS"] = register_flag(v, l, g, e)
                output_A(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]], mem_addr[lst_input[i][3]])
            else:
                error += 1
                errors.append(i+1)

        # Subtraction
        elif lst_input[i][0] == "sub" and len(lst_input[i]) == 4:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers and lst_input[i][3] in list_registers:
                k = subtraction(registers.get(lst_input[i][1]), registers.get(lst_input[i][2]), registers.get(lst_input[i][3]))
                registers[lst_input[i][1]] = k[0]
                v = k[1]
                registers["FLAGS"] = register_flag(v, l, g, e)
                output_A(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]], mem_addr[lst_input[i][3]])
            else:
                error += 1
                errors.append(i+1)

        # Move Immediate
        elif lst_input[i][0] == "mov" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2][0] == "$":
                s = lst_input[i][2][1:]
                s = int(s)
                registers[lst_input[i][1]] = move(registers[lst_input[i][1]], s)
                output_B(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], s)

        # Move Register
            elif lst_input[i][1] in list_registers and lst_input[i][2] in list_registers:
                registers[lst_input[i][1]] = move(registers[lst_input[i][1]], registers[lst_input[i][2]])
                output_C(opcode["mov_reg"], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]])

            else:
                error += 1
                errors.append(i+1)
            
        # Load
        elif lst_input[i][0] == "ld" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2] in lst_variables:
                registers[lst_input[i][1]] = load(variables[lst_input[i][1]], registers[lst_input[i][1]])
                output_D(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]])
            else:
                error += 1
                errors.append(i+1)
        
        # Store
        elif lst_input[i][0] == "st" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2] in lst_variables:
                variables[lst_input[i][2]] = store(registers[lst_input[i][1]], variables[lst_input[i][2]])
                output_D(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]])
            else:
                error += 1
                errors.append(i+1)
        
        # Multiply
        elif lst_input[i][0] == "mul" and len(lst_input[i]) == 4:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers and lst_input[i][3] in list_registers:
                k = multiplication(registers.get(lst_input[i][1]), registers.get(lst_input[i][2]),registers.get(lst_input[i][3]))
                registers[lst_input[i][1]] = k[0]
                v = k[1]
                registers["FLAGS"] = register_flag(v, l, g, e)
                output_A(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]], mem_addr[lst_input[i][3]])
            else:
                error += 1
                errors.append(i+1)
        
        # Divide
        elif lst_input[i][0] == "div" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers:
                if registers.get(lst_input[i][2]) != 0:
                    k = division(registers.get(lst_input[i][1]), registers.get(lst_input[i][2]))
                    registers["R0"] = k[0]
                    registers["R1"] = k[1]
                    output_C(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]])
                else:
                    error += 1
                    errors.append(i+1)
            else:
                error += 1
                errors.append(i+1)
        
        # Right Shift
        elif lst_input[i][0] == "rs" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2][0] == "$":
                s = lst_input[i][2][1:]
                s = int(s)
                registers[lst_input[i][1]] = right_shift(registers[lst_input[i][1]], s)
                output_B(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], s)
            else:
                error += 1
                errors.append(i+1)
        
        # Left Shift
        elif lst_input[i][0] == "ls" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2][0] == "$":
                s = lst_input[i][2][1:]
                s = int(s)
                registers[lst_input[i][1]] = left_shift(registers[lst_input[i][1]], s)
                output_B(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], s)
            else:
                error += 1
                errors.append(i+1)
        
        # Exclusive OR
        elif lst_input[i][0] == "xor" and len(lst_input[i]) == 4:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers and lst_input[i][3] in list_registers:
                registers[lst_input[i][1]] = XOR(registers.get(lst_input[i][2]), registers.get(lst_input[i][3]))
                output_A(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]], mem_addr[lst_input[i][3]])
            else:
                error += 1
                errors.append(i+1)
        
        # OR
        elif lst_input[i][0] == "or" and len(lst_input[i]) == 4:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers and lst_input[i][3] in list_registers:
                registers[lst_input[i][1]] = OR(registers.get(lst_input[i][2]), registers.get(lst_input[i][3]))
                output_A(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]], mem_addr[lst_input[i][3]])
            else:
                error += 1
                errors.append(i+1)
        
        # AND
        elif lst_input[i][0] == "and" and len(lst_input[i]) == 4:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers and lst_input[i][3] in list_registers:
                registers[lst_input[i][1]] = AND(registers.get(lst_input[i][2]), registers.get(lst_input[i][3]))
                output_A(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]], mem_addr[lst_input[i][3]])
            else:
                error += 1
                errors.append(i+1)
        
        # Invert
        elif lst_input[i][0] == "not" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers:
                registers[lst_input[i][1]] = invert(registers[lst_input[i][1]], registers[lst_input[i][2]])
                output_C(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]])
            else:
                error += 1
                errors.append(i+1)
        
        # Compare
        elif lst_input[i][0] == "cmp" and len(lst_input[i]) == 3:
            if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers:
                k = compare(registers[lst_input[i][1]], registers[lst_input[i][2]])
                l = k[0]
                g = k[1]
                e = k[2]

                registers["FLAGS"] = register_flag(v, l, g, e)
                # print(registers["FLAGS"])
                output_C(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]], mem_addr[lst_input[i][2]])
            else:
                error += 1
                errors.append(i+1)
        
        # Unconditional Jump
        elif lst_input[i][0] == "jmp" and len(lst_input[i]) == 2:
            if lst_input[i][1] in list_registers :
                unconditional_jump(registers[lst_input[i][2]])
                output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
            elif lst_input[i][1] in list_registers and lst_input[i][2] in lst_variables:
                unconditional_jump(variables[lst_input[i][2]])
                output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
            else:
                error += 1
                errors.append(i+1)
        
        # Jump if less than
        elif lst_input[i][0] == "jlt" and len(lst_input[i]) == 2:
            if lst_input[i][1] in list_registers:
                output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
                if l:
                    if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers:
                        jump_if_less_than(registers[lst_input[i][2]])
                        # output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
                    if lst_input[i][1] in list_registers and lst_input[i][2] in lst_variables:
                        jump_if_less_than(variables[lst_input[i][2]])
                        # output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
            else:
                error += 1
                errors.append(i+1)
        
        # Jump if greater than
        elif lst_input[i][0] == "jgt" and len(lst_input[i]) == 2:
            if lst_input[i][1] in list_registers :
                # print(g)
                output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
                if g:
                    if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers:
                        jump_if_greater_than(registers[lst_input[i][2]])
                        # output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
                    if lst_input[i][1] in list_registers and lst_input[i][2] in lst_variables:
                        jump_if_greater_than(variables[lst_input[i][2]])
                        # output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
            else:
                error += 1
                errors.append(i+1)
        
        # Jump if equal
        elif lst_input[i][0] == "je" and len(lst_input[i]) == 2:
            if lst_input[i][1] in list_registers :
                output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
                if e:
                    if lst_input[i][1] in list_registers and lst_input[i][2] in list_registers:
                        jump_if_equal(registers[lst_input[i][2]])
                        # output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
                    if lst_input[i][1] in list_registers and lst_input[i][2] in lst_variables:
                        jump_if_equal(variables[lst_input[i][2]])
                        # output_E(opcode[lst_input[i][0]], mem_addr[lst_input[i][1]])
            else:
                error += 1
                errors.append(i+1)
        
        # None of the syntax match "Syntax Error"
        else:
            error += 1
            errors.append(i+1)  # maintains list of lines on which error is generated

        i += 1
    # change
    output_F(opcode["hlt"])


    if hlt_error:
        print("Halt Error")

    if error > 0:
        print("Syntax Error On Line" + str(errors[0]))


if __name__ == '__main__':
    main()
