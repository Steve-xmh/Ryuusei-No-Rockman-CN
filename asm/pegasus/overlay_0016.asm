.nds
.open TEMP+"/overlay/overlay_0016.bin",readu32(TEMP+"/y9.bin", 16 * 0x20 + 0x4)
.thumb

.org 0x021B4D16
.area 0x021B4D20-., 0x00
  bl Script_CustomMenuWriteCardDamageHook
.endarea

.close
