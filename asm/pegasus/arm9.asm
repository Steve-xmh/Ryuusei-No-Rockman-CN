.nds
.thumb
.open TEMP+"/arm9.bin", 0x02000000

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
.org 0x020D4B98 + 0x20 * 2 // 字体间的空位，用来放代码 和缓存
  .region 0x20 * (0x1E3 - 8), 0x12
  .endregion
.org 0x020D8798 + 0x40 * 2 // 字体间的空位，用来放代码 和缓存
  .region 0x40 * (0x1E3 - 8), 0x34
  .endregion
.org 0x020E0F98 + 0x40 * 2 // 字体间的空位，用来放代码 和缓存
  .region 0x40 * (0x1E3 - 8), 0x56
  .endregion
.org 0x020E9798 + 0x80 * 8 // 原主字体位置，现在拿来放代码 和缓存
  .region 0x80 * (0x1E3 - 8), 0x78
  .endregion

; 字符缓存位置
.org 0x020D09EC + 1 // 12x12 字符的字符宽度数据，对应原本的 0 字符
FontWidthZero:
  .fill 0x1, 0x21
.org 0x020D4B98 + 0x20 // 8x8 小字符的缓存位置，对应原本的 0 字符
Font8x8Zero:
    .fill 0x20, 0x43
.org 0x020D8798 + 0x40 // 8x16 细字符的缓存位置，对应原本的 0 字符
Font8x16Zero:
    .fill 0x40, 0x65
.org 0x020E0F98 + 0x40 // 8x16 粗字符的缓存位置，对应原本的 0 字符
Font8x16BoldZero:
    .fill 0x40, 0x87
.org 0x020E9798 + 0x80 // 12x12 字符的缓存位置，对应原本的 0 字符（实际占用了 16x16 的尺寸）
Font12x12Zero:
    ; .fill 0x80, 0xFF
    .import "asm/common/cache_mark_16x16.bin"
.org 0x020F9928 // 代码中的一段码表数据，可能用来处理文字输入了
FontEncodingZero:
    .dw 0x3f00

.include "asm/pegasus/nitro.asm"
.include "asm/common/scripts.asm"
.include "asm/common/text.asm"
.include "asm/common/dx.asm"
.include "asm/common/text_cache.asm"
.include "asm/common/text_hooks.asm"
.include "asm/common/text_input.asm"
.include "asm/common/text_utils.asm"

; 似乎开始显示显存字体时会被执行
; 可以用来重置我们自己的字体缓存
; Seems to be executed when displaying the video memory font
; Can be used to reset our own font cache
.org 0x0202F3F0
    push {r4-r6, lr}
    bl CopyFontHook

; sub_200BF94 是玩家名字的默认值被写入的函数
;     0x20F8E98 是姓氏
;     0x20F8E9E 是名字

.org 0x20F8E9E
  .dh 0x1D3
  .dh 0x1E5 ; 0xE6 + 0xFF

; 逆向出来的函数们（和 0xE4 相关的东西）
; sub_200A830 疑似是检测当前脚本位置是否还有控制指令
; sub_2009CCC 是测量脚本长度的函数
; sub_20099E4 疑似是拷贝脚本内容的函数
; sub_200A538 是从字库编码到脚本编码的转换
; sub_201C3B8 疑似是解析脚本然后复制小字体的子模的函数
; sub_201B0BC 梦　开　始　的　地　方（大雾） —— 打印剧情文本的函数
; sub_201B864 打印水平两个按钮文字的函数
; sub_201B99C 疑似是打印剧情文本的函数？
; sub_201FA30 疑似是脚本解析的函数
; sub_20107D0 疑似是从字库编码到脚本编码的转换
; sub_2009AAC 疑似是拷贝脚本内容的函数（且进行了目标位置大小限制）
; sub_2010798 疑似是将脚本编码转换成 ASCII 编码（可能？）的函数
; sub_2176B60 将输入文字编码转换回脚本编码的函数
; sub_2176BA4 是输入文字时转换输入内容到字体编码的函数，并返回是否为空
; sub_20202D8 疑似和显存字库有关
; sub_215BB8C 和地名显示有关
; sub_2009908 和读取内嵌脚本有关
; sub_2195D70 战斗时 Custom 页面的卡名打印 overlay9_0006
; sub_201FAC8 鸣谢画面时调用的文字打印函数
; sub_202002C 也是打印小字体和大字体的函数

.autoregion
.align
; 拦截正常的文件系统初始化函数
; 在这里初始化我们需要的东西
Fake_FS_Init:
  push {lr}
  blx FS_Init
  .msg "Ryuusei No Rockman 1 CN Patch by SteveXMH!"
  .msg "Special thanks to:"
  .msg "  - Enler"
  .msg "  - Prof. 9"
  pop {pc}
.endautoregion

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

.close