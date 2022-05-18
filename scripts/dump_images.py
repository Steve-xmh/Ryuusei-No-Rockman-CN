import os, sys
import subprocess

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
workspace_path = os.path.join(pydir, '..', '_workspace')
rom_path = os.path.join(pydir, '..', '_rom')
asm_path = os.path.join(pydir, '..', 'asm')
tools_path = os.path.join(pydir, '..', 'tools')

pixelpet_path = os.path.join(tools_path, 'pixelpet.exe')
def run_pixelpet(args: list):
    a = [pixelpet_path]
    a.extend(args)
    subprocess.run(a).check_returncode()

def dump_image(
    palette_path: str,
    tilemap_path: str,
    tileset_path: str,
    dest_path: str,
    tiles_per_row: int = 32,
    tiles_per_column: int = 24,
    ):
    run_pixelpet([
        'Import-Bytes', palette_path,
        'Deserialize-Palettes', 'GBA',
        'Import-Bytes', tilemap_path,
        'Deserialize-Tilemap', 'NDS-8BPP', '--base-tile', '1',
        'Import-Bytes', tileset_path,
        'Deserialize-Tileset', 'NDS-8BPP',
        'Render-Tilemap', str(tiles_per_row), str(tiles_per_column),
        'Export-Bitmap', dest_path,
    ])

capcomlogo_path = os.path.join(workspace_path, 'unpacked_bins', 'capcomlogo.bin')

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_000.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_001.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_002.bin'),
    os.path.join(workspace_path, 'capcom.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_005.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_004.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_003.bin'),
    os.path.join(workspace_path, 'title-pegasus.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_009.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_008.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_007.bin'),
    os.path.join(workspace_path, 'title-leo.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_013.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_012.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_011.bin'),
    os.path.join(workspace_path, 'title-dragon.png'),
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_017.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_016.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_015.bin'),
    os.path.join(workspace_path, 'title-none.png'),
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_024.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_022.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_021.bin'),
    os.path.join(workspace_path, 'title-bg.png'),
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_029.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_030.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_028.bin'),
    os.path.join(workspace_path, 'star-force.png'),
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_036.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_037.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_035.bin'),
    os.path.join(workspace_path, 'subscreen-bg-pegasus.png'),
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_039.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_040.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_038.bin'),
    os.path.join(workspace_path, 'subscreen-bg-leo.png'),
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_042.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_043.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_041.bin'),
    os.path.join(workspace_path, 'subscreen-bg-dragon.png'),
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_055.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_056.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_054.bin'),
    os.path.join(workspace_path, 'all-compelete-top.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_055.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_058.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_057.bin'),
    os.path.join(workspace_path, 'all-compelete-bottom.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_061.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_062.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_060.bin'),
    os.path.join(workspace_path, 'pegasus-misc-0.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_064.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_065.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_063.bin'),
    os.path.join(workspace_path, 'leo-misc-0.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_067.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_068.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_066.bin'),
    os.path.join(workspace_path, 'dragon-misc-0.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_071.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_069.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_070.bin'),
    os.path.join(workspace_path, 'subscreen-0.png'),
    tiles_per_column = 32,
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_075.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_073.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_074.bin'),
    os.path.join(workspace_path, 'subscreen-1.png'),
    tiles_per_column = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_079.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_077.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_078.bin'),
    os.path.join(workspace_path, 'subscreen-2.png'),
    tiles_per_column = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_083.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_081.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_082.bin'),
    os.path.join(workspace_path, 'subscreen-3.png'),
    tiles_per_column = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_087.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_085.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_086.bin'),
    os.path.join(workspace_path, 'subscreen-4.png'),
    tiles_per_column = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_090.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_088.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_089.bin'),
    os.path.join(workspace_path, 'subscreen-5.png'),
    tiles_per_column = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_092.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_095.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_094.bin'),
    os.path.join(workspace_path, 'subscreen-6.png'),
    tiles_per_column = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_142.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_137.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_136.bin'),
    os.path.join(workspace_path, 'start-0-top.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_142.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_139.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_138.bin'),
    os.path.join(workspace_path, 'start-0-bottom.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_143.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_141.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_140.bin'),
    os.path.join(workspace_path, 'start-0-bottom-0.png'),
    tiles_per_column = 28,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_178.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_165.bin'),
    os.path.join(workspace_path, 'andromeda.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_177.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_164.bin'),
    os.path.join(workspace_path, 'credit-ship.png'),
    tiles_per_row = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_176.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_163.bin'),
    os.path.join(workspace_path, 'credit-earth.png'),
    tiles_per_row = 32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_175.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_162.bin'),
    os.path.join(workspace_path, 'credit-leo.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_174.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_161.bin'),
    os.path.join(workspace_path, 'credit-dragon.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_173.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_160.bin'),
    os.path.join(workspace_path, 'credit-pegasus.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_172.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_159.bin'),
    os.path.join(workspace_path, 'credit-gemini.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_171.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_158.bin'),
    os.path.join(workspace_path, 'credit-ophiuca.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_170.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_157.bin'),
    os.path.join(workspace_path, 'credit-balance.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_169.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_156.bin'),
    os.path.join(workspace_path, 'credit-harp.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_168.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_155.bin'),
    os.path.join(workspace_path, 'credit-cygnus.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_167.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_154.bin'),
    os.path.join(workspace_path, 'credit-ox.png'),
    tiles_per_row = 40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_166.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_153.bin'),
    os.path.join(workspace_path, 'bg-sky.png'),
    tiles_per_row = 32,
)