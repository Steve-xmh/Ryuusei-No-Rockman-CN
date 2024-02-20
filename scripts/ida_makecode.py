# 根据 SYM 符号信息，在 IDA 内解析相应的函数并重命名
import os, sys, idc, idaapi

names = set()

with open("""G:\Programs\others\Ryuusei-No-Rockman-2-CN\_rom\\ninja.txt""", 'r', encoding='utf8') as r:
    for line in r.read().splitlines():
        if len(line.strip()) > 0:
            try:
                print(line)
                [addr, raw_name] = line.strip().split('\t')
                if raw_name.startswith('REG_'):
                    continue
                if raw_name.startswith('HW_'):
                    continue
                name = raw_name
                counter = 1
                while name in names:
                    name = raw_name + '_' + str(counter)
                    counter += 1
                names.add(name)
                addr_int = int(addr, 16)
                inst = idc.generate_disasm_line(addr_int, idc.GENDSM_FORCE_CODE)
                if inst.startswith("PUSH"):
                    idc.create_insn(addr_int)
                    idaapi.add_func(addr_int)
                idc.set_name(addr_int, name, idc.SN_NOCHECK)
            except Exception:
                pass
