op_codes = {
    "LOAD": "0000",
    "STORE": "0001",
    "CLEAR": "0010",
    "ADD": "0011",
    "INCREMENT": "0100",
    "SUBTRACT": "0101",
    "DECREMENT": "0110",
    "COMPARE": "0111",
    "JUMP": "1000",
    "JUMPGT": "1001",
    "JUMPEQ": "1010",
    "JUMPLT": "1011",
    "IN": "1101",
    "OUT": "1110",
    "HALT": "1111"
}

symbols = {}

def asmToML(asm):
        asm_strings = asm.strip().split(" ")
        if asm_strings[1] in symbols:
            if isinstance(symbols[asm_strings[1]], list):
                ml = "{}{}".format(op_codes[asm_strings[0]], f'{symbols[asm_strings[1]][-1]:b}'.zfill(12))
            else:
                ml = "{}{}".format(op_codes[asm_strings[0]], f'{symbols[asm_strings[1]]:b}'.zfill(12))
        return ml

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')

def mlToHex(ml):
    return hex(int(ml, 2))

conn = open("program.txt", 'r')
lines = conn.readlines()
conn.close()

bin_conn = open("assembled/binary.txt", 'w')
raw = open("assembled/raw.swag", 'wb+')

#First sweep looking for halt, begin, end, and jump symbols
for i, line in enumerate(lines):
    if 'HALT' in line:
        halt_index = lines.index(line)
    elif '.BEGIN' in line:
        begin_index = lines.index(line)
    elif '.END' in line:
        end_index = lines.index(line)
    elif ':' in line and ".DATA" not in line:
        symbols[line.split(":")[0]] = lines.index(line) - 1
        temp = line.split(":")[1].strip()
        lines.remove(line)
        lines.insert(i, temp)

#Getting all symbols
for i in range(halt_index+2, len(lines)):
    symbols[lines[i].split(":")[0]] = [lines[i].split(".DATA")[-1].strip(), i-1]


#Compile instructions
for i in range(begin_index + 1, halt_index):
    bit_string = asmToML(lines[i])
    binary = bitstring_to_bytes(bit_string)
    print(bit_string)
    #print(mlToHex(bit_string))
    raw.write(binary)

print("")

#Compile symbols
for i in range(end_index + 1, len(lines)):
    bit_string = f'{int(lines[i].split(".DATA")[-1].strip()):b}'.zfill(16)
    binary = bitstring_to_bytes(bit_string)
    raw.write(binary)


bin_conn.close()
raw.close()