.nds
.thumb
.open TEMP+"/overlay/overlay_0023.bin",readu32(TEMP+"/y9.bin", 23 * 0x20 + 0x4)

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
