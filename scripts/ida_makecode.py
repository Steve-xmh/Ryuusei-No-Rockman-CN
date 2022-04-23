# 根据 SYM 符号信息，在 IDA 内解析相应的函数并重命名

import os, sys, idc

with open("""G:\Programs\others\Ryuusei-No-Rockman-CN\_rom\pegasus.txt""", 'r', encoding='utf8') as r:
    for line in r.read().splitlines():
        if len(line.strip()) > 0:
            print(line)
            [addr, name] = line.strip().split('\t')
            idc.create_insn(int(addr, 16))
            idc.set_name(int(addr, 16), name, idc.SN_CHECK)
