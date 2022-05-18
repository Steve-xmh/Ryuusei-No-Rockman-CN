.nds
.thumb
.open TEMP+"/overlay/overlay_0002.bin",readu32(TEMP+"/y9.bin", 2 * 0x20 + 0x4)

; 扩大战洛克武器说明脚本的内存区域大小到 8KB （原 6KB）
; 内存大小必须大于 mess_1220.msg 的大小，否则会溢出花屏
.org 0x02189BBC
	.dw 20104 + 2048 ; 原总大小 + 调整大小
.org 0x0218986E
	mov r1, 0x8 ; 脚本内存的大小除以 1024

.org 0x0218A018
	.dw Script_0D5520
.org 0x0215BCE4
	.dw Script_0D5BA4

.org 0x0217FE92 ; 始终打印右侧文本
	mov r0, 1

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
.org 0x02176B6E
.area 0x02176B94-., 0x00
	bl sub_2176B60_hook
	b 0x02176B94
.endarea


.org 0x02176BE2
.area 0x02176BEE-., 0x00
	bl sub_2176BA4_hook
	b 0x02176BEE
.endarea


// Walk through NPCs
// 穿过 NPC
.org 0x02174408
field_canWalk:
.org 0x02174280
field_isInNPC:
.org 0x02173A8E
	bl	field_walkThroughNPC
.org 0x02173A16
	bl	field_walkThroughNPCStop
	
.close
