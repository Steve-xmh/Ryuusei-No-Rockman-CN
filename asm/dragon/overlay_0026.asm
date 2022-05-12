.nds
.open TEMP+"/overlay/overlay_0026.bin",readu32(TEMP+"/y9.bin", 26 * 0x20 + 0x4)
.thumb

; 商店中的物品脚本
.org 0x021B83D8
  .dw Script_0D65CC
  .dw Script_0D4BD0

.close
