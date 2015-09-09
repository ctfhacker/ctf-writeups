import string
import glob

for filename in glob.glob('output*.txt'):
    if '00000' in filename:
        continue

    data = open(filename, 'r').read().splitlines()

    for line in data:
        print line
        good = False
        count = 0
        for c in line:
            if c in string.ascii_lowercase or c in string.ascii_uppercase:
                good = True
                count = count + 1

        if good and count > (len(line)/2) and len(line) > 4:
            with open('winning', 'a') as f:
                f.write(line + '\n')
