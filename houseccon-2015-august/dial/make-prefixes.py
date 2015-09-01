import glob
data = open('dialer.cs', 'r').read()

for prefix in [399, 437, 767, 935]:
    with open('dialer-{}.cs'.format(prefix), 'w') as f:
        f.write(data.replace('LOWVALUE', '311{}0000'.format(prefix)).replace('HIGHVALUE', '311{}0000'.format(prefix+1)).replace("OUTFILE", str(prefix)))

command = ''
for index, filename in enumerate(glob.glob('./dialer-*cs')):
    command += 'csc /out:dialer-prefix{}.exe {} && '.format(index, filename)

print command


