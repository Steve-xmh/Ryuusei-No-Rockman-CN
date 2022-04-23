import idc

def mark_thumb_func(addr_push, addr_pop):
    for offset in range(addr_push, addr_pop):
        idc.split_sreg_range(offset, "T", 1)
    idc.create_insn(addr_push)
