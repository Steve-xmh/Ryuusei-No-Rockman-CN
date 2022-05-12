.nds
.thumb
.open TEMP+"/arm9.dec", 0x02000000

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
	.region 0x40 * (0x1E3 - 8), 0x34
    .endregion
.org 0x020D87DC + 0x40 * 2 // 字体间的空位，用来放代码 和缓存
    .region 0x40 * (0x1E3 - 2)
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

.close
