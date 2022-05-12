'''
扫描脚本，重组/生成字库！
请在打包前执行这个脚本以生成新的字库，确保不会缺失字形。
'''

import os, re, sys, json, math
from scripts.font import Font, get_or_create_font
from PIL import Image, ImageDraw, ImageFont

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
tpl_path = os.path.join(pydir, 'tpl')
tpl_arm9_path = os.path.join(pydir, 'tpl_arm9')
original_tbl_path = os.path.join(pydir, 'tools', 'plugins', 'rnr1-utf8-cn.tbl')
workspace_tpl_path = os.path.join(pydir, '_workspace', 'mess_out_tpl')

FONT_2_SIZE = 12

# 所有日语的平假名和片假名
jp_hiragana_and_katakana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"

tbl_char_texts = set()
char_texts: 'set[str]' = set()

wide_r = re.compile(r"\{(.*?)\}")

def load_tbl(p: str):
    with open(p, 'r', encoding='utf-8', errors='ignored') as r:
        for line in r.read().splitlines():
            if len(line.strip()) > 0:
                [_code, char] = line.split('=', 1)
                if len(char) == 1 and not char in ['\n', '\t', ' ']:
                    tbl_char_texts.add(char)

def check_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as r:
        text = r.read()
        # 单行文字
        for result in re.finditer(r'\"(.*?)\"',text):
            for c in result[0]:
                char_texts.add(c)
            for result in re.finditer(r"\{(.*?)\}", result[0]):
                # 粗体字
                char_texts.add(result[0])
        # 多行文字
        for result in re.finditer(r'(\"\"\")(.*?)(\"\"\")', text, flags=re.DOTALL):
            for c in result.group(0):
                char_texts.add(c)
            for result in re.finditer(r"\{(.*?)\}", result[0]):
                # 粗体字
                char_texts.add(result[0])

def calc_chunk_size(character: str) -> int:
    font = get_or_create_font(FONT_2_SIZE)
    (width, height) = font.getsize(character)
    width += 1
    return math.ceil(width / 8)

def gen_two_half_graph(character: str, bold = False) -> 'list[bytes]':
    font = get_or_create_font(FONT_2_SIZE)
    (width, height) = font.getsize(character)
    width += 1
    chunk_width = math.ceil(width / 8)
    if chunk_width > 11:
        print('警告：要生成的 8x16 宽字', character, '超出 11 个字形限制，可能会导致打印出现损坏！')
    img_width = chunk_width * 8
    img = Image.new('L', (img_width, 16), 255)
    draw = ImageDraw.Draw(img)
    draw.fontmode = "1" # 点阵字体，而非矢量
    offset_x = math.floor((img_width - width) / 2)
    draw.text(         (1 + offset_x, 2), character, 127, font=font)
    if bold: draw.text((2 + offset_x, 2), character, 127, font=font)
    draw.text(         (0 + offset_x, 1), character, 0, font=font)
    if bold: draw.text((1 + offset_x, 1), character, 0, font=font)
    graphs = []
    for cx in range(chunk_width):
        pixels = []
        for cy in range(2):
            for y in range(8):
                for x in range(8):
                    pixel = img.getpixel((cx * 8 + x, cy * 8 + y))
                    if pixel == 0:
                        pixels.append(1)
                    elif pixel == 255:
                        pixels.append(0)
                    else:
                        pixels.append(2)
        graphs.append(bytes(pixels))
    return graphs

def check_dir(dir_path: str):
    for file_or_dir in os.listdir(dir_path):
        joined = os.path.join(dir_path, file_or_dir)
        if os.path.isfile(joined) and joined.endswith('.tpl'):
            check_file(joined)
        elif os.path.isdir(joined):
            check_dir(joined)

def hex_to_bytes(data: str) -> bytes:
    result = []
    for d in data:
        result.append(int(d, 16))
    return bytes(result)

def main():
    print('正在加载原始码表')
    load_tbl(os.path.join(pydir, 'tools', 'plugins', 'rnr1-utf8-copy.tbl'))

    print('正在统计所需字形')
    check_dir(workspace_tpl_path)
    check_dir(tpl_arm9_path)
    check_dir(tpl_path)

    def filter_spaces(c: str):
        return not (c in [' ', '\t', '\n', '', '\\', '[', ']'])

    r = list(char_texts)
    r.sort()
    r = list(filter(filter_spaces, r))

    rr = list(filter(lambda x: not (x in tbl_char_texts), r))
    rr.sort(key=lambda x: len(x))

    print('所需字形数量', len(r)) 
    print('所需生成字形数量', len(rr)) 
    print('正在生成所需字形')

    # 12x12
    f = Font(2, 2)
    f.load_from_original_font(
        os.path.join(pydir, '_workspace', 'fonts', 'font3.bin'),
        os.path.join(pydir, 'tools', 'plugins', 'rnr1-utf8-copy.tbl'),
        os.path.join(pydir, 'scripts', 'font3_width.bin')
    )
    # 直接将昴和 467 号字符替换
    f.gen_character('昴', FONT_2_SIZE)
    f.table[467] = f.table[-1]
    f.table.pop()
    f.character_graphs[467] = f.character_graphs[-1]
    f.character_graphs.pop()
    f.widths[467] = f.widths[-1]
    f.widths.pop()
    # 俩空格
    f.gen_character(' ', FONT_2_SIZE)
    f.gen_character('　', FONT_2_SIZE)

    # 嵌入美版字体
    fontus = {}
    with open(os.path.join(pydir, 'scripts', 'font12_12_us.json'), 'r', encoding='utf8') as r:
        fontus = json.load(r)
        for c in fontus['characters']:
            char = chr(c[0])
            if (not (char in f.table)) and (char in rr):
                f.table.append(chr(c[0]))
                f.widths.append(c[1])
                imgdata = hex_to_bytes(c[2])
                transformed = [0 for x in range(16*16)]
                for y in range(12):
                    for x in range(12):
                        pass
                        ix = math.floor(x / 8)
                        iy = math.floor(y / 8)
                        px = x % 8
                        py = y % 8
                        transformed[iy * 128 + ix * 64 + py * 8 + px] = imgdata[y * 12 + x]
                f.character_graphs.append(bytes(transformed))

    for c in f.table: # 重新生成已有汉字
        if len(c) == 1 and ord(c) in range(0x4E00, 0x9FFF) and (not c in jp_hiragana_and_katakana):
            f.gen_character(c, FONT_2_SIZE)
    for c in rr:
        m = wide_r.match(c)
        if m:
            f.gen_character(m[0], FONT_2_SIZE)
        elif len(c) == 1 and not (c in f.table):
            f.gen_character(c, FONT_2_SIZE)
    f.dump_table(os.path.join(pydir, 'tools', 'plugins', 'rnr1-utf8-cn.tbl'))
    f.save_to_bin(os.path.join(pydir, 'fonts', 'font3.bin'))
    f.dump_widths(os.path.join(pydir, 'fonts', 'font3_width.bin'))

    # 生成粗体窄字体
    gb2312 = Font(1, 2)
    gb2312.load_from_json(os.path.join(pydir, 'scripts', 'font_cn_8_16_bold.json'))
    gb2312.load_from_json(os.path.join(pydir, 'scripts', 'GB2312.json'))
    f = Font(1, 2)
    def replace_or_append(c: str):
        m = wide_r.match(c)
        if m:
            text = m[1]
            # 粗体字
            print('生成粗体字', m[1])
            graphs = gen_two_half_graph(text, True)
            graph = bytes(f.block_width * f.block_height * 8 * 8)
            width = f.block_width * 8
            for graph in graphs:
                f.character_graphs.append(graph)
                f.widths.append(width)
                f.table.append(text)
        else:
            found_graph = False
            graph = bytes(f.block_width * f.block_height * 8 * 8)
            width = f.block_width * 8
            for i in range(len(gb2312.table)):
                if gb2312.table[i] == c:
                    graph = gb2312.character_graphs[i]
                    width = gb2312.widths[i]
                    found_graph = True
                    break
            for i in range(len(f.table)):
                if f.table[i] == c:
                    if graph == bytes(len(graph)):
                        return
                    f.character_graphs[i] = graph
                    f.widths[i] = width
                    found_graph = True
                    return
            if not found_graph:
                print('警告：未找到可用的 8x16 粗体字形：', c, '将使用空白字形代替')
            f.character_graphs.append(graph)
            f.widths.append(width)
            f.table.append(c)

    f = Font(1, 2)
    f.load_from_original_font(
        os.path.join(pydir, '_workspace', 'fonts', 'font2.bin'),
        os.path.join(pydir, 'tools', 'plugins', 'rnr1-utf8-copy.tbl')
    )
    # 直接将昴和 467 号字符替换
    replace_or_append('昴')
    f.table[467] = f.table[-1]
    f.table.pop()
    f.character_graphs[467] = f.character_graphs[-1]
    f.character_graphs.pop()
    f.widths[467] = f.widths[-1]
    f.widths.pop()
    # 俩空格
    f.gen_character(' ', 16)
    f.gen_character('　', 16)
    for c in f.table: # 重新生成已有汉字
        if len(c) == 1 and ord(c) in range(0x4E00, 0x9FFF) and (not c in jp_hiragana_and_katakana):
            replace_or_append(c)
    for c in rr:
        if not (c in f.table):
            replace_or_append(c)
    
    f.save_to_bin(os.path.join(pydir, 'fonts', 'font2.bin'))

    gb2312 = Font(1, 2)
    gb2312.load_from_json(os.path.join(pydir, 'scripts', 'font_cn_8_16.json'))
    gb2312.load_from_json(os.path.join(pydir, 'scripts', 'GB2312.json'))
    
    f = Font(1, 2)
    def replace_or_append(c: str):
        m = wide_r.match(c)
        if m:
            text = m[1]
            # 粗体字
            print('生成粗体字', m[1])
            graphs = gen_two_half_graph(text, False)
            graph = bytes(f.block_width * f.block_height * 8 * 8)
            width = f.block_width * 8
            for graph in graphs:
                f.character_graphs.append(graph)
                f.widths.append(width)
                f.table.append(text)
        else:
            found_graph = False
            graph = bytes(f.block_width * f.block_height * 8 * 8)
            width = f.block_width * 8
            for i in range(len(gb2312.table)):
                if gb2312.table[i] == c:
                    graph = gb2312.character_graphs[i]
                    width = gb2312.widths[i]
                    found_graph = True
                    break
            for i in range(len(f.table)):
                if f.table[i] == c:
                    if graph == bytes(len(graph)):
                        return
                    f.character_graphs[i] = graph
                    f.widths[i] = width
                    found_graph = True
                    return
            if not found_graph:
                print('警告：未找到可用的 8x16 细体字形：', c, '将使用空白字形代替')
            f.character_graphs.append(graph)
            f.widths.append(width)
            f.table.append(c)
    f.load_from_original_font(
        os.path.join(pydir, '_workspace', 'fonts', 'font1.bin'),
        os.path.join(pydir, 'tools', 'plugins', 'rnr1-utf8-copy.tbl')
    )
    # 直接将昴和 467 号字符替换
    replace_or_append('昴')
    f.table[467] = f.table[-1]
    f.table.pop()
    f.character_graphs[467] = f.character_graphs[-1]
    f.character_graphs.pop()
    f.widths[467] = f.widths[-1]
    f.widths.pop()
    # 俩空格
    f.gen_character(' ', 16)
    f.gen_character('　', 16)
    for c in f.table: # 重新生成已有汉字
        if len(c) == 1 and ord(c) in range(0x4E00, 0x9FFF):
            replace_or_append(c)
    for c in rr:
        if not (c in f.table):
            replace_or_append(c)

    f.save_to_bin(os.path.join(pydir, 'fonts', 'font1.bin'))

    print('字库生成完毕！请尝试打包查看效果吧！')
'''
try:
    main()
except Exception as e:
    print('喔不！出错了！')
    print('请查看错误信息，确认问题来由：', e)
    print('报错堆栈')
    print(e.with_traceback(None))
'''
main()
if sys.argv[0].endswith('.exe'):
    print('按回车键退出本程序...')
    input()
