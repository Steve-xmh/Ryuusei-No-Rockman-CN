# Ryuusei-No-Rockman Chinese Font-Expand Hack Project

[简体中文](./README-CN.md)

A modification of Ryuusei No Rockman 1 with font characters expansion.
Similar to [Mega-Man-Star-Force-DX](https://github.com/Prof9/Mega-Man-Star-Force-DX).

Currently in heavy development and there is no promise when to finish this (As I'm a beginner for hacking this).

## Some words

This hack replaced the original text rendering logic. So the hard-coded fonts data in arm9 is free and can be used in any purpose.

And for me, I want to share my hacking experience to everyone who wants to translate your favourite game into your language. So I open-sourced this, with almost all code full of comments (Both in Chinese and English).

If this project is full finished, it will be used in Chinese translation project for Chinese players.

## Setup Development

### Tools

First of all, you need to copy ROM files into `_rom` folder. See `_rom/roms_go_here.txt` for details.

- Mega Man Star Force: Pegasus - Japan version (流星のロックマン - ペガサス)
- Mega Man Star Force: Leo - Japan version (流星のロックマン - レオ)
- Mega Man Star Force: Dragon - Japan version (流星のロックマン - ドラゴン)

You must have at least one of them, or you will only get the built ROM(s) of version of what you places.

Second, you need to prepare some tools and place them in `_tools` folder:

- Nightly Version of (ARMIPS)[https://github.com/Kingcom/armips] by Kingcom, you can get it on [here](https://buildbot.orphis.net/armips/)
- ndstool from devkitPro
- PixelPet by Prof. 9
- TextPet by Prof. 9
- [SFArcTool-rs by myself](https://github.com/Steve-xmh/sfarctool) ([Prof.9's version](https://github.com/Prof9/SFArcTool) may work too?)
- Python 3.x (Just install it to your computer.)

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

### Generate Fonts

In order to keep font files small, fonts are not pre-generated. You can generate them by yourself.

After modified scripts, you must run `python3 genfont.py` to generate fonts and table which will cover all the characters you used.

### Build ROM(s)

Check you have run `python3 genfont.py` before. Then run `python3 build.py`.

Then you can check your built ROM(s) in `_build` folder.

## Credits

- [Prof. 9](https://github.com/Prof9) - Tools and MMSF-DX project for reference.
- [Kingcom](https://github.com/Kingcom) - For his ARMIPS tool.
- [SteveXMH](https://github.com/Steve-xmh) - Main programming and hacking.
- Enler - Who teaches me how to hack this.
- Everyone who are supporting me!

## Other

Any contribution/PR is welcomed! If you have any questions, feel free to open an issue!

And if you need my hack resources (.ida files and some notes, **ALL in Chinese comments**), you can contact me on Discord (SteveXMH#3394) or (Twitter)[https://twitter.com/SteveXmh].
