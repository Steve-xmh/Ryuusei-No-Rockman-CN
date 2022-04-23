# 根据 CT2 的符号表生成 asm 文件

def read_text(file: str) -> str:
    with open(file, 'r', encoding='utf8', errors='ignore') as r:
        return r.read()

def gen_nitro(txt_file: str, asm_file: str):
    redefined_table = set()
    with open(asm_file, 'w', encoding='utf8') as w:
        w.writelines([
            '; 从 CrystalTile2 生成的 NEF 符号清单中生成的汇编位置信息',
            '\n'
        ])
        for line in read_text(txt_file).splitlines():
            if len(line.strip()) > 0:
                [position, name] = line.strip().split('\t')
                if not(int(position, 16) in range(0x02000000, 0x02400000)):
                    continue
                if name.lower() in redefined_table:
                    i = 0
                    while True:
                        i += 1
                        new_name = name + '_' + str(i)
                        if not (new_name.lower() in redefined_table):
                            name = new_name
                            break
                redefined_table.add(name.lower())
                w.write('.org 0x')
                w.write(position)
                w.write('\n')
                w.write(name)
                w.write(':\n')

gen_nitro('_rom/leo.txt', 'asm/leo/nitro.asm')
gen_nitro('_rom/dragon.txt', 'asm/dragon/nitro.asm')
gen_nitro('_rom/pegasus.txt', 'asm/pegasus/nitro.asm')
