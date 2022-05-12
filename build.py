'''
从当前的解包文件中重组成 NDS 游戏文件
目前只能将文字进行重组，其余的玩意还在研究（大雾）
'''

from distutils import dir_util
import os, sys, filecmp
import shutil, subprocess
from distutils.dir_util import copy_tree

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
workspace_path = os.path.join(pydir, '_workspace')
rom_path = os.path.join(pydir, '_rom')
temp_path = os.path.join(pydir, '_temp')
build_path = os.path.join(pydir, '_build')
tools_path = os.path.join(pydir, 'tools')
asm_path = os.path.join(pydir, 'asm')
tpl_path = os.path.join(pydir, 'tpl')
txt_path = os.path.join(pydir, 'txt')

print('正在清理临时文件夹')
shutil.rmtree(temp_path, ignore_errors=True)
os.mkdir(temp_path)

def is_dir_different(path1: str, path2: str):
    return len(filecmp.dircmp(path1, path2).diff_files) > 0

armips_path = os.path.join(tools_path, 'armips.exe')
def run_armips(args: list):
    a = [armips_path]
    a.extend(args)
    subprocess.run(a).check_returncode()

print('正在复制工作空间到临时文件夹')
# shutil.copytree(workspace_path, os.path.join(temp_path, 'workspace'))
print('_workspace/dragon -> _temp/workspace/dragon')
shutil.copytree(os.path.join(workspace_path, 'dragon'), os.path.join(temp_path, 'workspace', 'dragon'))
print('_workspace/leo -> _temp/workspace/leo')
shutil.copytree(os.path.join(workspace_path, 'leo'), os.path.join(temp_path, 'workspace', 'leo'))
print('_workspace/pegasus -> _temp/workspace/pegasus')
shutil.copytree(os.path.join(workspace_path, 'pegasus'), os.path.join(temp_path, 'workspace', 'pegasus'))
print('_workspace/unpacked_bins -> _temp/workspace/unpacked_bins')
dir_util.copy_tree(os.path.join(workspace_path, 'unpacked_bins'), os.path.join(temp_path, 'workspace', 'unpacked_bins'))
print('bins -> _temp/workspace/unpacked_bins')
for subdir in os.listdir(os.path.join(pydir, 'bins')):
    for file in os.listdir(os.path.join(pydir, 'bins', subdir)):
        print(f'{subdir}/{file}', '->', f'{temp_path}/workspace/unpacked_bins/{subdir}/{file}')
        if os.path.exists(os.path.join(temp_path, 'workspace', 'unpacked_bins', subdir, file)):
            os.remove(os.path.join(temp_path, 'workspace', 'unpacked_bins', subdir, file))
        shutil.copy(os.path.join(pydir, 'bins', subdir, file), os.path.join(temp_path, 'workspace', 'unpacked_bins', subdir))

ndstool_path = os.path.join(tools_path, 'ndstool.exe')
def pack_nds(unpacked_dir: str, output_nds_file: str):
    print('正在从解包文件夹', unpacked_dir, '打包到', output_nds_file)
    subprocess.run([
        ndstool_path,
        '-c', output_nds_file,
        '-9', os.path.join(unpacked_dir, 'arm9.bin'),
        '-7', os.path.join(unpacked_dir, 'arm7.bin'),
        '-d', os.path.join(unpacked_dir, 'data'),
        '-y', os.path.join(unpacked_dir, 'overlay'),
        '-h', os.path.join(unpacked_dir, 'header.bin'),
        '-y9', os.path.join(unpacked_dir, 'y9.bin'),
        '-y7', os.path.join(unpacked_dir, 'y7.bin'),
        '-t', os.path.join(unpacked_dir, 'banner.bin'),
    ]).check_returncode()

sfarctool_path = os.path.join(tools_path, 'sfarctool.exe')
def pack_archive(from_dir: str, dest_bin: str):
    print('正在打包文件夹 ', from_dir, '到 SFA 归档文件', dest_bin)
    os.makedirs(os.path.dirname(dest_bin), exist_ok=True)
    subprocess.run([
        sfarctool_path,
        '-p',
        '-i', from_dir,
        '-o', dest_bin,
    ]).check_returncode()

textpet_path = os.path.join(tools_path, 'TextPet.exe')
textpet_plugins_path = os.path.join(tools_path, 'plugins')

def pack_mess(mess_tpl_dir: str, output_mess_dir: str):
    print('正在转换文件夹', mess_tpl_dir, '中的脚本归档到', output_mess_dir)
    os.mkdir(output_mess_dir)
    subprocess.run([
        textpet_path,
        'Load-Plugins', textpet_plugins_path,
        'Game', 'rnr1-cn',
        'Read-Text-Archives', mess_tpl_dir, '--format', 'tpl',
        'Read-Text-Archives', tpl_path, '--format', 'tpl', '--patch',
        'Write-Text-Archives', output_mess_dir, '--format', 'msg',
    ]).check_returncode()

print('正在打包嵌入脚本')
os.mkdir(os.path.join(temp_path, 'tpl_arm9'))
subprocess.run([
    textpet_path,
    'Load-Plugins', textpet_plugins_path,
    'Game', 'rnr1-cn',
    'Read-Text-Archives', os.path.join(pydir, 'tpl_arm9'), '--format', 'tpl',
    'Write-Text-Archives', os.path.join(temp_path, 'tpl_arm9'), '--format', 'msg',
]).check_returncode()

print('正在编译 ARM9 代码')

print('正在编译天马版代码')
run_armips([
    os.path.join(asm_path, 'pegasus', '_main.asm'),
    '-sym', os.path.join(temp_path, 'workspace', 'pegasus.sym'),
    '-strequ', 'TEMP', os.path.join(temp_path, 'workspace', 'pegasus')
])
print('正在编译青龙版代码')
run_armips([
    os.path.join(asm_path, 'dragon', '_main.asm'),
    '-sym', os.path.join(temp_path, 'workspace', 'dragon.sym'),
    '-strequ', 'TEMP', os.path.join(temp_path, 'workspace', 'dragon')
])
print('正在编译雄狮版代码')
run_armips([
    os.path.join(asm_path, 'leo', '_main.asm'),
    '-sym', os.path.join(temp_path, 'workspace', 'leo.sym'),
    '-strequ', 'TEMP', os.path.join(temp_path, 'workspace', 'leo')
])

print('正在给文本打上更改补丁')
pack_mess(
    os.path.join(workspace_path, 'mess_out_tpl'),
    os.path.join(temp_path, 'workspace', 'mess_out'),
)

mess_out_path = os.path.join(temp_path, 'workspace', 'mess.bin')
pack_archive(os.path.join(temp_path, 'workspace', 'mess_out'), mess_out_path)

shutil.copy(mess_out_path, os.path.join(temp_path, 'workspace', 'dragon', 'data', 'datbin', 'com', 'mess.bin'))
shutil.copy(mess_out_path, os.path.join(temp_path, 'workspace', 'leo', 'data', 'datbin', 'com', 'mess.bin'))
shutil.copy(mess_out_path, os.path.join(temp_path, 'workspace', 'pegasus', 'data', 'datbin', 'com', 'mess.bin'))

# 打包其他归档
packed_bins_path = os.path.join(temp_path, 'packed_bins')
if True:
    for file in os.listdir(os.path.join(workspace_path, 'unpacked_bins')):
        if file == 'mess.bin': continue
        if len(os.listdir(os.path.join(pydir, 'bins', file))) == 0: continue
        dest_pack = os.path.join(temp_path, 'packed_bins', file)
        pack_archive(
            os.path.join(temp_path, 'workspace', 'unpacked_bins', file),
            dest_pack
        )
        shutil.copy(dest_pack, os.path.join(temp_path, 'workspace', 'dragon', 'data', 'datbin', 'com'))
        shutil.copy(dest_pack, os.path.join(temp_path, 'workspace', 'leo', 'data', 'datbin', 'com'))
        shutil.copy(dest_pack, os.path.join(temp_path, 'workspace', 'pegasus', 'data', 'datbin', 'com'))

print('正在复制字体')
copy_tree(os.path.join(workspace_path, 'fonts'), os.path.join(temp_path, 'workspace', 'dragon', 'data', 'datbin', 'fonts'))
copy_tree(os.path.join(workspace_path, 'fonts'), os.path.join(temp_path, 'workspace', 'leo', 'data', 'datbin', 'fonts'))
copy_tree(os.path.join(workspace_path, 'fonts'), os.path.join(temp_path, 'workspace', 'pegasus', 'data', 'datbin', 'fonts'))

copy_tree(os.path.join(pydir, 'fonts'), os.path.join(temp_path, 'workspace', 'dragon', 'data', 'datbin', 'fonts'))
copy_tree(os.path.join(pydir, 'fonts'), os.path.join(temp_path, 'workspace', 'leo', 'data', 'datbin', 'fonts'))
copy_tree(os.path.join(pydir, 'fonts'), os.path.join(temp_path, 'workspace', 'pegasus', 'data', 'datbin', 'fonts'))

if not os.path.isdir(build_path): os.mkdir(build_path)

print('正在复制代码调试符号表')
try:
    shutil.copy(os.path.join(temp_path, 'workspace', 'leo.sym'), os.path.join(build_path, 'leo.sym'))
    shutil.copy(os.path.join(temp_path, 'workspace', 'dragon.sym'), os.path.join(build_path, 'dragon.sym'))
    shutil.copy(os.path.join(temp_path, 'workspace', 'pegasus.sym'), os.path.join(build_path, 'pegasus.sym'))
except Exception as e:
    print(e)

print('正在重组游戏')
pack_nds(os.path.join(temp_path, 'workspace', 'pegasus'), os.path.join(build_path, 'pegasus.nds'))
pack_nds(os.path.join(temp_path, 'workspace', 'dragon'), os.path.join(build_path, 'dragon.nds'))
pack_nds(os.path.join(temp_path, 'workspace', 'leo'), os.path.join(build_path, 'leo.nds'))
