# Ryuusei-No-Rockman Chinese Font-Expand Hack Project

[Chinese 简体中文](./README-CN.md)

A modification of Ryuusei No Rockman 1 with font characters expansion.
Similar to [Mega-Man-Star-Force-DX](https://github.com/Prof9/Mega-Man-Star-Force-DX).
But it mainly focus on Chinese translation hacking.

The code may VERY messy since this is my very first hacking project.
And for the opinion of the translation team, the Chinese translation (scripts or images) will not be included in the source code.
(Except the scripts that embed inside the arm9 code.)

## Features

- Expanded fonts that can support thousands of Chinese chatacters (Or other language if needed).
- Merged some patches from [Mega-Man-Star-Force-DX](https://github.com/Prof9/Mega-Man-Star-Force-DX)
- By the method of the hacking, the original cheats should work as well.

## Setup Development

### Tools

First of all, you need to copy ROM files into `_rom` folder. See `_rom/roms_go_here.txt` for details.

- Mega Man Star Force: Pegasus - Japan version (流星のロックマン - ペガサス)
- Mega Man Star Force: Leo - Japan version (流星のロックマン - レオ)
- Mega Man Star Force: Dragon - Japan version (流星のロックマン - ドラゴン)

You must have at ALL of them, or you will only get the built ROM(s) of version of what you places.

Second, you need to prepare some tools and place them in `_tools` folder:

- Nightly Version of (ARMIPS)[https://github.com/Kingcom/armips] by Kingcom, you can get it on [here](https://buildbot.orphis.net/armips/)
- ndstool from devkitPro
- PixelPet by Prof. 9
- TextPet by Prof. 9
- [SFArcTool-rs by myself](https://github.com/Steve-xmh/sfarctool) ([Prof.9's version](https://github.com/Prof9/SFArcTool) may work too?)
- Python 3.x (Just install it to your computer.)
- Pillow for Python (Install it by `pip3 install pillow`)

If you need to modify sprite files, you can also check [BNSpriteEditor](https://github.com/brianuuu/BNSpriteEditor) or my work-in-progress [SFSpriteEditor Web](https://github.com/Steve-xmh/SFSpriteEditor-web).

### Setup workspace

Now everything is ready, you can run `python3 setup.py` to unpack the rom(s) and setup the workspace.

After execution, you will see a directory named `_workspace` under the current directory which contains all the files we unpacked.

For script translation purposes, check `_workspace/mess_out_tpl` to see game scripts.

### Adjust font cache size

For someone who want to make your own code patch, you may need to reduce the font cache size for more free space to place your patch code.

Open `asm/common/font_cache.asm` and find those lines:

```asm
Font0_CacheSize equ 128
Font1_CacheSize equ 128
Font2_CacheSize equ 128
Font3_CacheSize equ 128
```

Read the comment above them and change them to any number you want.

### Start translation

Create a `tpl` directory at the root directory, and copy the scripts from `_workspace/mess_out_tpl` to `tpl` directory.
Then you can edit the script and start translation.

#### Modify default player name

To change the default player name, you can check `./asm/{VERSION_TYPE}/arm9.asm` and look for the line:
```asm
; sub_200BF94 是玩家名字的默认值被写入的函数
;    0x020F8E9C 是姓氏
;    0x020F8EA2 是名字

// 姓氏 First Name
.org 0x020F8E9C
	// No need to modify as `星河` already the correct name.

// 名字 Last Name
.org 0x020F8EA2
	.dh 0x1D3
	.dh 0x1E5 ; 0xE6 + 0xFF ; End of the text
```

Modify it to what you want, but need to follow that the character code should not larger than `0x1E3` and remenber add `.dh 0x1E5` at the end of the text.

### Generate Fonts

In order to keep font files small, fonts are not pre-generated. You can generate them by yourself.

After modified scripts, you must run `python3 genfont.py` to generate fonts and table which will cover all the characters you used.

The default font is `SimSun` (Or `宋体` in Chinese), which has most of the Chinese characters in 12x12 size. If you need other type of chatacters that the default font doesn't contain, you can modify `./scripts/font.py` and change `default_font_path` to your own font file path.

### Build ROM(s)

Check you have run `python3 genfont.py` before. Then run `python3 build.py`.

Then you can check your built ROM(s) in `_build` folder.

## Credits

- [Prof. 9](https://github.com/Prof9) - Tools and MMSF-DX project for reference.
- [Kingcom](https://github.com/Kingcom) - For his ARMIPS tool.
- [SteveXMH](https://github.com/Steve-xmh) - Main programming and hacking.
- [diaowinner](https://github.com/diaowinner) - 8x12 MuZai font support.
- Enler - Who teaches me how to hack this.
- Everyone who are supporting me!

## Some words

This hack replaced the original text rendering logic. So the hard-coded fonts data in arm9 is free and can be used in any purpose.

And for me, I want to share my hacking experience to everyone who wants to translate your favourite game into your language. So I open-sourced this with almost all code full of comments.

## Other

Any contribution/PR is welcomed! If you have any questions, feel free to open an issue!
