.thumb

; 阻塞当前程序，直到等待 A 按钮按下
.autoregion
.align
.func Input_WaitForButtonA
    push {r0-r7, lr}
    ldr r7,=0x4000130
@@CheckLoop:
    swi 0x05
    ldr r2, [r7]
    mov r0, 1
    and r0, r2
    cmp r0, 0
    bne @@CheckLoop
    pop {r0-r7, pc}
.endfunc
.pool
.endautoregion
