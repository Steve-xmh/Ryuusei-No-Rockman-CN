.nds
.thumb
.open TEMP+"/overlay/overlay_0006.bin",readu32(TEMP+"/y9.bin", 6 * 0x20 + 0x4)

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
