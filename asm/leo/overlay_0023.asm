.nds
.thumb
.open TEMP+"/overlay/overlay_0023.bin",readu32(TEMP+"/y9.bin", 23 * 0x20 + 0x4)

; 存放战斗卡说明文本的内存区域
; 因为翻译完成后大小已经超过原定的 0x17440
; 所以需要二次扩大
.org 0x021B3DA4
	.dw 95296 + 4096
.org 0x021B4668
	mov r1, 0x5
.org 0x021B466C
	lsl r1, 0xC

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

.org 0x021B519A ; 锁定文字缓存防止在不可见但使用中时被覆盖 普通战斗卡
	bl sub_21B514C_hook_lock
.org 0x021B5278
	bl sub_21B514C_21B514C_21B5290_hook_unlock
  
.org 0x021B52DA ; 锁定文字缓存防止在不可见但使用中时被覆盖 EX 战斗卡
	bl sub_21B5290_hook_lock
.org 0x021B544C
	bl sub_21B514C_21B514C_21B5290_hook_unlock

.org 0x021B54AE ; 锁定文字缓存防止在不可见但使用中时被覆盖 GA 战斗卡
	bl sub_21B5464_hook_lock
.org 0x021B544C
	bl sub_21B514C_21B514C_21B5290_hook_unlock

.close
