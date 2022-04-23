.thumb

; 测量脚本长度的钩子
OriginalScriptGetLengthLoopStart equ 0x02009CE2
OriginalScriptGetLengthLoopEnd equ 0x02009CF8

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
; sub_2176B60 尚未探明
; sub_2176BA4 尚未探明
; sub_20202D8 疑似和显存字库有关
; sub_215BB8C 和地名显示有关
; sub_2009908 和读取内嵌脚本有关
; sub_2195D70 战斗时 Custom 页面的卡名打印 overlay9_0006
; sub_201FAC8 鸣谢画面时调用的文字打印函数

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

.include "asm/common/text_utils.asm"
