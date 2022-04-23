# 检查文件是否是一个精灵格式

import os, struct

'''
x 填充字节
c char
b signed char
B unsigned char
? _Bool
h short
H unsigned short
i int
I unsigned int
l long
L unsigned long
'''

def check_file(file: str) -> bool:
    try:
        with open(file, 'rb') as r:
            r.seek(0, os.SEEK_END)
            fileSize = r.tell()
            r.seek(0, os.SEEK_SET)
            assert fileSize >= 4 * 5
            header = r.read(4 * 5)
            assert len(header) == 4 * 5
            (
                tilesetHeaderPos,
                paletteHeaderPos,
                animationHeaderPos,
                spriteHeaderPos,
                tileNumberShift
            ) = struct.unpack('IIIII', header)
            # TilesetHeader
            r.seek(tilesetHeaderPos)
            tilesetHeader = r.read(2 * 4)
            assert len(tilesetHeader) == 2 * 4
            (
                maxTiles,
                totalTiles,
                tilesetHeaderSize,
                unknownTilesetProperty
            ) = struct.unpack('HHHH', tilesetHeader)
            for i in range(totalTiles):
                tilesetEntry = r.read(2 * 2)
                assert len(tilesetEntry) == 2 * 2
            # PaletteHeader
            r.seek(paletteHeaderPos)
            paletteHeader = r.read(2 * 2)
            assert len(paletteHeader) == 2 * 2
            (
                colorDepth,
                maxPalettesAllowed
            ) = struct.unpack('HH', paletteHeader)
            assert colorDepth == 5 or colorDepth == 6
            # AnimationHeader
            r.seek(animationHeaderPos)
            animationHeader = r.read(2 * 2)
            assert len(animationHeader) == 2 * 2
            (
                totalAnimations,
                unknownAnimationProperty,
            ) = struct.unpack('HH', animationHeader)
            for i in range(totalAnimations):
                animationEntry = r.read(4)
                assert len(animationEntry) == 4
                (animationEntryPos, ) = struct.unpack('I', animationEntry)
                entryPos = r.tell()
                r.seek(animationEntryPos + animationHeaderPos)
                r.seek(entryPos)
        return True
    except AssertionError:
        return False

def get_size(file: str) -> int:
    with open(file, 'rb') as r:
        r.seek(os.SEEK_END)
        return r.tell()

sprite_files = []

for root, dirs, files in os.walk('_workspace'):
    for file in files:
        p = os.path.join(root, file)
        if check_file(p):
            sprite_files.append(p)
        elif get_size(p) == 512:
            pass

with open('疑似精灵文件清单.txt', 'w', encoding='utf8') as w:
    for sprite_file in sprite_files:
        w.write(sprite_file)
        w.write('\n')