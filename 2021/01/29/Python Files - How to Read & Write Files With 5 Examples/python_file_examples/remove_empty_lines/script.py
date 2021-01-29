with open('essay.txt', 'r') as fi, open('essay_formatted.txt', 'w') as fo:
    lines = fi.readlines()
    for line in lines:
        if line.strip() != '':
            fo.write(line.strip())
            fo.write('\n')