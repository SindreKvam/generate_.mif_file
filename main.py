import numpy as np
import re

decimal_pos = []
ascii_value = []

# https://www.intel.com/content/www/us/en/programmable/quartushelp/13.0/mergedProjects/reference/glossary/def_mif.htm

with open('TableLU.asm') as f:
    lines = f.readlines()

    for line in range(82, len(lines) - 2):  # Skip header by number of lines

        # Ignore line if it's just a newline and whitespace
        if lines[line].strip(' ') != '\n':
            # ASCII value for one line (vertical)
            ascii_value.append(re.findall("([0|1]{8})", lines[line])[0])

            # Position in RAM
            hex_position = re.findall("x([A-F0-9]{2})", lines[line])
            decimal_pos.append(int(hex_position[0], 16))

# remove duplicates in list
decimal_pos = list(dict.fromkeys(decimal_pos))

ascii_array = np.zeros((len(ascii_value), len(ascii_value[0])), dtype=int)

for i in range(len(ascii_value)):
    for x in range(len(ascii_value[i])):
        ascii_array[i, x] = ascii_value[i][x]

depth = max(decimal_pos) + 1
width = 8 * 5

total_bits = depth * width

with open('ascii_table.mif', 'w') as f:
    f.write(f'DEPTH = {depth};\n')
    f.write(f'WIDTH = {width};\n')
    f.write(f'ADDRESS_RADIX = DEC;\n')
    f.write(f'DATA_RADIX = BIN;\n')
    f.write(f'CONTENT\nBEGIN')

    for data in range(depth):
        x, y = data * 5, data * 5 + 5
        f.write(f'\n{data} : ')
        for word in ascii_array[x:y].T:
            # f.write('\n')
            for bit in word:
                f.write(f'{bit}')
        f.write(';')
        print(data)

    f.write('\nEND;')
