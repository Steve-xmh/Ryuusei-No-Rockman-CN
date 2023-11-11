; 用于给游戏写入第一屏的工具库

.thumb

; 等待一帧
.autoregion
.align
.func Video_VSync
    push {r0-r7, lr}
    swi 0x05
    pop {r0-r7, pc}
.endfunc
.pool
.endautoregion

; 从白色淡入效果
.autoregion
.align
.func Video_FadeIn
    push {r0-r7, lr}
    
    mov r0, 1
    lsl r0, 14
    
    ldr r4,=0x0400006C
    ldr r5,=0x0400106C
    
    mov r1, 16
    
@@FadeLoop:
    mov r3, r0
    orr r3, r1
    
    str r3, [r4]
    str r3, [r5]
    
    sub r1, 1
    bl Video_VSync
    cmp r1, 0
    bgt @@FadeLoop
    
    pop {r0-r7, pc}
.endfunc
.pool
.endautoregion

; 到白色淡出效果
.autoregion
.align
.func Video_FadeOut
    push {r0-r7, lr}
    
    mov r0, 1
    lsl r0, 14
    
    ldr r4,=0x0400006C
    ldr r5,=0x0400106C
    
    mov r1, 0
    
@@FadeLoop:
    mov r3, r0
    orr r3, r1
    
    str r3, [r4]
    str r3, [r5]
    
    add r1, 1
    bl Video_VSync
    cmp r1, 16
    ble @@FadeLoop
    
    pop {r0-r7, pc}
.endfunc
.pool
.endautoregion


; 打印预制好的图片
.autoregion
.align
.func SplashScreen_PrintInfo
    push {r0-r7, lr}
    sub sp, 0x3C ; 存放文件指针
    
    mov r5, sp
    mov r0, r5
    blx FS_InitFile
    
    ; ############ 初始化背景 ############
    
    ; 打开 VRAM 空间
    
    ldr r0,=0b10000001
    ldr r1,=0x4000240 ; 上屏
    strb r0, [r1]
    ldr r0,=0b10000100
    ldr r1,=0x4000242 ; 下屏
    strb r0, [r1]
    
    ; ############ 加载调色板 ############
    
    mov r0, r5
    ldr r1, =@SplashScreen_PAL_Path
    blx FS_OpenFile
    
    cmp r0, 1
    beq @@LoadPAL
    .msg "Failed to open splash_screen.pal.bin"
    b .
@@LoadPAL:
    mov r0, r5
    ldr r1, =0x5000000
    ldr r2, =0xFF * 2
    blx FS_ReadFile
    
    mov r0, r5
    mov r1, 0
    mov r2, 0
    blx FS_SeekFile
    
    mov r0, r5
    ldr r1, =0x5000400
    ldr r2, =0xFF * 2
    blx FS_ReadFile
    
    mov r0, r5
    blx FS_CloseFile
    
    ; ############ 加载上屏图块集 ############
    
    mov r0, r5
    ldr r1, =@SplashScreen_TST_Top_Path
    blx FS_OpenFile
    
    cmp r0, 1
    beq @@LoadTopTST
    .msg "Failed to open splash_screen.tst.t.bin"
    b .
@@LoadTopTST:
    mov r0, r5
    ldr r1, =0x6004000
    ldr r2, =98304
    blx FS_ReadFile
    
    mov r0, r5
    blx FS_CloseFile
    
    ; ############ 加载上屏图块表 ############
    
    mov r0, r5
    ldr r1, =@SplashScreen_TMP_Top_Path
    blx FS_OpenFile
    
    cmp r0, 1
    beq @@LoadTopTMP
    .msg "Failed to open splash_screen.tmp.t.bin"
    b .
@@LoadTopTMP:
    mov r0, r5
    ldr r1, =0x6000000
    ldr r2, =1536
    blx FS_ReadFile
    
    mov r0, r5
    blx FS_CloseFile
    
    ; ############ 加载下屏图块集 ############
    
    mov r0, r5
    ldr r1, =@SplashScreen_TST_Bottom_Path
    blx FS_OpenFile
    
    cmp r0, 1
    beq @@LoadBottomTST
    .msg "Failed to open splash_screen.tst.b.bin"
    b .
@@LoadBottomTST:
    mov r0, r5
    ldr r1, =0x6204000
    ldr r2, =98304
    blx FS_ReadFile
    
    mov r0, r5
    blx FS_CloseFile
    
    ; ############ 加载下屏图块表 ############
    
    mov r0, r5
    ldr r1, =@SplashScreen_TMP_Bottom_Path
    blx FS_OpenFile
    
    cmp r0, 1
    beq @@LoadBottomTMP
    .msg "Failed to open splash_screen.tmp.b.bin"
    b .
@@LoadBottomTMP:
    mov r0, r5
    ldr r1, =0x6200000
    ldr r2, =1536
    blx FS_ReadFile
    
    mov r0, r5
    blx FS_CloseFile
    
    ; ############ 完成绘制 ############
    
    ; 启用 BG0 显示
    ; 0 0 000 000 0 0 00 00 01 000000010 0 0 0 0 000
    ldr r0,=0b00000000000000010000000100000000
    ldr r1,=0x4000000
    str r0, [r1]
    ldr r1,=0x4001000
    str r0, [r1]
    ; 切换 BG0 模式
    ldr r0,=(1 << 7) | (1 << 2)
    ldr r1,=0x4000008
    str r0, [r1]
    ldr r1,=0x4001008
    str r0, [r1]
    
    
    ldr r0,=60
@@WaitSec:
    sub r0, 1
    cmp r0, 0
    bgt @@WaitSec
    
    add sp, 0x3C
    pop {r0-r7, pc}
.endfunc
.pool
.align
@SplashScreen_PAL_Path:
.asciiz "/splash_screen.pal.bin"
.align
@SplashScreen_TST_Top_Path:
.asciiz "/splash_screen.tst.t.bin"
.align
@SplashScreen_TMP_Top_Path:
.asciiz "/splash_screen.tmp.t.bin"
.align
@SplashScreen_TST_Bottom_Path:
.asciiz "/splash_screen.tst.b.bin"
.align
@SplashScreen_TMP_Bottom_Path:
.asciiz "/splash_screen.tmp.b.bin"
.endautoregion
