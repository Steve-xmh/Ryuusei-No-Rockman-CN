.thumb
; 测量脚本长度，转换脚本到字库编码等操作

; 计算脚本位置函数 (sub_2009908) 的钩子
.autoregion
.align
Script_RedirectScriptPositionHook:
  push {lr}
  bl Script_RedirectScriptPosition
  lsl r1, r1, #0x11
  lsr r3, r1, #0x10
  add r1, r3, #1
  ldrb r1, [r0, r1]
  lsl r2, r1, #8
  ldrb r1, [r0, r3]
  orr r1, r2
  lsl r1, r1, #0x10
  lsr r1, r1, #0x10
  add r0, r0, r1
  pop {pc}
.endautoregion

; 将输入的内嵌脚本位置转换成我们的版本
; 参数
; r0 = 输入的内嵌脚本位置
; 返回值
; r0 = 转换后的内嵌脚本位置
.autoregion
.align
Script_RedirectScriptPosition:
  push {r1, lr}
  ; .msg "Redirecting script for %r0%"
  ; 天马版的脚本位置
  ldr r1, =#0x020D0BD0
  cmp r0, r1
  beq @@Script_0D4BD0
  ldr r1, =#0x020D25CC
  cmp r0, r1
  beq @@Script_0D65CC
  ldr r1, =#0x020D30A4
  cmp r0, r1
  beq @@Script_0D70A4
  ldr r1, =#0x020D3C6C
  cmp r0, r1
  beq @@Script_0D7C6C
  ldr r1, =#0x020D0EC8
  cmp r0, r1
  beq @@Script_0D4EC8
  ldr r1, =#0x020D1520
  cmp r0, r1
  beq @@Script_0D5520
  ldr r1, =#0x020D090C
  cmp r0, r1
  beq @@Script_0D490C
  ldr r1, =#0x020D1BA4
  cmp r0, r1
  beq @@Script_0D5BA4
  ; 青龙/雄狮版的脚本位置
  ldr r1, =#0x020D0BD4
  cmp r0, r1
  beq @@Script_0D4BD0
  ldr r1, =#0x020D25D0
  cmp r0, r1
  beq @@Script_0D65CC
  ldr r1, =#0x020D30A8
  cmp r0, r1
  beq @@Script_0D70A4
  ldr r1, =#0x020D3C70
  cmp r0, r1
  beq @@Script_0D7C6C
  ldr r1, =#0x020D0ECC
  cmp r0, r1
  beq @@Script_0D4EC8
  ldr r1, =#0x020D1524
  cmp r0, r1
  beq @@Script_0D5520
  ldr r1, =#0x020D0910
  cmp r0, r1
  beq @@Script_0D490C
  ldr r1, =#0x020D1BA8
  cmp r0, r1
  beq @@Script_0D5BA4
; 已经在使用新的脚本了
  ldr r1, =Script_0D4BD0
  cmp r0, r1
  beq @@End
  ldr r1, =Script_0D65CC
  cmp r0, r1
  beq @@End
  ldr r1, =Script_0D70A4
  cmp r0, r1
  beq @@End
  ldr r1, =Script_0D7C6C
  cmp r0, r1
  beq @@End
  ldr r1, =Script_0D4EC8
  cmp r0, r1
  beq @@End
  ldr r1, =Script_0D5BA4
  cmp r0, r1
  beq @@End
  ldr r1, =Script_0D5520
  cmp r0, r1
  beq @@End
@@CantRedirect:
  .msg "WARNING: Can't redirect script position for %r0%"
  b @@End
@@Script_0D4BD0:
  ldr r0, =Script_0D4BD0
  b @@End
@@Script_0D65CC:
  ldr r0, =Script_0D65CC
  b @@End
@@Script_0D70A4:
  ldr r0, =Script_0D70A4
  b @@End
@@Script_0D7C6C:
  ldr r0, =Script_0D7C6C
  b @@End
@@Script_0D4EC8:
  ldr r0, =Script_0D4EC8
  b @@End
@@Script_0D5BA4:
  ldr r0, =Script_0D5BA4
  b @@End
@@Script_0D490C:
  ldr r0, =Script_0D490C
  b @@End
@@Script_0D5520:
  ldr r0, =Script_0D5520
@@End:
  pop {r1, pc}
.pool
.endautoregion

.autoregion
.align
Script_WriteSelectedCardNameHook:
  push {lr}
  add r0, #0x60
  asr r7, r0, #0x6 ; 原先是 #0x5

  push {r0}
  mov r0, r7
  bl Font2_LoadCharacterToVRAM
  mov r7, r0
  pop {r0}

  pop {pc}

.endautoregion

.autoregion
.align
Script_WriteCardIdHook:
  push {lr}
  add r1, #0x1
  push {r0}
  mov r0, r1
  bl Font2_LoadCharacterToVRAM
  mov r2, r0
  pop {r0}
  pop {pc}

.endautoregion

.autoregion
.align
Script_CustomMenuWriteCardDamageHook:
  push {lr}
  ; R5 存储的原始数字字符编码
  ; R6 + R7 / R2 + R7 是目标位置
  asr r5, 1
  push {r0}
  mov r0, r5
  bl Font2_LoadCharacterToVRAM
  mov r5, r0
  pop {r0}
  lsl r7, r3, 1
  strh r5, [r2, r7]
  add r5, 1
  mov r4, 1
  strh r5, [r6, r7]
  pop {pc}
.endautoregion

.autoregion
.align
Script_CustomWriteCardDamageHook:
  push {lr}
  ; R7 存储的原始数字字符编码
  ; R0 是目标位置
  push {r0}
  mov r0, r7
  asr r0, 1
  bl Font2_LoadCharacterToVRAM
  mov r7, r0
  pop {r0}
  mov r1, r3
  lsl r0, r5, 1
  orr r1, r7
  mov r12, r0
  strh r1, [r4, r0]
  add r0, r7, 1
  mov r7, r3
  orr r7, r0
  ldr r0, [sp, #0x10 + 0x4]
  mov r1, r12
  mov r6, 1
  strh r7, [r0, r1]
  pop {pc}
.endautoregion

.autoregion
.align
Script_CustomWriteCardMarkHook:
  push {lr}
  ; R6 存储的原始数字字符编码
  ; R0 是目标位置
  push {r0}
  mov r0, r6
  asr r0, 1
  bl Font2_LoadCharacterToVRAM
  mov r6, r0
  pop {r0}
  add r1, r5, r7
  add r1, 0x40
  strh r6, [r1]
  add r1, r5, r7
  add r6, r6, 1
  add r1, 0x58
  mov r4, 1
  strh r6, [r1]
  pop {pc}
.endautoregion

; 将输入的脚本编码转换成字库编码
; 参数：
;   r0 = 输入的脚本指针
; 返回值:
;   r0 = 输出的字库编码
;   r1 = 输入的文字长度
.autoregion
.align
Script_ScriptEncodeToFontEncode:
    push {r2-r7, lr}
    ldrb r3, [r0]
    cmp r3, #0xD0
    bcc @@NotInExtendEncode
    cmp r3, #0xE4
    bhi @@NotInExtendEncode
    mov r5, 0x1
    mov r1, 0x2
    cmp r3, #0xE4
    beq @@InOriginalExtendEncode
@@InExtendEncode:
    sub r3, #0xD0
    mov r2, #0xE4
    mul r3, r2
    add r3, #0xD0
    ldrb r4, [r0, #0x1]
    add r3, r4
    b @@End
@@InOriginalExtendEncode:
    ldrb r4, [r0, #0x1]
    add r3, r4
    b @@End
@@NotInExtendEncode:
    mov r1, 0x1
@@End:
    mov r0, r3
    pop {r2-r7, pc}
.pool
.endautoregion

.autoregion
.align
; 将输入的字库编码转换成脚本编码
; 如果字库编码范围在 0xE4 - 0x1E3 之间，则转换成 0xE4 + 字库编码（确保兼容）
; 如果字库编码范围在 0xD0 - 0xE3, 0x1E3 或者更大，则转换成 0xD0 + 字库编码
; r7 = 字库编码
; r0 = 脚本指针
Script_FontEncodeToScriptEncodeHookLoop:
  push {r1-r7, lr}
  ; .msg "SFETSEHL r0 = %r0% r7 = %r7%"
  ldr r2, =0x1E3
  cmp r7, r2
  bcs @@InExtendedEncode
  cmp r7, #0xE4
  bcs @@InOriginalExtendedEncode
  cmp r7, #0xD0
  bcs @@InExtendedEncode
  ; 0-0xE3
  strb r7, [r0]
  add r0, 1
  b @@End
@@InExtendedEncode:
  sub r7, 0xD0
  mov r2, 0xD0
  mov r3, r2
@@Loop:
  cmp r7, 0xE4
  bcc @@Finished
  add r2, 0x1
  sub r7, 0xE4
  b @@Loop
@@Finished:
  strb r2, [r0]
  strb r7, [r0, #0x1]
  add r0, 2
  b @@End
@@InOriginalExtendedEncode:
  mov r2, 0xE4
  strb r2, [r0]
  sub r7, 0xE4
  strb r7, [r0, #0x1]
  add r0, 2
@@End:
  pop {r1-r7, pc}
.pool
.endautoregion

.autoregion
.align
; 测量脚本长度
; 参数
; r0 = 当前脚本位置
; 返回值
; r0 = 脚本长度
Script_GetLength:
  push {r1-r7,lr}
  mov r1, #0x0
@@LoopStart:
  ldrb r2, [r0]
  cmp r2, #0xE6
  beq @@LoopEnd
  cmp r2, 0xD0
  blt @@NotExtendEncode
  cmp r2, 0xE4
  bgt @@NotExtendEncode
@@ExtendEncode:
  add r0, r0, #2
  add r1, r1, #1
  b @@LoopStart
@@NotExtendEncode:
  add r0, r0, #1
  add r1, r1, #1
  b @@LoopStart
@@LoopEnd:
  mov r0, r1
  pop {r1-r7,pc}
.endautoregion

.autoregion
.align
; r5 = 脚本上下文
; r6 = 脚本位置
sub_20202D8_hook:
  push {r0-r7,lr}
  mov r0, r5
  add r0, 0x30
  ldrb r0, [r0]
  cmp r0, #0x0
  bne @@Size8x16
@@Size16x16:
  ldr r0, [r5, #0x10] // 当前脚本指针位置
  bl Script_ScriptEncodeToFontEncode
  strh r0, [r5, #0x28]
  ldr r0, [r6]
  add r0, r1
  str r0, [r6]
  pop {r0-r7,pc}
@@Size8x16:
  ldr r0, [r5, #0x10] // 当前脚本指针位置
  bl Script_ScriptEncodeToFontEncode
  bl Font2_LoadCharacterToVRAM
  sub r0, 0x1
  lsr r0, 0x1
  strh r0, [r5, #0x28]
  ldr r0, [r6]
  add r0, r1
  str r0, [r6]
  pop {r0-r7,pc}
.pool
.endautoregion

.autoregion
.align
sub_201FAF8_hook:
  push {r0-r7,lr}
  mov r0, r5
  bl ReadScript_extended
  mov r4, r0
  ldr r0, [r5, #0x10] // 当前脚本指针位置
  add r0, r4
  str r0, [r5, #0x10]
  mov r0, 1
  strh r0, [r5, #0x28]
  mov r0, r5
  bl 0x0201E554
  pop {r0-r7,pc}
.pool
.endautoregion

.autoregion
.align
sub_2176BA4_hook:
  push {r3-r5,lr}
  mov r3, r0
  mov r4, r1
  
  mov r0, r2
  ; .msg "Script2Font %r0%"
  bl Script_ScriptEncodeToFontEncode
  ; .msg "Script2FontR ScriptPointer %r2% -> FontEncode %r0% Length %r1%"
  strh r0, [r4]
  add r2, r1
  cmp r0, 0
  beq @@End
  
  mov r6, 1
@@End:
  
  mov r1, r4
  mov r0, r3
  add r1, 0x2
  pop {r3-r5,pc}
.pool
.endautoregion

.autoregion
.align
; 用于将脚本编码转换为 ASCII 编码的函数
; r0 = 未知
; r1 = 脚本位置
; r2 = 目标写入位置
; r3 = 最大写入长度
; 返回值
; r0 = 转码的文字数量
sub_2010798_hook:
  push {r1-r7,lr}
  mov r7, 0
  mov r4, r1
@@Loop:
  ldrb r6, [r4]
  cmp r6, 0xE6
  beq @@End
  cmp r3, 0
  beq @@End
  
  mov r0, r4
  bl Script_ScriptEncodeToFontEncode
  cmp r0, 0xE4
  bcs @@InExtendedEncode
  ldr r6, =0x02106A98
  b @@LoopEnd
@@InExtendedEncode:
  sub r0, 0xE4
  ldr r6, =0x02106B7C
@@LoopEnd:
  ldrb r0, [r6, r0]
  strb r0, [r2]
  add r4, r1
  add r7, 1
  add r2, 1
  sub r3, 1
  b @@Loop
@@End:
  mov r0, r7
  pop {r1-r7, pc}
.pool
.endautoregion

.autoregion
.align
; 将字库编码转换成脚本编码
; 参数
; r1 = 字库编码
; r2 = 写入脚本位置
; 返回值
; r0 = 已写入的字节数量
sub_20107D0_hook:
  push {r3-r7,lr}
  ldr r0, =0x02106C6C
  lsl r1, 1
  ldrh r1, [r0, r1]
  mov r0, 2
  cmp r1, 0xE4
  bcs @@InOriginalEncode
  cmp r1, 0xD0
  bcs @@InExtendedEncode
  strb r1, [r2]
  mov r0, 1
  b @@End
@@InOriginalEncode:
  mov r3, 0xE4
  strb r3, [r2]
  sub r1, 0xE4
  strb r1, [r2, #1]
  b @@End
@@InExtendedEncode:
  mov r3, 0xD0
  strb r3, [r2]
  sub r1, 0xD0
  strb r1, [r2, #1]
@@End:
  pop {r3-r7,lr}
.pool
.endautoregion

.autoregion
.align
ReadScriptToVramHook:
  push {lr}
; 天马版
	ldr r5, =0x020D25CC
	cmp r0, r5
	beq @@Script_20D25CC
	ldr r5, =0x020D0BD0
	cmp r0, r5
	beq @@Script_20D0BD0
; 青龙版
	ldr r5, =0x020D25D0
	cmp r0, r5
	beq @@Script_20D25CC
	ldr r5, =0x020D0BD4
	cmp r0, r5
	beq @@Script_20D0BD0
  .msg "ERROR: Unmodified script %r0%"
	b .
@@Script_20D25CC: ; 普通战斗卡脚本 20D25CC
	ldr r0, =Script_0D65CC
	b @@End
@@Script_20D0BD0: ; 我们的太阳联动脚本 20D0BD0
	ldr r0, =Script_0D4BD0
@@End:
	mov r5, r0
	mov r6, r1
	mov r7, r2
	mov r4, r3
  pop {pc}
.pool
.endautoregion

.autoregion
.align
sub_2009A2C_hook:
  push {r2-r7, lr}
  mov r2, r0 ; src
  mov r3, r1 ; dest
  
  bl Script_ScriptEncodeToFontEncode
@@CopyLoop:
  cmp r1, 0
  beq @@End
  ldrb r0, [r2]
  strb r0, [r3]
  add r2, 1
  add r3, 1
  sub r1, 1
  b @@CopyLoop
@@End:
  mov r0, r2
  mov r1, r3
  pop {r2-r7, pc}
.pool
.endautoregion

.autoregion
.align
sub_21B514C_hook_lock:
  mov r0, 0
  str r0, [sp, #0x8]
  push {r0-r7, lr}
  mov r0, 1
  bl FontCache_UnlockGraphs
  bl FontCache_Lock
  pop {r0-r7, pc}
.pool
.endautoregion

.autoregion
.align
sub_21B5464_hook_lock:
  ldrsh r0, [r4, r0]
  add r0, r2
  push {r0-r7, lr}
  cmp r1, r0
  beq @@SkipLock
  mov r0, 3
  bl FontCache_UnlockGraphs
  bl FontCache_Lock
@@SkipLock:
  pop {r0-r7, pc}
.pool
.endautoregion

.autoregion
.align
sub_21B5290_hook_lock:
  ldrsh r0, [r4, r0]
  add r0, r2
  push {r0-r7, lr}
  cmp r1, r0
  beq @@SkipLock
  mov r0, 2
  bl FontCache_UnlockGraphs
  bl FontCache_Lock
@@SkipLock:
  pop {r0-r7, pc}
.pool
.endautoregion

.autoregion
.align
sub_21B514C_21B514C_21B5290_hook_unlock:
  ldr r0, [r0]
  mov r1, 1
  push {r0, lr}
  mov r0, 0
  bl FontCache_Lock
  pop {r0, pc}
.pool
.endautoregion
