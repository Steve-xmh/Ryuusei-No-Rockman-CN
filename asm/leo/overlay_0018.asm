.nds
.open TEMP+"/overlay/overlay_0018.bin",readu32(TEMP+"/y9.bin", 18 * 0x20 + 0x4)
.thumb

; 菜单物品页面的脚本
.org 0x021B5574
  .dw Script_0D5520

.close