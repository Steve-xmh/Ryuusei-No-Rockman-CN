.nds
.thumb
.open TEMP+"/overlay/overlay_0002.bin",readu32(TEMP+"/y9.bin", 2 * 0x20 + 0x4)

.org 0x0217FBA4
	.dw Script_0D490C
.org 0x021788F8
	.dw Script_0D490C

; 扩大邮件页面相关的脚本存放内存区域
.org 0x021835E4
	.dw 0xB720 + 4096
.org 0x021833DE;
	mov r1, 0x6
.org 0x02183440
	mov r1, 0x6
	lsl r1, 0xC

; 扩大战洛克武器说明脚本的内存区域大小到 8KB （原 6KB）
; 内存大小必须大于 mess_1220.msg 的大小，否则会溢出花屏
.org 0x02189BB8
	.dw 20104 + 2048 ; 原总大小 + 调整大小
.org 0x0218986A
	mov r1, 0x8 ; 脚本内存的大小除以 1024

; sub_2177C10
; 在加载自定义战斗卡时分配内存
.org 0x02177D04
	.dw 0x1D750 + 0x4000 + 0x4000
.org 0x02178200
	lsl r1, 0xF
.org 0x0217820C
	lsl r1, 0xF

.org 0x0218A014
	.dw Script_0D5520
.org 0x0215BCE0
	.dw Script_0D5BA4

; sub_217AD00
; 在文件夹页面的显示卡片攻击值的的函数
.org 0x0217ADA4
.area 0x0217ADBC-., 0x00
	bl Script_CustomWriteCardDamageHook
.endarea

.org 0x0217AE36
.area 0x0217AE46-., 0x00
	bl Script_CustomWriteCardMarkHook
.endarea

; sub_2176B60
; 疑似解码输入内容的函数
; 0x02108F8C
; 0x021C5D28
; 0x02113E58
; 0x0211433E
.org 0x02176B6A
.area 0x02176B90-., 0x00
	bl sub_2176B60_hook
	b 0x02176B90
.endarea


.org 0x02176BDE
.area 0x02176BEA-., 0x00
	bl sub_2176BA4_hook
	b 0x02176BEA
.endarea

// Walk through NPCs
// 穿过 NPC
.org 0x02174404
field_canWalk:
.org 0x0217427C
field_isInNPC:
.org 0x02173A8A
	bl	field_walkThroughNPC
.org 0x02173A12
	bl	field_walkThroughNPCStop
	
.close
