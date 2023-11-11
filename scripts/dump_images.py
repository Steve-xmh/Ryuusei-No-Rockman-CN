import os
import sys
import subprocess

pydir = os.path.dirname(os.path.realpath(sys.argv[0]))
workspace_path = os.path.join(pydir, '..', '_workspace')
images_path = os.path.join(pydir, '..', 'images')
rom_path = os.path.join(pydir, '..', '_rom')
temp_path = os.path.join(pydir, '..', '_temp')
asm_path = os.path.join(pydir, '..', 'asm')
tools_path = os.path.join(pydir, '..', 'tools')

pixelpet_path = os.path.join(tools_path, 'pixelpet.exe')


def run_pixelpet(args: list):
    # return
    a = [pixelpet_path]
    a.extend(args)
    subprocess.run(a, stdout=subprocess.DEVNULL).check_returncode()


def dump_image(
    palette_path: str,
    tilemap_path: str,
    tileset_path: str,
    dest_path: str,
    tiles_per_row: int = 32,
    tiles_per_column: int = 24,
    base_tile: int = 1,
    reimport_image: str = None,
    reimport_tileset: str = None,
    reimport_tilemap: str = None,
):
    print("Dumping", os.path.relpath(palette_path), os.path.relpath(
        tilemap_path), os.path.relpath(tileset_path), "to", os.path.relpath(dest_path))
    run_pixelpet([
        'Import-Bytes', palette_path,
        'Deserialize-Palettes', 'GBA',
        'Import-Bytes', tilemap_path,
        'Deserialize-Tilemap', 'NDS-8BPP', '--base-tile', str(base_tile),
        'Import-Bytes', tileset_path,
        'Deserialize-Tileset', 'NDS-8BPP',
        'Render-Tilemap', str(tiles_per_row), str(tiles_per_column),
        'Export-Bitmap', dest_path,
    ])
    if reimport_tileset is not None and reimport_tilemap is not None and reimport_image is not None:
        dest_txt_path = dest_path.replace('.png', '.in.txt')
        palette_path = os.path.relpath(palette_path, os.path.join(pydir, '..'))
        reimport_image = os.path.relpath(
            reimport_image, os.path.join(pydir, '..'))
        reimport_tileset = os.path.relpath(
            reimport_tileset, os.path.join(pydir, '..'))
        reimport_tilemap = os.path.relpath(
            reimport_tilemap, os.path.join(pydir, '..'))
        with open(dest_txt_path, 'w', encoding='utf8') as f:
            f.write(f'Import-Bytes "{palette_path}"\n')
            f.write(f'Deserialize-Palettes GBA\n')
            f.write(f'Import-Bitmap "{reimport_image}"\n')
            f.write(f'Convert-Bitmap GBA --sloppy\n')
            # if base_tile > 0: f.write(f'Pad-Tileset {base_tile}\n')
            f.write(
                f'Generate-Tilemap NDS-8BPP\n')
            f.write(f'Serialize-Tileset\n')
            f.write(f'Export-Bytes "{reimport_tileset}"\n')
            f.write(f'Serialize-Tilemap --base-tile {base_tile}\n')
            f.write(f'Export-Bytes "{reimport_tilemap}"\n')
            # if base_tile > 0:
            #     f.write(f'Import-Bytes "{reimport_tileset}" -o {base_tile * 8 * 8}\n')
            #     f.write(f'Export-Bytes "{reimport_tileset}"\n')


def dump_image_gba(
    palette_path: str,
    tilemap_path: str,
    tileset_path: str,
    dest_path: str,
    tiles_per_row: int = 32,
    tiles_per_column: int = 24,
    base_tile: int = 1,
    reimport_image: str = None,
    reimport_tileset: str = None,
    reimport_tilemap: str = None,
):
    print("Dumping (GBA)", os.path.relpath(palette_path), os.path.relpath(
        tilemap_path), os.path.relpath(tileset_path), "to", os.path.relpath(dest_path))
    run_pixelpet([
        'Import-Bytes', palette_path,
        'Deserialize-Palettes', 'GBA',
        'Import-Bytes', tilemap_path,
        'Deserialize-Tilemap', 'GBA-4BPP', '--base-tile', str(base_tile),
        'Import-Bytes', tileset_path,
        'Deserialize-Tileset', 'GBA-4BPP',
        'Render-Tilemap', str(tiles_per_row), str(tiles_per_column),
        'Export-Bitmap', dest_path,
    ])
    if reimport_tileset is not None and reimport_tilemap is not None and reimport_image is not None:
        dest_txt_path = dest_path.replace('.png', '.in.txt')
        palette_path = os.path.relpath(palette_path, os.path.join(pydir, '..'))
        reimport_image = os.path.relpath(
            reimport_image, os.path.join(pydir, '..'))
        reimport_tileset = os.path.relpath(
            reimport_tileset, os.path.join(pydir, '..'))
        reimport_tilemap = os.path.relpath(
            reimport_tilemap, os.path.join(pydir, '..'))
        with open(dest_txt_path, 'w', encoding='utf8') as f:
            f.write(f'Import-Bytes "{palette_path}"\n')
            f.write(f'Deserialize-Palettes GBA\n')
            f.write(f'Import-Bitmap "{reimport_image}"\n')
            f.write(f'Convert-Bitmap GBA --sloppy\n')
            # if base_tile > 0: f.write(f'Pad-Tileset {base_tile}\n')
            f.write(
                f'Generate-Tilemap GBA-4BPP\n')
            f.write(f'Serialize-Tileset\n')
            f.write(f'Export-Bytes "{reimport_tileset}"\n')
            f.write(f'Serialize-Tilemap --base-tile {base_tile}\n')
            f.write(f'Export-Bytes "{reimport_tilemap}"\n')
            # if base_tile > 0:
            #     f.write(f'Import-Bytes "{reimport_tileset}" -o {base_tile * 8 * 4}\n')
            #     f.write(f'Export-Bytes "{reimport_tileset}"\n')


capcomlogo_path = os.path.join(
    workspace_path, 'unpacked_bins', 'capcomlogo.bin')
subscreen_path = os.path.join(workspace_path, 'unpacked_bins', 'subscreen.bin')
shop_path = os.path.join(workspace_path, 'unpacked_bins', 'shop.bin')
cardforce_path = os.path.join(workspace_path, 'unpacked_bins', 'fieldcardforce.bin')
result_path = os.path.join(workspace_path, 'unpacked_bins', 'result.bin')

result_column_list = [
    15,
    8,
    3,
    3,
    3,
    8,
    8,
    15,
]
for i in range(8):
    dump_image_gba(
        palette_path=os.path.join(result_path, f'result_{str(i ).zfill(2)}.bin'),
        tilemap_path=os.path.join(result_path, f'result_{str(i + 16).zfill(2)}.bin'),
        tileset_path=os.path.join(result_path, f'result_{str(i + 8).zfill(2)}.bin'),
        dest_path=os.path.join(workspace_path, f'result_{i}.png'),
        reimport_image=os.path.join(images_path, f'result_{i}.png'),
        reimport_tileset=os.path.join(temp_path, f'workspace/unpacked_bins/result.bin/result_{str(i + 8).zfill(2)}.bin'),
        reimport_tilemap=os.path.join(temp_path, f'workspace/unpacked_bins/result.bin/result_{str(i + 16).zfill(2)}.bin'),
        base_tile=0,
        tiles_per_column=result_column_list[i]
    )

dump_image(
    tileset_path=os.path.join(cardforce_path, 'fieldcardforce_00.bin'),
    tilemap_path=os.path.join(cardforce_path, 'fieldcardforce_01.bin'),
    palette_path=os.path.join(cardforce_path, 'fieldcardforce_03.bin'),
    dest_path=os.path.join(workspace_path, 'fieldcardforce_0.png'),
    reimport_image=os.path.join(images_path, 'fieldcardforce_0.png'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/fieldcardforce.bin/fieldcardforce_00.bin'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/fieldcardforce.bin/fieldcardforce_01.bin'),
    base_tile=0,
)
for i in range(5):
    dump_image(
        tileset_path=os.path.join(cardforce_path, f'fieldcardforce_{str(i * 2 + 4).zfill(2)}.bin'),
        tilemap_path=os.path.join(cardforce_path, f'fieldcardforce_{str(i * 2 + 5).zfill(2)}.bin'),
        palette_path=os.path.join(cardforce_path, 'fieldcardforce_03.bin'),
        dest_path=os.path.join(workspace_path, f'fieldcardforce_{i + 1}.png'),
        reimport_image=os.path.join(images_path, f'fieldcardforce_{i + 1}.png'),
        reimport_tileset=os.path.join(temp_path, f'workspace/unpacked_bins/fieldcardforce.bin/fieldcardforce_{str(i * 2 + 4).zfill(2)}.bin'),
        reimport_tilemap=os.path.join(temp_path, f'workspace/unpacked_bins/fieldcardforce.bin/fieldcardforce_{str(i * 2 + 5).zfill(2)}.bin'),
        base_tile=0,
        tiles_per_row=16,
        tiles_per_column=8,
    )
    dump_image(
        tileset_path=os.path.join(cardforce_path, f'fieldcardforce_{str(i * 3 + 14).zfill(2)}.bin'),
        palette_path=os.path.join(cardforce_path, f'fieldcardforce_{str(i * 3 + 15).zfill(2)}.bin'),
        tilemap_path=os.path.join(cardforce_path, f'fieldcardforce_{str(i * 3 + 16).zfill(2)}.bin'),
        dest_path=os.path.join(workspace_path, f'fieldcardforce_mugshot_{i + 1}.png'),
        reimport_image=os.path.join(images_path, f'fieldcardforce_mugshot_{i + 1}.png'),
        reimport_tileset=os.path.join(temp_path, f'workspace/unpacked_bins/fieldcardforce.bin/fieldcardforce_{str(i * 3 + 14).zfill(2)}.bin'),
        reimport_tilemap=os.path.join(temp_path, f'workspace/unpacked_bins/fieldcardforce.bin/fieldcardforce_{str(i * 3 + 16).zfill(2)}.bin'),
        base_tile=0,
        tiles_per_row=18,
        tiles_per_column=16,
    )

dump_image(
    os.path.join(shop_path, 'shop_0.bin'),
    os.path.join(shop_path, 'shop_1.bin'),
    os.path.join(shop_path, 'shop_2.bin'),
    os.path.join(workspace_path, 'shop.png'),
    reimport_image=os.path.join(images_path, 'shop.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/shop.bin/shop_1.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/shop.bin/shop_2.bin'),
)
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
)

dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_075.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_073.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_074.bin'),
    os.path.join(workspace_path, 'subscreen-1.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_079.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_077.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_078.bin'),
    os.path.join(workspace_path, 'subscreen-2.png'),
    reimport_image=os.path.join(images_path, 'subscreen-2.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/capcomlogo.bin/capcomlogo_077.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/capcomlogo.bin/capcomlogo_078.bin'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_083.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_081.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_082.bin'),
    os.path.join(workspace_path, 'subscreen-3.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_087.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_085.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_086.bin'),
    os.path.join(workspace_path, 'subscreen-4.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_090.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_088.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_089.bin'),
    os.path.join(workspace_path, 'subscreen-5.png'),
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_092.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_095.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_094.bin'),
    os.path.join(workspace_path, 'subscreen-6.png'),
    tiles_per_column=32,
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
    tiles_per_column=28,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_178.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_165.bin'),
    os.path.join(workspace_path, 'andromeda.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_177.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_164.bin'),
    os.path.join(workspace_path, 'credit-ship.png'),
    tiles_per_row=32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_176.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_163.bin'),
    os.path.join(workspace_path, 'credit-earth.png'),
    tiles_per_row=32,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_175.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_162.bin'),
    os.path.join(workspace_path, 'credit-leo.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_174.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_161.bin'),
    os.path.join(workspace_path, 'credit-dragon.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_173.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_160.bin'),
    os.path.join(workspace_path, 'credit-pegasus.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_172.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_159.bin'),
    os.path.join(workspace_path, 'credit-gemini.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_171.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_158.bin'),
    os.path.join(workspace_path, 'credit-ophiuca.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_170.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_157.bin'),
    os.path.join(workspace_path, 'credit-balance.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_169.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_156.bin'),
    os.path.join(workspace_path, 'credit-harp.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_168.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_155.bin'),
    os.path.join(workspace_path, 'credit-cygnus.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_167.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_154.bin'),
    os.path.join(workspace_path, 'credit-ox.png'),
    tiles_per_row=40,
)
dump_image(
    os.path.join(capcomlogo_path, 'capcomlogo_152.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_166.bin'),
    os.path.join(capcomlogo_path, 'capcomlogo_153.bin'),
    os.path.join(workspace_path, 'bg-sky.png'),
    tiles_per_row=32,
)

dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_001.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_002.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_003.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_1.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_013.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_014.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_015.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_2.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_025.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_026.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_027.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_3.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_040.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_041.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_042.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_4.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_063.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_064.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_065.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_5.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_5.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_065.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_063.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_066.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_067.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_068.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_6.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_6.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_068.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_066.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_069.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_070.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_071.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_7.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_7.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_071.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_069.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_081.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_082.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_083.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_8.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_8.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_083.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_081.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_084.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_085.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_086.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_9.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_9.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_086.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_084.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_087.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_088.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_089.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_10.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_10.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_089.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_087.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_090.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_091.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_092.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_11.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_11.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_092.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_090.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_107.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_108.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_109.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_12.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_12.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_109.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_107.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_114.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_115.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_116.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_13.png'),
    tiles_per_row=64,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_125.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_126.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_127.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_14.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_148.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_149.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_150.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_15.png'),
    tiles_per_row=64,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_175.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_176.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_177.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_16.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_179.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_180.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_181.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_17.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_222.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_223.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_225.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_18.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_18.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_223.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_222.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_235.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_236.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_237.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_19.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_19.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_236.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_235.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_264.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_265.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_266.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_20.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_20.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_266.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_264.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_267.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_268.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_269.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_21.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_21.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_269.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_267.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_270.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_271.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_272.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_22.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_22.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_272.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_270.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_273.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_274.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_275.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_23.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_23.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_275.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_273.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_282.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_283.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_284.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_24.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_24.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_284.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_282.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_285.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_286.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_287.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_25.png'),
    tiles_per_row=32,
    reimport_image=os.path.join(images_path, 'subscreen_25.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_287.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_285.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_294.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_295.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_296.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_26.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_297.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_298.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_299.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_27.png'),
    tiles_per_row=32,
    tiles_per_column=14,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_300.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_301.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_302.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_28.png'),
    tiles_per_row=32,
    tiles_per_column=14,
    reimport_image=os.path.join(images_path, 'subscreen_28.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_302.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_300.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_303.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_304.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_305.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_29.png'),
    tiles_per_row=32,
    tiles_per_column=14,
)
dump_image(
    palette_path=os.path.join(subscreen_path, 'subscreen_317.bin'),
    tileset_path=os.path.join(subscreen_path, 'subscreen_318.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_319.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_30.png'),
    tiles_per_row=32,
)
dump_image(
    palette_path=os.path.join(subscreen_path, 'subscreen_325.bin'),
    tileset_path=os.path.join(subscreen_path, 'subscreen_326.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_327.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_31.png'),
    tiles_per_row=32,
)
dump_image(
    palette_path=os.path.join(subscreen_path, 'subscreen_333.bin'),
    tileset_path=os.path.join(subscreen_path, 'subscreen_334.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_335.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_32.png'),
    tiles_per_row=32,
)
dump_image(
    palette_path=os.path.join(subscreen_path, 'subscreen_339.bin'),
    tileset_path=os.path.join(subscreen_path, 'subscreen_340.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_341.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_33.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_353.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_354.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_356.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_34.png'),
    tiles_per_row=32,
)
dump_image(
    palette_path=os.path.join(subscreen_path, 'subscreen_358.bin'),
    tileset_path=os.path.join(subscreen_path, 'subscreen_359.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_360.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_35.png'),
    tiles_per_row=32 * 3,
)
dump_image(
    palette_path=os.path.join(subscreen_path, 'subscreen_361.bin'),
    tileset_path=os.path.join(subscreen_path, 'subscreen_362.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_363.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_36.png'),
    tiles_per_row=32 * 3,
)
dump_image(
    palette_path=os.path.join(subscreen_path, 'subscreen_364.bin'),
    tileset_path=os.path.join(subscreen_path, 'subscreen_365.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_366.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_37.png'),
    tiles_per_row=32 * 3,
)
dump_image_gba(
    tileset_path=os.path.join(subscreen_path, 'subscreen_261.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_262.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_263.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_38.png'),
    tiles_per_row=12,
    tiles_per_column=20,
    reimport_image=os.path.join(images_path, 'subscreen_38.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_263.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_261.bin'),
)
dump_image_gba(
    tileset_path=os.path.join(subscreen_path, 'subscreen_120.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_121.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_122.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_39.png'),
    tiles_per_row=11,
    tiles_per_column=19,
    reimport_image=os.path.join(images_path, 'subscreen_39.png'),
    reimport_tilemap=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_122.bin'),
    reimport_tileset=os.path.join(temp_path, 'workspace/unpacked_bins/subscreen.bin/subscreen_120.bin'),
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_346.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_347.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_350.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_40.png'),
    tiles_per_row=32,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_346.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_349.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_350.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_41.png'),
    tiles_per_row=27,
    tiles_per_column=4,
)
dump_image(
    tileset_path=os.path.join(subscreen_path, 'subscreen_346.bin'),
    tilemap_path=os.path.join(subscreen_path, 'subscreen_348.bin'),
    palette_path=os.path.join(subscreen_path, 'subscreen_350.bin'),
    dest_path=os.path.join(workspace_path, 'subscreen_42.png'),
    tiles_per_row=29,
    tiles_per_column=18,
)
