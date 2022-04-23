.nds
.thumb
.open TEMP+"/arm9.bin", 0x02000000

; 分配可用代码空间
.org 0x020D4B98 + 0x20 * 2 // 字体间的空位，用来放代码 和缓存
  .region 0x20 * (0x1E3 - 2), 0x12
  .endregion
.org 0x020D8798 + 0x40 * 2 // 字体间的空位，用来放代码 和缓存
  .region 0x40 * (0x1E3 - 2), 0x34
  .endregion
.org 0x020E0F98 + 0x40 * 2 // 字体间的空位，用来放代码 和缓存
  .region 0x40 * (0x1E3 - 2), 0x56
  .endregion
.org 0x020E9798 + 0x80 * 8 // 原主字体位置，现在拿来放代码 和缓存
  .region 0x80 * (0x100 - 2), 0x78
  .endregion

; 字符缓存位置
.org 0x020D09EC + 1 // 12x12 字符的字符宽度数据，对应原本的 0 字符
FontWidthZero:
  .fill 0x1, 0xFF
.org 0x020D4B98 + 0x20 // 8x8 小字符的缓存位置，对应原本的 0 字符
Font8x8Zero:
    .fill 0x20, 0xFF
.org 0x020D8798 + 0x40 // 8x16 细字符的缓存位置，对应原本的 0 字符
Font8x16Zero:
    .fill 0x40, 0xFF
.org 0x020E0F98 + 0x40 // 8x16 粗字符的缓存位置，对应原本的 0 字符
Font8x16BoldZero:
    .fill 0x40, 0xFF
.org 0x020E9798 + 0x80 // 12x12 字符的缓存位置，对应原本的 0 字符（实际占用了 16x16 的尺寸）
Font12x12Zero:
    ; .fill 0x80, 0xFF
    .import "asm/common/cache_mark_16x16.bin"
.org 0x020F9928 // 代码中的一段码表数据，可能用来处理文字输入了
FontEncodingZero:
    .dw 0x3f00


// .\tools\armips.exe .\asm\pegasus\arm9.asm -strequ TEMP .\_temp\workspace\pegasus

.include "asm/pegasus/nitro.asm"
.include "asm/pegasus/text_hooks.asm"
.include "asm/pegasus/text_utils.asm"
.include "asm/pegasus/text_cache.asm"
.include "asm/common/text.asm"
.include "asm/common/text_input.asm"
.include "asm/common/scripts.asm"

.org 0x0200917A
.area 0x02009182-. , 0x00
  bl @ReadScriptToVramHook
.endarea

.org 0x02009A68
.area 0x02009A9C-., 0x00
  push {lr}
  bl GetFontGraphAddressHook
  pop {pc}
.endarea

.autoregion
.align
@ReadScriptToVramHook:
  ldr r5, =0x020D25CC
  cmp r0, r5
  beq @@Script_20D25CC
  ldr r5, =0x020D0BD0
  cmp r0, r5
  beq @@Script_20D0BD0
@@NotModifiedScript:
  b @@NotModifiedScript
@@Script_20D25CC: ; 普通战斗卡脚本 20D25CC
  ldr r0, =Script_0D65CC
  b @@End
@@Script_20D0BD0: ; 我们的太阳联动脚本 20D0BD0
  ldr r0, =Script_0D4BD0
@@End:
  mov r5, r0
  mov r6, r1
  mov r7, r2
  mov r4, r3
  blx lr
.pool
.endautoregion

/*
.autoregion
.align
TransformInputToTableHook:
  push {r1-r7, lr}
  // r1 要保存的位置
  // r4 输入上下文
  // r7 原输入编码

  mov r0, r4
  // mov r1, r1
  bl TransformInputToTable_extended
  add r1, r0
  mov r0, r1

  pop {r1-r7, pc}
.endautoregion
*/

.close

.open TEMP+"/overlay/overlay_0023.bin",readu32(TEMP+"/y9.bin", 23 * 0x20 + 0x4)
.thumb

; 写入纯数字显存字体相关的函数
.org 0x021B56EC
.area 0x021B56F4-. , 0x00
  bl Script_WriteCardIdHook
.endarea

; 显示当前已选中卡片的名字的函数
.org 0x021B57B8
.area 0x021B57BC-., 0x00
  bl Script_WriteSelectedCardNameHook
.endarea

.close

.open TEMP+"/overlay/overlay_0002.bin",readu32(TEMP+"/y9.bin", 2 * 0x20 + 0x4)
.thumb

.org 0x0215BCE4
  .dw Script_0D5BA4

; sub_217AD00
; 在文件夹页面的显示卡片攻击值的的函数
.org 0x0217ADA8
.area 0x0217ADC0-., 0x00
  bl Script_CustomWriteCardDamageHook
.endarea

.org 0x0217AE3A
.area 0x0217AE4A-., 0x00
  bl Script_CustomWriteCardMarkHook
.endarea

; sub_2176B60
; 疑似解码输入内容的函数
; 0x02108F8C
; 0x021C5D28
; 0x02113E58
; 0x0211433E
; .org 0x02176B6E
; .area 0x02176B94-., 0x00
;   bl sub_2176B60_hook
;   b 0x02176B94
; .pool
; .endarea

.close


.open TEMP+"/overlay/overlay_0006.bin",readu32(TEMP+"/y9.bin", 6 * 0x20 + 0x4)
.thumb

; sub_2195D70 战斗时 Custom 页面的卡名打印 overlay9_0006
.org 0x02195E98
  .dw Script_0D65CC
.org 0x02195E9C
  .dw Script_0D4BD0
; sub_2198254 战斗时上屏的候选卡名
.org 0x02198370
  .dw Script_0D65CC
.org 0x02198374
  .dw Script_0D4BD0
; sub_2198498 上屏右上角的病毒名称
.org 0x02198604
  .dw Script_0D70A4
.org 0x02198608
  .dw Script_0D7C6C

.close

.open TEMP+"/overlay/overlay_0016.bin",readu32(TEMP+"/y9.bin", 16 * 0x20 + 0x4)
.thumb

.org 0x021B4D16
.area 0x021B4D20-., 0x00
  bl Script_CustomMenuWriteCardDamageHook
.endarea

.close

.open TEMP+"/overlay/overlay_0018.bin",readu32(TEMP+"/y9.bin", 18 * 0x20 + 0x4)
.thumb

.org 0x021B5574
  .dw Script_0D5520

.close

.open TEMP+"/overlay/overlay_0026.bin",readu32(TEMP+"/y9.bin", 26 * 0x20 + 0x4)
.thumb
.org 0x021B83D8
  .dw Script_0D65CC
  .dw Script_0D4BD0

.close
