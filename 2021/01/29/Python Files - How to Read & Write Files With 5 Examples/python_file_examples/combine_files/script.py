import os

with open('combined_output.txt', 'w') as fo:
    files = os.listdir('journal')
    for input_file in files:
        with open(f'journal/{input_file}', 'r') as fi:
            fo.write(f'-------------------{input_file}-------------------')
            fo.write('\n')
            fo.write(fi.read())
            fo.write('\n')