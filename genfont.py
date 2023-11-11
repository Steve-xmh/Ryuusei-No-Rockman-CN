
import os, sys, subprocess
from os.path import join as pjoin

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
tools_path = pjoin(pydir, 'tools')
tpl_path = pjoin(pydir, 'tpl')
tpl_arm9_path = pjoin(pydir, 'tpl_arm9')
original_tbl_path = pjoin(pydir, 'tools', 'plugins', 'rnr1-utf8-copy.tbl')
generated_tbl_path = pjoin(pydir, 'tools', 'plugins', 'rnr1-utf8-cn.tbl')
workspace_tpl_path = pjoin(pydir, '_workspace', 'mess_out_tpl')

sfonts_path = pjoin(pydir, 'scripts', 'sfonts')
sfont_gen_path = pjoin(tools_path, 'sfont-gen.exe')

subprocess.run([
    sfont_gen_path,
    'gen-table',
    '-i', tpl_path,
    '-i', tpl_arm9_path,
    '-i', workspace_tpl_path,
    '-b', original_tbl_path,
    '-o', generated_tbl_path,
]).check_returncode()

# 我们保留原字体的所有 ASCII（含半角） 全角空格 和 日语平片假名
# 对应的正则表达式是： "[\x00-\x7F\u3040-\u30FF\uFF00-\uFFEF\u3000]"

# 大字体 font3
subprocess.run([
    sfont_gen_path,
    'gen-font',
    '--output-base-font', pjoin(pydir, 'debugdatas', 'font3.bin'),
    '--output-base-width', pjoin(pydir, 'debugdatas', 'font3_width.bin'),
    '--full-space-width', '12',
    '--half-space-width', '6',
    '-t', generated_tbl_path,
    '-o', pjoin(pydir, 'fonts', 'font3.bin'),
    '-w', pjoin(pydir, 'fonts', 'font3_width.bin'),
    '-f', pjoin(sfonts_path, 'cn', 'sf1-jp-font3.sfont'),
    '-f', pjoin(sfonts_path, 'us', 'font-12x12-us.resized.sfont'),
    '-f', pjoin(sfonts_path, 'simsun', 'font-simsun-12x12.cliped.sfont'),
]).check_returncode()

# 字体 font2
subprocess.run([
    sfont_gen_path,
    'gen-font',
    '--output-base-font', pjoin(pydir, 'debugdatas', 'font2.bin'),
    '-t', generated_tbl_path,
    '-o', pjoin(pydir, 'fonts', 'font2.bin'),
    '-f', pjoin(sfonts_path, 'cn', 'sf1-jp-font2.sfont'),
    '-f', pjoin(sfonts_path, 'muzai', 'font-muzai-8x12.mod.shadow.bold.sfont'),
    '-f', pjoin(sfonts_path, 'gb2312', 'gb2312.purified.shifted.shadow.bold.sfont'),
]).check_returncode()

# 字体 font1
subprocess.run([
    sfont_gen_path,
    'gen-font',
    '--output-base-font', pjoin(pydir, 'debugdatas', 'font1.bin'),
    '-t', generated_tbl_path,
    '-o', pjoin(pydir, 'fonts', 'font1.bin'),
    '-f', pjoin(sfonts_path, 'cn', 'sf1-jp-font1.sfont'),
    '-f', pjoin(sfonts_path, 'muzai', 'font-muzai-8x12.mod.shadow.sfont'),
    '-f', pjoin(sfonts_path, 'gb2312', 'gb2312.purified.shifted.shadow.sfont'),
]).check_returncode()
