.nds
.thumb
.open TEMP+"/arm9.bin", 0x02000000

// .\tools\armips.exe .\asm\arm9.asm -strequ TEMP .\_workspace\pegasus

; 过场动画的逐字打印函数
; Function to print a string in the game's text window
OriginalPrintFontConditionStart equ 0x0201B158
OriginalPrintFontConditionEnd equ 0x0201B192

; 过场动画的逐字打印函数 的前面的一个判断
; Function to print a string in the game's text window
OriginalAdditionalConditionStart equ 0x0201B114
OriginalAdditionalConditionEnd equ 0x0201B130

; 某些小字体的常用打印函数
; Function containing the code to print a string in the game's text window
OriginalPrintAnotherFontConditionStart equ 0x02020060
OriginalPrintAnotherFontConditionEnd equ 0x0202007A

; 过场动画的瞬间打印的函数
; Function to print a string in the game's text window instantly
OriginalPrintInstantFontConditionStart equ 0x0201B254
OriginalPrintInstantFontConditionEnd equ 0x0201B2A2

; 分配可用代码空间
.org 0x020D4BBC + 0x20 * 2 // 字体间的空位，用来放代码 和缓存
	.region 0x20 * (0x1E3 - 8), 0x12
    .endregion
.org 0x020D87DC + 0x40 * 2 // 字体间的空位，用来放代码 和缓存
    .region 0x40 * (0x1E3 - 2), 0x34
    .endregion
.org 0x020E0FDC + 0x40 * 2// 字体间的空位，用来放代码 和缓存
	.region 0x40 * (0x1E3 - 8), 0x56
    .endregion
.org 0x020E981C + 0x80 * 2// 原主字体位置，现在拿来放代码 和缓存
	.region 0x80 * (0x1E3 - 8), 0x78
    .endregion

; 字符缓存位置
.org 0x020D09F0 + 1 // 12x12 字符的字符宽度数据，对应原本的 0 字符
FontWidthZero:
  .fill 0x1, 0xFF
.org 0x020D4BBC // 8x8 小字符的缓存位置，对应原本的 0 字符
Font8x8Zero:
    .fill 0x20, 0xFF
.org 0x020D87DC // 8x16 细字符的缓存位置，对应原本的 0 字符
Font8x16Zero:
    .fill 0x40, 0xFF
.org 0x020E0FDC // 8x16 粗字符的缓存位置，对应原本的 0 字符
Font8x16BoldZero:
    .fill 0x40, 0xFF
.org 0x020E981C // 12x12 字符的缓存位置，对应原本的 0 字符（实际占用了 16x16 的尺寸）
Font12x12Zero:
		; .fill 0x80, 0xFF
		.import "asm/common/cache_mark_16x16.bin"
.org 0x020F992C // 代码中的一段码表数据，可能用来处理文字输入了
FontEncodingZero:
    .dw 0x3f00

.include "asm/leo/nitro.asm"
.include "asm/common/scripts.asm"
.include "asm/common/text.asm"
.include "asm/common/debug.asm"
.include "asm/common/init.asm"
.include "asm/common/dx.asm"
.include "asm/common/text_cache.asm"
.include "asm/common/text_hooks.asm"
.include "asm/common/text_input.asm"
.include "asm/common/text_utils.asm"

.org 0x02009178
read_script_direct:

; 似乎开始显示显存字体时会被执行
; 可以用来重置我们自己的字体缓存
; Seems to be executed when displaying the video memory font
; Can be used to reset our own font cache
.org 0x0202F3F4
		push {r4-r6, lr}
		bl CopyFontHook

; 调试用
; 捕获尚未 Hook 的脚本位置
.org 0x02008E92
	bl Debug_GetScriptPos
	

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

.org 0x02012C1E
	bl Debug_LoadArchive

.org 0x02020094
	bl Debug_ScriptError

.org 0x02012B14
	bl Fake_FS_Init

.org 0x02009908
.area 0x0200991E-., 0x00
	push {lr}
	bl Script_RedirectScriptPositionHook
	pop {pc}
.endarea

; 
.org 0x0201FA5E
.area 0x0201FA76-. , 0x00
	mov r0, r5
	bl ReadScript_extended
	ldr r1, [r6]
	add r0, r1
	
	mov r1, 0x1
	strh r1, [r5, #0x28]
.endarea

; sub_201B99C
.org 0x0201B9C4
.area 0x0201B9EC-., 0x00
	mov r0, r5
	bl ReadScript_extended
	ldr r1, [r4]
	add r0, r1
	str r0, [r4]

	mov r0, 0x1
	strh r0, [r5, #0x28]

	mov r0, r5
	bl 0x0201E554
.endarea

; sub_201B864
.org 0x0201B88C
.area 0x0201B8B4-., 0x00
	mov r0, r5
	bl ReadScript_extended
	ldr r1, [r4]
	add r0, r1
	str r0, [r4]

	mov r0, 0x1
	strh r0, [r5, #0x28]

	mov r0, r5
	bl 0x0201E554
.endarea

; 获取脚本长度
.org 0x02009CE2
.area 0x02009CFA-. , 0x00
	mov r0, r2
	push {lr}
	bl Script_GetLength
	pop {pc}
.endarea

.org 0x0200A558
.area 0x0200A56A-. , 0x00
	bl Script_FontEncodeToScriptEncodeHookLoop
.endarea

; 和战斗卡脚本读取相关的函数
; 经检查发现还会用来打印输入文字文本
; sub_20202D8
.org 0x0202030C
.area 0x02020326-. , 0x00
	bl sub_20202D8_hook
	b 0x02020326
.endarea

.org 0x0201FAF8
.area 0x0201FB18-. , 0x00
	bl sub_201FAF8_hook
	b 0x0201FB18
.endarea

.org 0x0200917A
.area 0x02009182-. , 0x00
	bl ReadScriptToVramHook
.endarea

.org 0x02009A68
.area 0x02009A9C-., 0x00
	push {lr}
	bl GetFontGraphAddressHook
	pop {pc}
.endarea

.org 0x02010798
	push {lr}
	bl sub_2010798_hook
	pop {pc}

.org 0x020107D0
	push {lr}
	bl sub_20107D0_hook
	pop {pc}

.org 0x02009A2C
.area 0x02009A40-. , 0x00
	bl sub_2009A2C_hook
	b 0x02009A40
.endarea

.close
