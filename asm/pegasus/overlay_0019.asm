.nds
.open TEMP+"/overlay/overlay_0019.bin",readu32(TEMP+"/y9.bin", 19 * 0x20 + 0x4)
.thumb

; BOSS 记录的脚本
.org 0x021B4A20
  .dw Script_0D7C6C

.close