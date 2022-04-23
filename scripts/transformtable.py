
with open('scripts/transformedtable.txt', 'w', encoding='utf8') as w:
    with open('scripts/originaltable.txt', 'r', encoding='utf8') as r:
        code = 0xD000
        for line in r.read().splitlines():
            [_, char] = line.split('=', 1)
            w.write(hex(code)[2:].upper())
            w.write('=')
            w.write(char)
            w.write('\n')
            code += 1