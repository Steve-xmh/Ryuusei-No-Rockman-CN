.nds
.thumb
.open TEMP+"/overlay/overlay_0006.bin",readu32(TEMP+"/y9.bin", 6 * 0x20 + 0x4)

; sub_2195D70 战斗时 Custom 页面的卡名打印 overlay9_0006
.org 0x02195E98
  .dw Script_0D65CC
.org 0x02195E9C
  .dw Script_0D4BD0
; sub_21998F4 战斗时使用带动画的卡片前显示在上屏的文字
.org 0x02199B6C
  .dw Script_0D65CC
.org 0x02199B70
  .dw Script_0D4BD0
; sub_219B114 战斗结束时奖励战斗卡的脚本
.org 0x0219B230
  .dw Script_0D65CC
.org 0x0219B234
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
.org 0x02198244
  .dw Script_0D65CC
.org 0x02198248
  .dw Script_0D4BD0

.close
