; 调试相关的代码，用于拦截函数调用，确认hook是否生效

.autoregion
.align
Debug_GetScriptPos:
	push {r1-r2, lr}
	; 检查调用者是否还在使用原脚本
	; 天马版的脚本位置
	ldr r1, =#0x020D0BD0
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D25CC
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D30A4
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D3C6C
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D0EC8
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D1520
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D1BA4
	cmp r0, r1
	beq @@Unhooked
	; 青龙/雄狮版的脚本位置
	ldr r1, =#0x020D0BD4
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D25D0
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D30A8
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D3C70
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D0ECC
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D1524
	cmp r0, r1
	beq @@Unhooked
	ldr r1, =#0x020D1BA8
	cmp r0, r1
	beq @@Unhooked
	b @@End
@@Unhooked:
	ldr r1, [sp, #0x4 * 8]
	.msg "WARN: Unhooked embed script 0x%r0%"
	.msg "Caller: 0x%r1%"
@@End:
	mov r4, r0
	ldr r0, =0x0212DBB0
	pop {r1-r2, pc}
.pool
.endautoregion

.autoregion
.align
Debug_LoadArchive:
	sub sp, sp, #0x8
	mov r6, r2
	push {r0-r7, lr}
	
	lsr r0, r2, #0x10
	cmp r0, #0x4
	beq @@IsLoadingMessBin
	ldr r0, [sp, #0x8 + 0x4*12]
	.msg "Loading archive 0x%r2% to 0x%r1%, caller 0x%r0%"
	b @@End
@@IsLoadingMessBin:
	lsl r2, #0x10
	lsr r2, #0x10
	ldr r0, [sp, #0x8 + 0x4*12]
	.msg "Loading script 0x%r2% to 0x%r1%, caller 0x%r0%"
	ldr r3, =95
	cmp r2, r3
	beq @@Break
	ldr r3, =13
	cmp r2, r3
	beq @@Break
	b @@End
@@Break:
	; mov r11, r11
@@End:
	pop {r0-r7, pc}
.pool
.endautoregion

.autoregion
.align
Debug_ScriptError:
	cmp r1, r0
	bls @@Return
	.msg "Script Error!"
	.msg "Script overflowed with %r1% bytes"
	.msg "Allocated %r0% bytes"
	.msg "Script Context address: 0x%r5%"
	b .
@@Return:
	blx lr
.endautoregion

.autoregion
.align
Debug_PrintScriptContext:
	push {r0-r7, lr}
	ldr r1, [r0, #0x10]
	ldrb r2, [r1]
	ldrb r3, [r1, #1]
	.msg "ScriptCTX: 0x%r0% 0x%r1% 0x%r2% 0x%r3%"
	pop {r0-r7, pc}
.endautoregion
