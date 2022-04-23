.nds
.thumb
.open TEMP+"/overlay/overlay_0002.bin",readu32(TEMP+"/y9.bin", 2 * 0x20 + 0x4)

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
