.org 0x02016240 + 2 * 4
    bl Arena_Init_Ext_Hook
.org 0x020162F6
.area 0x4
    bl Arena_Init_Post_Hook
.endarea
.org 0x02016304 + 2 * 3
    bl Arena_Init_Hook
.org 0x02016396
.area 0x4
    bl Arena_Init_Post_Hook
.endarea

.autoregion
.align
Arena_Init_Ext_Hook:
    push {r0-r4, lr}
    
	ldr r4, [sp, #0x4 * 9]
    .msg ""
    .msg "## Init Arena 0x%r0% for size 0x%r1% (ext)"
    .msg "    Caller: 0x%r4%"
    
    lsl r6, r6, 0x3
    str r5, [r5]
    
    pop {r0-r4, pc}
.pool
.endautoregion

.autoregion
.align
Arena_Init_Ext_Post_Hook:
    ldr r0, [r5, 0x18]
    ; 这里不再回到原先的位置，直接回到原调用函数的位置
    .msg "    Start Pos: 0x%r0%"
    .msg "    Return: 0x%r5%"
    .msg ""
    mov r0, r5
    pop {r4-r6, pc}
.pool
.endautoregion

.autoregion
.align
Arena_Init_Hook:
    push {r0-r3, lr}
    
	ldr r3, [sp, #0x4 * 5]
    .msg ""
    .msg "## Init Arena 0x%r0% for size 0x%r1%"
    .msg "    Caller: 0x%r3%"
    
    str r5, [r5]
    mov r4, r1
    
    pop {r0-r3, pc}
.pool
.endautoregion

.autoregion
.align
Arena_Init_Post_Hook:
    ldr r0, [r5, 0x18]
    ; 这里不再回到原先的位置，直接回到原调用函数的位置
    .msg "    Start Pos: 0x%r0%"
    .msg "    Return: 0x%r5%"
    .msg ""
    mov r0, r5
    pop {r4-r6, pc}
.pool
.endautoregion


.org 0x020163D4 + 2 * 1
    bl Arena_Alloc_Hook
.autoregion
.align
Arena_Alloc_Hook:
    push {lr}
    
    push {r0-r7}
    
    .msg "Alloc arena 0x%r0% id 0x%r2% size 0x%r1%"
	ldr r7, [sp, #0x4 * 10]
    .msg "  Caller: 0x%r7%"
    ldr r1, [r0, 0x4]
    .msg "  Alloc Ptr: 0x%r1%"
    
    pop {r0-r7}
    
    mov r3, 3
    mov r4, r1
    
    pop {pc}
.pool
.endautoregion


.org 0x020163C8
    bl Arena_Free_Hook
.autoregion
.align
Arena_Free_Hook:
    push {r0-r7, lr}
    
    bl 0x2015C1C
    
	ldr r7, [sp, #0x4 * 10]
    
    .msg "Freed arena 0x%r4%"
    .msg "  Caller: 0x%r7%"
    
    pop {r0-r7, pc}
.pool
.endautoregion

