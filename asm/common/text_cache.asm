; 字库缓存，用于减少文件系统的 IO 操作带来的卡顿延迟
; TODO: 另外三个字体的缓存

; Modify these number to adjust font cache size.
; Number can be not equal at all, but have to be larger than 1.
; The larger the number, the faster the game can display the same character.
; 修改这些数字可以调整字体缓存大小。
; 数字可以不完全相等，但必须大于 1。
; 将这些数字设置得更大，游戏就能更快地显示相同的字符。
Font0_CacheSize equ 128
Font1_CacheSize equ 128
Font2_CacheSize equ 128
Font3_CacheSize equ 128

.thumb

.autoregion
.align
CopyFontHook:
    push {lr}
    bl Font2_ResetVRAMCache
    mov r5, r2
    ldr r2, =0x212DBC0
    pop {pc}
.pool
.endautoregion

.autoregion
.align

; 从普通字库（8x8 8x16 8x16粗）中加载缓存
; 参数 r0：要加载的字符偏移编码
; 参数 r1：字库缓存数据结构的开头位置
; 之后字符会被载入到 0 字符位置
FontCommon_LoadCharacterFromCacheOrRead:
    push {r0-r7, lr}

    ; 先寻找有没有缓存这个字
    mov r2, 0 ; 计次变量
    ldr r3, [r1] ; 缓存大小

@@SearchLoop:
    ; 计算当前字形地址
    ldr r4, [r1, #0x4] ; 字形大小
    add r4, 0x4 ; 字形中字符编码所占用的大小
    mul r4, r2
    add r4, 5 * 4 ; 字符缓存中字形大小和块大小所占用的大小
    add r4, r1

    ; 读取该字形编码
    ldr r5, [r4]
    cmp r5, r0

    ; 此时 r2 存储的是字形在缓存中的位置
    beq @@Cached

    add r2, 1
    cmp r2, r3
    beq @@NoCached
    b @@SearchLoop
@@NoCached:
    ; 从文件中读取字形
    ; 此处循环选择需要丢弃的缓存字形
    ; 而之后的 r6 存储的是目标缓存位置
    ldr r4, [r1, #0x8]
    add r4, 1
    cmp r4, r3
    bne @@NoCached_StartRead
    mov r4, 0
@@NoCached_StartRead:
    ; 保存当前覆盖位置
    mov r2, r4
    str r4, [r1, #0x8]

    mov r4, r0 ; 文字编码
    mov r5, r1 ; 缓存指针

    ; 计算需要读取后保存的位置
    ldr r6, [r5, #0x4] ; 字形大小
    add r6, 0x4
    mul r6, r2
    add r6, r5
    add r6, 5 * 4

    str r4, [r6] ; 存储编码

    add r6, 0x4 ; 位移到字符数据位置

    ldr r0, [r5, #0xC] ; 字库文件结构变量

    ldr r1, [r5, #0x4] ; 字形大小
    mul r1, r4
    mov r2, 0

    blx FS_SeekFile

    cmp r0, 0
    beq @@CopyEmpty

    ldr r0, [r5, #0xC]
    mov r1, r6
    ldr r2, [r5, #0x4]

    blx FS_ReadFile
    
    ; 此时 r1 存储的是字形在缓存中的位置
    ; r6 存储的是字形的缓存指针
    sub r6, 0x4
    mov r0, r5
    mov r1, r6
    b @@MoveFont
@@Cached:
    mov r0, r1
    mov r1, r4
@@MoveFont:
    ; r0 应该是缓存指针
    ; r1 应该是字形位置
    ; 将字符数据从缓存中移动到相应的位置

    ; 移动字库
    add r1, 0x4
    ldr r4, [r0, #0x4] ; 字形大小
    ldr r0, [r0, #0x10]
    cmp r4, 0x20
    beq @@Copy20DoubleWorlds
    ; 0x40 (64) 个字节 或
    ; 0x20 (32) 个字节
    
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}

    ldmia r1!, {r2-r5}
    stmia r0!, {r2-r5}

    pop {r0-r7, pc}
@@Copy20DoubleWorlds:
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r3}
    stmia r0!, {r2-r3}

    pop {r0-r7, pc}
@@CopyEmpty:
    ; 当遇到任何失败状况时，跳转到此处以复制空字符
    ; 防止出现错误的字符被渲染
    ; r0 应该是缓存指针

    mov r0, r5

    ldr r2, [r0, #0x4] ; 字形大小
    ldr r0, [r0, #0x10] ; 字形复制到的位置
    cmp r2, 0x20
    beq @@CopyEmpty20DoubleWorlds
    ldr r2, =#0x11001100
    ldr r3, =#0x00110011
    ; 0x40 (64) 个字节 或
    ; 0x20 (32) 个字节
    
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    
    ldmia r1!, {r2-r5}
    stmia r0!, {r2-r5}

    pop {r0-r7, pc}
@@CopyEmpty20DoubleWorlds:
    ldr r2, =#0x11001100
    ldr r3, =#0x00110011
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r3}
    stmia r0!, {r2-r3}

    pop {r0-r7, pc}
    .pool
.endautoregion

.autoregion
.align

; 从 12x12 字库中加载缓存，因为需要加载字宽所以额外写了函数
; 参数 r0：要加载的字符偏移编码
; 参数 r1：字库缓存数据结构的开头位置
; 之后字符会被载入到 0 字符位置
Font3_LoadCharacterFromCacheOrRead:
    push {r0-r7, lr}

    ; 先寻找有没有缓存这个字
    mov r2, 0 ; 计次变量
    ldr r3, [r1] ; 缓存大小

@@SearchLoop:
    ; 计算当前字形地址
    ldr r4, [r1, #0x4] ; 字形大小
    add r4, 8 ; 字形中字符编码和其字宽所占用的大小
    mul r4, r2
    add r4, 7 * 4 ; 字符缓存中字形大小和块大小所占用的大小
    add r4, r1

    ; 读取该字形编码
    ldr r5, [r4]
    cmp r5, r0

    ; 此时 r2 存储的是字形在缓存中的位置
    beq @@Cached

    add r2, 1
    cmp r2, r3
    beq @@NoCached
    b @@SearchLoop
@@NoCached:
    ; 从文件中读取字形
    ; 此处循环选择需要丢弃的缓存字形
    ; 而之后的 r6 存储的是目标缓存位置
    ldr r4, [r1, #0x8]
    add r4, 1
    cmp r4, r3
    bne @@NoCached_StartRead
    mov r4, 0
@@NoCached_StartRead:
    ; 保存当前覆盖位置
    mov r2, r4
    str r4, [r1, #0x8]

    mov r4, r0
    mov r5, r1

    ; 计算需要读取后保存的位置
    ldr r6, [r5, #0x4] ; 字形大小
    add r6, 0x8
    mul r6, r2
    add r6, r5
    add r6, 7 * 4

    str r4, [r6] ; 存储编码
    add r6, 0x8 - 1 ; 位移到存储字宽的位置

    ldr r0, [r5, #0x10] ; 字符宽度文件
    mov r1, r4
    mov r2, 0
    blx FS_SeekFile

    cmp r0, 0
    beq @@CopyEmpty

    ldr r0, [r5, #0x10] ; 字符宽度文件
    mov r1, r6
    mov r2, 0x1
    blx FS_ReadFile

    add r6, 0x1 ; 位移到字符数据位置

    ldr r0, [r5, #0xC]

    ldr r1, [r5, #0x4]
    mul r1, r4
    mov r2, 0

    blx FS_SeekFile

    cmp r0, 0
    beq @@CopyEmpty

    ldr r0, [r5, #0xC]
    mov r1, r6
    ldr r2, [r5, #0x4]

    blx FS_ReadFile
    
    ; 此时 r1 存储的是字形在缓存中的位置
    ; r6 存储的是字形的缓存指针
    sub r6, 0x8
    mov r0, r5
    mov r1, r6
    b @@MoveFont
@@Cached:
    mov r0, r1
    mov r1, r4
@@MoveFont:
    ; r0 应该是缓存指针
    ; r1 应该是字形位置
    ; 将字符数据从缓存中移动到相应的位置

    ; 移动字宽
    ldrb r2, [r1, #0x7]
    ldr r3, [r0, #0x18]
    strb r2, [r3]
    ; 移动字库
    add r1, 0x8
    ldr r0, [r0, #0x14]
    ; 0x80 (128) 个字节
    ; 只要简单重复五遍就行，然后再补上两个

    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}

    ldmia r1!, {r2-r3}
    stmia r0!, {r2-r3}

    pop {r0-r7, pc}
    .pool
@@CopyEmpty:
    ; 当遇到任何失败状况时，跳转到此处以复制空字符
    ; 防止出现错误的字符被渲染
    ; r0 应该是缓存指针

    mov r0, r5

    ; 空字宽
    mov r2, 0xC ; 12 像素
    ldr r3, [r0, #0x18]
    strb r2, [r3]

    ldr r2, =#0x11001100
    ldr r3, =#0x00110011
    mov r4, r2
    mov r5, r3
    mov r6, r2
    mov r7, r3

    ldr r0, [r0, #0x14]

    stmia r0!, {r2-r7}
    stmia r0!, {r2-r7}
    stmia r0!, {r2-r7}
    stmia r0!, {r2-r7}
    stmia r0!, {r2-r7}

    stmia r0!, {r2-r3}

    pop {r0-r7, pc}
    .pool
.endautoregion

.autoregion
.align
; 加载粗字体并写入显存（缓存）
; 用于战斗卡的显示
; 参数：
;   r0 需要加载的字符，字库编码
; 返回值：
;   r0 字符对应的显存 Map Id，加一之后可获得字模的下半部分 Map Id
Font2_LoadCharacterToVRAM:
    push {r1-r7, lr}
    ; 查询缓存是否已有字形
    ldr r1, =@Font2VramCache
    mov r2, 0x3 ; 计次
    mov r5, 0
@@CacheSearchLoop:
    ldrh r4, [r1]
    cmp r4, r0
    beq @@CacheFound
    add r1, 0x2
    add r2, 0x2
    add r5, 1
    cmp r5, 128
    bhs @@NotFound
    b @@CacheSearchLoop
@@CacheFound:
    mov r0, r2
    pop {r1-r7, pc}
@@NotFound:
    ldr r1, =FontCache_Font_CacheArea_00000002
    bl FontCommon_LoadCharacterFromCacheOrRead
    
    ; 0x06214020
    mov r2, r0 ; 把字库编码移到 r2
    ldr r0, =@Font2VramCachePointer
    ldr r0, [r0]
    ldr r1, =@Font2VramCache
    add r1, r0
    strh r2, [r1]
    mov r1, 0x40
    lsr r0, 0x1
    mul r0, r1
    ldr r1, =0x06214000 + (0x20 * 3)
    add r0, r1
    
    ; 复制字模
    ldr r1, =Font8x16BoldZero
    
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}
    ldmia r1!, {r2-r7}
    stmia r0!, {r2-r7}

    ldmia r1!, {r2-r5}
    stmia r0!, {r2-r5}
    
    ; 更新缓存指针
    ldr r0, =@Font2VramCachePointer
    ldr r0, [r0]
    mov r1, r0
    add r0, 0x2
    cmp r0, 0xFF
    bcc @@End
    mov r0, 0
@@End:
    ldr r2, =@Font2VramCachePointer
    str r0, [r2]
    mov r0, r1
    add r0, 0x3
    pop {r1-r7, pc}
    .pool
.endautoregion
.autoregion
.align
@Font2VramCachePointer:
    .dw 0
.endautoregion
.autoregion
.align
@Font2VramCache:
    .fill 0xFF, 128 * 2 ; 128 个字的缓存
.endautoregion

.autoregion
.align
Font2_ResetVRAMCache:
    push {r0-r7, lr}
    ldr r0, =@Font2VramCachePointer
    mov r1, 0
    ldr r2, =0x104
    blx MI_CpuFill8
    pop {r0-r7, pc}
.pool
.endautoregion


.macro FontCache, graphSize, cacheSize, fontFileVar, fontDest
    .autoregion
    ; 缓存区域定义宏
    .align ; 使用 stmia 和 ldmia 指令时，要确保读写的地址是 4 的倍数，否则会有一点点小问题出现
    Font_CacheArea:
        .dw cacheSize ; 缓存大小
        .dw graphSize ; #0x4 字形大小
        .dw cacheSize - 1 ; #0x8 当前的缓存指针位置，减一是为了让第一个缓存位置更新成 0
        .dw fontFileVar ; #0xC 字库文件结构变量
        .dw fontDest ; #0x10 字形复制到的位置
        .fill ((4 + graphSize) * cacheSize), 0xFF
    .endautoregion
.endmacro

FontCache 0x20, Font0_CacheSize, Font0FileVar, Font8x8Zero ; FontCache_Font_CacheArea_00000000
FontCache 0x40, Font1_CacheSize, Font1FileVar, Font8x16Zero ; FontCache_Font_CacheArea_00000001
FontCache 0x40, Font2_CacheSize, Font2FileVar, Font8x16BoldZero ; FontCache_Font_CacheArea_00000002

.autoregion
.align
Font3_CacheArea:
    .dw Font3_CacheSize ; 缓存大小
    .dw 0x80 ; #0x4 字形大小
    .dw Font3_CacheSize - 1 ; #0x8 当前覆盖位置
    .dw Font3FileVar ; #0xC 字库文件
    .dw Font3WidthFileVar ; #0x10 字形宽度文件
    .dw Font12x12Zero ; #0x14 原 0 字库位置
    .dw FontWidthZero ; #0x18 原 0 字符宽度位置
    .fill ((4 + 4 + 0x80) * Font3_CacheSize), 0xFF ; 使用 0xFF 来填充，否则在缓存尚未填满的时候会对空格字体造成误判（会被识别成字宽为 0 的字形）
.endautoregion