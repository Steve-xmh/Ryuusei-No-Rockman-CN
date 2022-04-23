from io import SEEK_SET
import os

original_areas = [
    ['OriginalPrintFontCondition', 0x0201B158, 0x0201B192],
    ['OriginalAdditionalCondition', 0x0201B114, 0x0201B130],
    ['OriginalPrintAnotherFontCondition', 0x02020060, 0x0202007A],
    ['OriginalPrintInstantFontCondition', 0x0201B254, 0x0201B2A2],
]

with open('_workspace/pegasus/arm9.dec', 'rb') as r:
    for hook in original_areas:
        hook[1] -= 0x02000000
        hook[2] -= 0x02000000
        hook[2] -= hook[1]
        assert hook[2] > 0
        assert hook[1] > 0
        r.seek(hook[1], SEEK_SET)
        hook.append(r.read(hook[2]))

print(original_areas)

def search_arm9(file: str):
    print('Searching', file)
    with open(file, 'rb') as r:
        data = r.read()
    for hook in original_areas:
        findresult = data.find(hook[3])
        if findresult != -1:
            print(hook[0] + 'Start', 'equ', hex(findresult + 0x02000000))
            print(hook[0] + 'End', 'equ', hex(findresult + hook[2] + 0x02000000))
        else:
            print(hook[0], 'can\'t find data')

search_arm9('_workspace/dragon/arm9.dec')
search_arm9('_workspace/leo/arm9.dec')
