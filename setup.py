"""
这个脚本用于初始化工作环境，包括解压 ROM，解包 BIN 归档文件，和解密相关的资源文件
请注意这将清空工作空间并重新生成，所以在汉化中途除非万不得已就不要再次执行这个脚本了
"""

import os, sys
import shutil
import subprocess

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
workspace_path = os.path.join(pydir, '_workspace')
rom_path = os.path.join(pydir, '_rom')
asm_path = os.path.join(pydir, 'asm')
tools_path = os.path.join(pydir, 'tools')

if os.path.isdir(workspace_path):
    print('警告：发现工作空间文件夹已存在，是否删除并重新配置？(Y/n)')
    print('WARNING: Detected existing workspace directory, do you want to delete and re-configure it? (Y/n)')
    if input() != 'Y':
        exit()

shutil.rmtree(workspace_path, ignore_errors=True)
os.mkdir(workspace_path)

ndstool_path = os.path.join(tools_path, 'ndstool.exe')

def unpack_nds(nds_file: str, dest_dir: str):
    print('正在解压 ROM', nds_file, '到', dest_dir)
    print('Unpacking ROM from', nds_file, 'to', dest_dir)
    os.makedirs(dest_dir, exist_ok=True)
    subprocess.run([
        ndstool_path,
        '-x', nds_file,
        '-9', os.path.join(dest_dir, 'arm9.bin'),
        '-7', os.path.join(dest_dir, 'arm7.bin'),
        '-d', os.path.join(dest_dir, 'data'),
        '-y', os.path.join(dest_dir, 'overlay'),
        '-h', os.path.join(dest_dir, 'header.bin'),
        '-y9', os.path.join(dest_dir, 'y9.bin'),
        '-y7', os.path.join(dest_dir, 'y7.bin'),
        '-t', os.path.join(dest_dir, 'banner.bin'),
    ]).check_returncode()


sfarctool_path = os.path.join(tools_path, 'sfarctool.exe')


def unpack_archive(bin_file: str, dest_dir: str):
    print('正在解包 SFA 归档文件', bin_file, '到', dest_dir)
    print('Unpacking SFA archive from', bin_file, 'to', dest_dir)
    subprocess.run([
        sfarctool_path,
        '-x', '-d',
        '-i', bin_file,
        '-o', dest_dir,
    ]).check_returncode()


pixelpet_path = os.path.join(tools_path, 'pixelpet.exe')
def run_pixelpet(args: list):
    a = [pixelpet_path]
    a.extend(args)
    subprocess.run(a).check_returncode()

def unzip_fonts(input_arm9: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    with open(input_arm9, 'rb') as r:
        with open(os.path.join(output_dir, 'font0.bin'), 'wb') as w:
            r.seek(0xD4B98)
            w.write(r.read(0x20 * 0x1E3))
        with open(os.path.join(output_dir, 'font1.bin'), 'wb') as w:
            r.seek(0xD8798)
            w.write(r.read(0x40 * 0x1E3))
        with open(os.path.join(output_dir, 'font2.bin'), 'wb') as w:
            r.seek(0xE0F98)
            w.write(r.read(0x40 * 0x1E3))
        with open(os.path.join(output_dir, 'font3.bin'), 'wb') as w:
            r.seek(0xE9798)
            w.write(r.read(0x80 * 0x1E3))

armips_path = os.path.join(tools_path, 'armips.exe')
def run_armips(args: list):
    a = [armips_path]
    a.extend(args)
    subprocess.run(a).check_returncode()

textpet_path = os.path.join(tools_path, 'TextPet.exe')
textpet_plugins_path = os.path.join(tools_path, 'plugins')

def transfer_text(mess_dir: str, output_tpl_mess_file: str, output_tpl_mess_dir: str):
    print('正在转换文件夹', mess_dir, '中的脚本归档到', output_tpl_mess_dir)
    print('Transforming text archives directory from', mess_dir, 'to', output_tpl_mess_dir)
    os.mkdir(output_tpl_mess_dir)
    subprocess.run([
        textpet_path,
        'Load-Plugins', textpet_plugins_path,
        'Game', 'rnr1',
        'Read-Text-Archives', mess_dir, '--format', 'msg',
        'Write-Text-Archives', output_tpl_mess_file, '--format', 'tpl', '--single',
        'Write-Text-Archives', output_tpl_mess_dir, '--format', 'tpl',
    ]).check_returncode()


def unpack_all_bin(bins_dir: str, output_dir: str):
    for file in os.listdir(bins_dir):
        if not file.endswith('.bin'):
            continue
        unpack_archive(os.path.join(bins_dir, file),
                       os.path.join(output_dir, file))
        os.makedirs(os.path.join(pydir, 'bins', file), exist_ok=True)


unpack_nds(os.path.join(rom_path, 'dragon.nds'),
           os.path.join(workspace_path, 'dragon'))

unpack_nds(os.path.join(rom_path, 'leo.nds'),
           os.path.join(workspace_path, 'leo'))

unpack_nds(os.path.join(rom_path, 'pegasus.nds'),
           os.path.join(workspace_path, 'pegasus'))


# 缩小 ARM9 字节大小
run_armips([
    os.path.join(asm_path, 'presetup.asm'),
    '-strequ', 'TEMP', os.path.join(workspace_path, 'dragon')
])
run_armips([
    os.path.join(asm_path, 'presetup.asm'),
    '-strequ', 'TEMP', os.path.join(workspace_path, 'leo')
])
run_armips([
    os.path.join(asm_path, 'presetup.asm'),
    '-strequ', 'TEMP', os.path.join(workspace_path, 'pegasus')
])

unzip_fonts(os.path.join(workspace_path, 'pegasus', 'arm9.dec'), os.path.join(workspace_path, 'fonts'))

# 因为三个版本中的归档内容是完全一样的，所以这里只导出一个
unpack_all_bin(os.path.join(workspace_path, 'pegasus', 'data', 'datbin', 'com'),
               os.path.join(workspace_path, 'unpacked_bins'))

# 因为三个版本中的 mess.bin 是完全一样的，所以这里只导出一个
transfer_text(os.path.join(workspace_path, 'unpacked_bins', 'mess.bin'), os.path.join(
    workspace_path, 'mess_out.tpl'), os.path.join(workspace_path, 'mess_out_tpl'))

print('工作环境配置完成！')
print('Configuration done!')
