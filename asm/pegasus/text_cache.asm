.thumb

; 似乎复制显存字体时会用到
.org 0x0202F3F0
    push {r4-r6, lr}
    bl CopyFontHook

.include "asm/common/text_cache.asm"
