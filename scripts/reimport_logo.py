import os, sys
import subprocess, tempfile
from PIL import Image

join = os.path.join

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
workspace_path = join(pydir, '..', '_workspace')
rom_path = join(pydir, '..', '_rom')
asm_path = join(pydir, '..', 'asm')
tools_path = join(pydir, '..', 'tools')

pixelpet_path = join(tools_path, 'pixelpet.exe')
def run_pixelpet(args: list):
    a = [pixelpet_path]
    a.extend(args)
    subprocess.run(a).check_returncode()

def export_image(
    src_path: str,
    palette_path: str,
    tilemap_path: str,
    tileset_path: str,
    ):
    img = Image.open(src_path)
    tmp_png = tempfile.mktemp(suffix=".png")
    print(tmp_png)
    img.quantize(256).save(tmp_png)
    run_pixelpet([
        'Import-Bitmap', tmp_png,
        'Convert-Bitmap', 'GBA', '--sloppy',
        'Extract-Palettes', '--palette-size', '256',
        'Pad-Palettes', '256',
        # 'Pad-Tileset', '1',
        'Generate-Tilemap', 'NDS-8BPP', '-a',
        'Serialize-Tileset',
        'Export-Bytes', tileset_path,
        'Serialize-Tilemap', '--base-tile', '1',
        'Export-Bytes', tilemap_path,
        'Serialize-Palettes',
        'Export-Bytes', palette_path,
        'Serialize-Palettes',
        'Serialize-Tilemap', '-a', '--base-tile', '1',
        'Serialize-Tileset', '-a',
        'Export-Bytes', src_path + '.bin',
    ])
    os.remove(tmp_png)

capcomlogo_path = join(workspace_path, 'unpacked_bins', 'capcomlogo.bin')
dest_path = join(pydir, '../bins', 'capcomlogo.bin')

export_image(
    join(pydir, '../images', 'title-pegasus.png'),
    os.path.join(dest_path, 'capcomlogo_005.bin'),
    os.path.join(dest_path, 'capcomlogo_004.bin'),
    os.path.join(dest_path, 'capcomlogo_003.bin'),
)

export_image(
    join(pydir, '../images', 'title-leo.png'),
    os.path.join(dest_path, 'capcomlogo_009.bin'),
    os.path.join(dest_path, 'capcomlogo_008.bin'),
    os.path.join(dest_path, 'capcomlogo_007.bin'),
)

export_image(
    join(pydir, '../images', 'title-dragon.png'),
    os.path.join(dest_path, 'capcomlogo_013.bin'),
    os.path.join(dest_path, 'capcomlogo_012.bin'),
    os.path.join(dest_path, 'capcomlogo_011.bin'),
)

export_image(
    join(pydir, '../images', 'title-pegasus.png'),
    os.path.join(dest_path, 'capcomlogo_017.bin'),
    os.path.join(dest_path, 'capcomlogo_016.bin'),
    os.path.join(dest_path, 'capcomlogo_015.bin'),
)
