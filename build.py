'''
从当前的解包文件中重组成 NDS 游戏文件
目前只能将文字进行重组，其余的玩意还在研究
Pack current workspace into ROM file(s).
'''

import os, sys, filecmp
import shutil, subprocess

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
workspace_path = os.path.join(pydir, '_workspace')
rom_path = os.path.join(pydir, '_rom')
temp_path = os.path.join(pydir, '_temp')
build_path = os.path.join(pydir, '_build')
tools_path = os.path.join(pydir, 'tools')
asm_path = os.path.join(pydir, 'asm')
tpl_path = os.path.join(pydir, 'tpl')
txt_path = os.path.join(pydir, 'txt')
ppl_path = os.path.join(pydir, 'ppl')

def override_copy(src: str, dst: str):
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copy(src, dst)
    
def copytree(src: str, dst: str):
    if os.path.exists(dst):
        for file in os.listdir(src):
            src_file = os.path.join(src, file)
            dst_file = os.path.join(dst, file)
            if os.path.isdir(src_file):
                copytree(src_file, dst_file)
            else:
                override_copy(src_file, dst_file)
    else:
        shutil.copytree(src, dst, copy_function=override_copy)

print('正在清理临时文件夹')
print('Cleaning up temporary directory')
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
print('Setting up temporary directory')
# copytree(workspace_path, os.path.join(temp_path, 'workspace'))
print('_workspace/dragon -> _temp/workspace/dragon')
copytree(os.path.join(workspace_path, 'dragon'), os.path.join(temp_path, 'workspace', 'dragon'))
print('_workspace/leo -> _temp/workspace/leo')
copytree(os.path.join(workspace_path, 'leo'), os.path.join(temp_path, 'workspace', 'leo'))
print('_workspace/pegasus -> _temp/workspace/pegasus')
copytree(os.path.join(workspace_path, 'pegasus'), os.path.join(temp_path, 'workspace', 'pegasus'))
print('_workspace/unpacked_bins -> _temp/workspace/unpacked_bins')
copytree(os.path.join(workspace_path, 'unpacked_bins'), os.path.join(temp_path, 'workspace', 'unpacked_bins'))
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

pixelpet_path = os.path.join(tools_path, 'PixelPet.exe')
def run_pixelpet_script(script_path: str):
    print('正在执行 PixelPet 脚本', script_path)
    subprocess.run([
        pixelpet_path, 'Run-Script', script_path
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
        'Read-Text-Archives', tpl_path, '--format', 'tpl', '--patch', '--recursive',
        'Write-Text-Archives', output_mess_dir, '--format', 'msg',
    ]).check_returncode()

print('正在执行 PixelPet 处理图片')
# 导入部分图像
for file in os.listdir(ppl_path):
    if file.endswith('.in.txt'):
        run_pixelpet_script(os.path.join(ppl_path, file))

# images\【产物】一代大概有字的精灵图导出参考图像
sfpatcher_path = os.path.join(tools_path, 'sfspatcher.exe')
images_path = os.path.join(pydir, 'images', '【产物】一代大概有字的精灵图导出参考图像')
print('正在使用 sfspatcher 修补精灵图')
for subfile in os.listdir(images_path):
    subfile_path = os.path.join(images_path, subfile)
    if os.path.isdir(subfile_path):
        for file in os.listdir(subfile_path):
            if file.endswith('.png'):
                file_path = os.path.join(subfile_path, file)
                # _temp\workspace\unpacked_bins\capcomlogo.bin\capcomlogo_000.bin
                template_file = os.path.join(temp_path, 'workspace', 'unpacked_bins', subfile + ".bin", file.replace('.png', '.bin'))
                print('正在修补', file_path, "到", template_file)
                subprocess.run([
                    sfpatcher_path,
                    # '--verbose',
                    'patch',
                    '--buildin-palette-only', 'true',
                    '-t', file_path,
                    '-i', template_file,
                    '-o', template_file,
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

try:
    print("正在导出脚本大小清单")
    with open(os.path.join(pydir, "hacknote", "script-size-table.txt"), "w", encoding="utf8") as w:
        out_path = os.path.join(temp_path, 'workspace', 'mess_out')
        max_size = 0
        for file in os.listdir(out_path):
            s = os.stat(os.path.join(out_path, file))
            max_size = max(max_size, s.st_size)
            mess_id = int(file[5:9])
            w.write(f"{mess_id:#010x} = {s.st_size}\n")
        w.write(f"max_size = {max_size}\n")
except Exception:
    pass

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
        # if not os.path.isdir(os.path.join(pydir, 'bins', file)): continue
        # if len(os.listdir(os.path.join(pydir, 'bins', file))) == 0: continue
        dest_pack = os.path.join(temp_path, 'packed_bins', file)
        pack_archive(
            os.path.join(temp_path, 'workspace', 'unpacked_bins', file),
            dest_pack
        )
        shutil.copy(dest_pack, os.path.join(temp_path, 'workspace', 'dragon', 'data', 'datbin', 'com'))
        shutil.copy(dest_pack, os.path.join(temp_path, 'workspace', 'leo', 'data', 'datbin', 'com'))
        shutil.copy(dest_pack, os.path.join(temp_path, 'workspace', 'pegasus', 'data', 'datbin', 'com'))

print('正在复制字体')
copytree(os.path.join(workspace_path, 'fonts'), os.path.join(temp_path, 'workspace', 'dragon', 'data', 'datbin', 'fonts'))
copytree(os.path.join(workspace_path, 'fonts'), os.path.join(temp_path, 'workspace', 'leo', 'data', 'datbin', 'fonts'))
copytree(os.path.join(workspace_path, 'fonts'), os.path.join(temp_path, 'workspace', 'pegasus', 'data', 'datbin', 'fonts'))

copytree(os.path.join(pydir, 'fonts'), os.path.join(temp_path, 'workspace', 'dragon', 'data', 'datbin', 'fonts'))
copytree(os.path.join(pydir, 'fonts'), os.path.join(temp_path, 'workspace', 'leo', 'data', 'datbin', 'fonts'))
copytree(os.path.join(pydir, 'fonts'), os.path.join(temp_path, 'workspace', 'pegasus', 'data', 'datbin', 'fonts'))

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
