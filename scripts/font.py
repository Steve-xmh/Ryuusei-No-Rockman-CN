import math
from re import A, I, match
import json
import os
import re
from PIL import Image, ImageDraw, ImageFont

pydir = os.path.dirname(os.path.abspath(__file__))
default_font_path = os.path.join(pydir, 'simsun.ttc')

# 虽然是 4BPP 但是也就用到了 4 个颜色
color_palettes = [
    0xF7FFF7,
    0x453C3C,
    0xAAAFAA,
    0xDFE7DF,
]

mmsf_color = [
    0xFFFFFF,
    0x423A3A,
    0xCEDEE6,
    0xDEE6DE,
]

color_palettes_ordered = [
    0xF7FFF7,
    0xDFE7DF,
    0xAAAFAA,
    0x453C3C,
]

color_palettes_ordered_byte = [
    0,
    3,
    2,
    1,
]

def split_pixels(data: bytes) -> bytes:
    '''
    把 4bpp 的像素数据转换成单个像素组成的数组数据
    '''
    result = []
    for d in data:
        result.append(d & 0xF)
        result.append((d >> 4) & 0xF)
    return bytes(result)

def concat_pixels(data: bytes) -> bytes:
    '''
    把单个像素组成的数组数据转换成 4bpp 的像素数据
    '''
    assert len(data) % 2 == 0
    result = []
    for i in range(int(len(data) / 2)):
        first_pixel = data[i * 2] & 0xF
        second_pixel = data[i * 2 + 1] & 0xF
        result.append((second_pixel << 4) | first_pixel)
    return bytes(result)

def hex_to_pixels(data: str) -> bytes:
    return bytes([int(x, 16) for x in data])

loaded_font_cache = {}

def get_or_create_font(size: int) -> ImageFont.FreeTypeFont:
    if not size in loaded_font_cache:
        loaded_font_cache[size] = ImageFont.truetype(default_font_path, size=size)
    return loaded_font_cache[size]

wide_r = re.compile(r"\{(.*?)\}")
def calc_chunk_size(character: str) -> int:
    font = get_or_create_font(12)
    (width, height) = font.getsize(character)
    width += 1
    return math.ceil(width / 8)

class Font:
    def __init__(self, block_width: int, block_height: int) -> None:
        self.table = []
        self.widths = []
        self.character_graphs = []
        self.block_width = block_width
        self.block_height = block_height
        pass
    def save_to_bin(self, file_path: str):
        '''
        保存当前字库到文件里
        '''
        with open(file_path, 'wb') as w:
            for graph in self.character_graphs:
                w.write(concat_pixels(graph))
    def dump_widths(self, file_path: str):
        '''
        导出字符宽度表
        '''
        with open(file_path, 'wb') as w:
            w.write(bytes(self.widths))
    def dump_table(self, file_path: str):
        '''
        导出码表，将按照新码表顺序导出
        '''
        with open(file_path, 'w', encoding='utf8') as w:
            counter = 0
            for c in self.table:
                def increase_counter():
                    nonlocal counter
                    left = (counter & 0xFF00) >> 8
                    right = counter & 0xFF
                    if left == 0:
                        right += 1
                        if right == 0xD0:
                            left = 0xD0
                            right = 0
                    elif left == 0xD0 and right == 0x13:
                        left = 0xE4
                        right = 0
                    elif left == 0xE4:
                        right += 1
                        if right > 0xFF:
                            left = 0xD1
                            right = 0x30
                    else:
                        right += 1
                        if right == 0xE4:
                            left += 1
                            right = 0
                    counter = (left << 8) | right
                def get_hex(x):
                    hex_counter = hex(x)[2:]
                    if x < 0x100:
                        hex_counter = '0' * (2 - len(hex_counter)) + hex_counter
                    else:
                        hex_counter = '0' * (4 - len(hex_counter)) + hex_counter
                    return hex_counter
                m = wide_r.match(c)
                if m:
                    s = calc_chunk_size(m[1])
                    for i in range(s):
                        w.write(get_hex(counter).upper())
                        increase_counter()
                else:
                    w.write(get_hex(counter).upper())
                    increase_counter()
                w.write('=')
                if len(c) != 1 and len(set(c)) == 1:
                    w.write('{' + c[0] + '}')     
                else:
                    w.write(c)
                w.write('\n')
            w.write('E900=\\n\n')
    def load_from_json(self, file_path: str):
        with open(file_path, 'r', encoding='utf8') as f:
            font_data = json.load(f)
        font_width = font_data['font_width']
        font_height = font_data['font_height']
        assert font_width <= self.block_width * 8
        assert font_height <= self.block_height * 8
        for [uc, graph_width, graph_data] in font_data['characters']:
            processed_data = ''
            for i in range(font_height):
                processed_data += (
                    graph_data[i * font_width: (i + 1) * font_width] + 
                    '0' * (self.block_width * 8 - font_width)
                )
            for i in range(self.block_height * 8 - font_height):
                processed_data += '0' * self.block_width * 8
            pixels = hex_to_pixels(processed_data)
            if pixels == bytes(len(pixels)): continue
            self.table.append(chr(uc))
            self.widths.append(graph_width)
            self.character_graphs.append(pixels)
    def load_from_original_font(self, file_path: str, tbl_path: str, width_path: str = None):
        '''
        从原始字库里添加字体，将会按照原码表顺序添加
        '''
        added_chars = 0
        with open(tbl_path, 'r', encoding='utf8') as tbl:
            for line in tbl.read().splitlines():
                if len(line.strip()) > 0:
                    [_code, char] = line.split('=', 1)
                    self.table.append(char)
                    # print('Appended', char, added_chars)
                    added_chars += 1
        with open(file_path, 'rb') as file:
            for c in range(added_chars):
                raw_graphs = file.read(int(self.block_width * self.block_height * 64 / 2))
                # print('Read', len(raw_graphs), 'bytes')
                raw_pixels = split_pixels(raw_graphs)
                # print('Splited into', len(raw_pixels), 'pixels')
                self.character_graphs.append(raw_pixels)
                '''
                ordered_pixels = []
                # 1 2
                # 3 4
                for y in range(self.block_height):
                    for x in range(self.block_width):
                        for i in range(8):
                            ordered_pixels.append(raw_pixels[y * self.block_width * 64 + x * 64 + i])
                '''
        if width_path is None:
            for c in range(added_chars):
                self.widths.append(self.block_width * 8)
        else:
            with open(width_path, 'rb') as file:
                for c in range(added_chars):
                    self.widths.append(file.read(1)[0])
    def gen_character(self, character: str, font_size: int, add_to_table = True):
        raw_character = character
        character = character[0]
        matched = wide_r.match(raw_character)
        if character == ' ':
            if character in self.table:
                pos = self.table.index(raw_character)
                self.character_graphs[pos] = bytes(8 * 8 * self.block_width * self.block_height)
                self.widths[pos] = 6
                pass
            else:
                self.table.append(raw_character)
                self.character_graphs.append(bytes(8 * 8 * self.block_width * self.block_height))
                self.widths.append(8)
            return
        elif character == '　':
            if character in self.table:
                pos = self.table.index(raw_character)
                self.character_graphs[pos] = bytes(8 * 8 * self.block_width * self.block_height)
                self.widths[pos] = 12
                pass
            else:
                self.table.append(raw_character)
                self.character_graphs.append(bytes(8 * 8 * self.block_width * self.block_height))
                self.widths.append(8)
            return
        elif matched is not None:
            self.table.append(matched[0])
            chars = list(matched[1])
            fit_size = calc_chunk_size(matched[1])
            i = 0
            while len(chars) < fit_size:
                if chars[i] != '':
                    if i >= len(chars):
                        chars.append('')
                    else:
                        chars.insert(i, '')
                        i += 2
            for c in chars:
                if c == '':
                    self.character_graphs.append(bytes(8 * 8 * self.block_width * self.block_height))
                    self.widths.append(0)
                else:
                    if c in self.table:
                        pos = self.table.index(c)
                        self.character_graphs.append(self.character_graphs[pos])
                        self.widths.append(self.widths[pos])
                    else:
                        self.gen_character(c, font_size, False)
            return
        img = Image.new('L', (self.block_width * 8, self.block_height * 8), 255)
        font = get_or_create_font(font_size)
        (graph_width, _) = font.getsize(character)
        draw = ImageDraw.Draw(img)
        draw.fontmode = "1" # 点阵字体，而非矢量
        draw.text((0, -1), character, 0, font=font)
        pixels = []
        for by in range(self.block_height):
            for bx in range(self.block_width):
                for y in range(8):
                    for x in range(8):
                        pixel = img.getpixel((bx * 8 + x, by * 8 + y))
                        if pixel == 0:
                            pixels.append(1)
                        else:
                            pixels.append(0)
        if add_to_table and raw_character in self.table:
            pos = self.table.index(raw_character)
            self.character_graphs[pos] = bytes(pixels)
            self.widths[pos] = graph_width
            pass
        else:
            if add_to_table:
                self.table.append(raw_character)
            self.character_graphs.append(bytes(pixels))
            self.widths.append(graph_width)

if __name__ == '__main__' and False:
    pass
    f = Font(2, 2)
    f.load_from_original_font('./_workspace/pegasus_fonts/font3.bin', './tools/plugins/rnr1-utf8 copy.tbl')
    for c in '你好世界！':
        f.gen_character(c, 12)
    f.dump_table('rnr1-utf8-out.tbl')
    f.save_to_bin('font3.bin')

if __name__ == '__main__' and False:
    import json, math
    f = Font(2, 2)
    f.load_from_original_font(
        os.path.join(pydir, '..', '_workspace', 'pegasus_fonts', 'font3.bin'),
        os.path.join(pydir, '..', 'tools', 'plugins', 'rnr1-utf8-copy.tbl'),
        os.path.join(pydir, '..', 'scripts', 'font3_width.bin')
    )
    # 俩空格
    f.gen_character(' ', 12)
    f.gen_character('　', 12)
    f.save_to_bin('fontus.bin')

if __name__ == '__main__' and False:
    f = Font(1, 2)
    with open('./scripts/k8x12jcn.hex', 'r') as r:
        for line in r.readlines():
            line = line.strip()
            if len(line) == 4 + 1 + 32:
                [code, graph] = line.split(':')
                f.table.append(chr(int(code, 16)))
                f.widths.append(8)
                data = []
                # print(code, graph)
                for h in graph:
                    b = bin(int(h, 16))
                    b = b[2:].rjust(4, '0')
                    for p in b:
                        data.append(int(p))
                
                for y in range(16 - 1):
                    for x in range(8 - 1):
                        if data[y * 8 + x] == 1:
                            if data[(y + 1) * 8 + x + 1] == 0:
                                data[(y + 1) * 8 + x + 1] = 2
                
                f.character_graphs.append(bytes(data))
