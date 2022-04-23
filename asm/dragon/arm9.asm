.nds
.thumb
.open TEMP+"/arm9.dec", 0x02000000

// .\tools\armips.exe .\asm\arm9.asm -strequ TEMP .\_workspace\pegasus

; 分配可用代码空间
.org 0x020D4BBC + 0x20 // 字体间的空位，用来放代码 和缓存
.region 0x20 * (0x1D0 - 2)
.endregion
.org 0x020D87DC + 0x40 // 字体间的空位，用来放代码 和缓存
.region 0x40 * (0x1D0 - 2)
.endregion
.org 0x020E0FDC + 0x40 // 字体间的空位，用来放代码 和缓存
.region 0x40 * (0x1D0 - 2)
.endregion
.org 0x020E981C + 0x80 // 原主字体位置，现在拿来放代码 和缓存
.region 0x80 * (0x1D0 - 2)
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
    .fill 0x80, 0xFF
.org 0x020F992C // 代码中的一段码表数据，可能用来处理文字输入了
FontEncodingZero:
    .dw 0x3f00

.include "asm/dragon/nitro.asm"
.include "asm/common/scripts.asm"
.include "asm/dragon/text_hooks.asm"
.include "asm/common/text_utils.asm"
.include "asm/common/text_cache.asm"
.include "asm/common/text.asm"

.close
