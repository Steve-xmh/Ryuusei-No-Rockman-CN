from io import SEEK_SET
import os, sys
import re

input_bin_file = sys.argv[-4]
input_asm_file = sys.argv[-3]
base_address = int(sys.argv[-2], 16)
target_bin_file = sys.argv[-1]

org_regexp = re.compile(r'^\s*\.org\s+(0x[0-9a-fA-F]+)')

with open(input_bin_file, 'rb') as binf:
    with open(target_bin_file, 'rb') as tbinf:
        with open(input_asm_file, 'r', encoding='utf8') as asmf:
            for line in asmf:
                matched = org_regexp.match(line)
                if matched:
                    org_address = int(matched.group(1), 16)
                    print(line)
                    binf.seek(org_address - base_address, SEEK_SET)
                    data = binf.read(16)
                    # search in target file
                    tbinf.seek(0, SEEK_SET)
                    cursor = 0
                    results = []
                    while True:
                        chunk_ = tbinf.read(1)
                        if len(chunk_) == 0:
                            break
                        b = chunk_[0]
                        if data[cursor] == b:
                            cursor += 1
                            if cursor == len(data):
                                target_pos = tbinf.tell() - len(data) + base_address
                                distance = target_pos - org_address
                                if abs(distance) < 0x1000:
                                    results.append((target_pos, abs(distance)))
                                cursor = 0
                        else:
                            cursor = 0
                    if len(results) > 0:
                        results.sort(key=lambda x: x[1])
                        print('\tfound at:', hex(results[0][0]))
                        print('\tdistance:', hex(results[0][1]))
                        