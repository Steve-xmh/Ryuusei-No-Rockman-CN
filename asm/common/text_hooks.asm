; 在定义好相关符号时引入此代码以拦截默认字库打印请求
; 并替换成自己的字库渲染函数

.thumb

// 0x0201B08A
// 0x0201B060

/*
	插入位置对应代码：
	if ( ctx->word52 == 0xE4 )
	ctx->word52 += ctx->current_script_data[1];
*/

/*
	插入位置对应代码：
	if ( ctx->current_script_code == 0xE4 )
	{
		ctx->dword34 = v3 | 0x2000;
		ctx->current_script_code += ctx->current_script_data[1];
		COM_LoadFontGraph(ctx); // 0x0201E554
		v4 = ctx->current_script_data + 2;
	}
	else
	{
		ctx->dword34 = v3 | 0x2000;
		COM_LoadFontGraph(ctx);
		v4 = ctx->current_script_data + 1;
	}
*/


.if OriginalPrintFontConditionStart != 0
	.org OriginalPrintFontConditionStart // 判断 0xE4 开始的那个位置
	.area OriginalPrintFontConditionEnd-. , 0x00
	@@OriginalPrintFontConditionStart:
		push {r0-r7}

		// r1 = a1->dword34;
		ldr r1, [r5, #0x34]
		
		// a1->dword34 = r1 | 0x2000;
		ldr r0, =0x2000
		orr r0, r1
		str r0, [r5, #0x34]

		push {r5}
		mov r0, r5
		bl ReadScript_extended
		mov r7, r0

		pop {r5}
		mov r0, r5
		mov r1, 0x1
		strh r1, [r5, #0x28]

		push {r5}
		// 调用绘制
		bl 0x0201E554

		pop {r5}
		ldr r0, [r5, #0x10]
		add r0, r7
		str r0, [r5, #0x10] // a1->current_script_pointer = v4;

		pop {r0-r7}
		.pool
	.endarea
.else
	.warning "OriginalPrintFontConditionStart is 0! Will ignore this patch!"
.endif


.if OriginalPrintInstantFontConditionStart != 0
	.org OriginalPrintInstantFontConditionStart
	.area OriginalPrintInstantFontConditionEnd-. , 0x00
		bl @OriginalPrintInstantFontConditionHook
	.endarea
.else
	.warning "OriginalPrintInstantFontConditionStart is 0! Will ignore this patch!"
.endif


.if OriginalPrintAnotherFontConditionStart != 0
	.org OriginalPrintAnotherFontConditionStart
	.area OriginalPrintAnotherFontConditionEnd-. , 0x00
		bl @OriginalPrintAnotherFontConditionHook
	.endarea
.else
	.warning "OriginalPrintAnotherFontConditionStart is 0! Will ignore this patch!"
.endif

.autoregion
.align

@OriginalPrintAnotherFontConditionHook:
	push {r1-r7, lr}

	mov r0, r5
	bl ReadScript_extended
	
	mov r1, 0x1
	strh r1, [r5, #0x28]

	// v6 = *v2 + ReadScript_extended(a1);
	mov r1, r0
	ldr r0, [r6]
	add r0, r1
	str r0, [r6]

	pop {r1-r7, pc}

.endautoregion

.autoregion
.align
@OriginalPrintInstantFontConditionHook:
	push {r0-r7, lr}

	ldr r1, [r6]
	ldr r0,=#0x2000
	orr r0, r1
	str r0, [r6]

	mov r0, r5
	bl ReadScript_extended
	mov r6, r0

	mov r0, 0x1
	strh r0, [r5, #0x28]

	// 调用绘制
	mov r0, r5
	bl 0x0201E554

	ldrh r0, [r7]
	add r0, #1
	strh r0, [r7]

	ldr r1, [r5, #0x10]
	add r1, r6
	str r1, [r5, #0x10]

	pop {r0-r7, pc}
	.pool
.endautoregion

.autoregion
.align
GetFontGraphAddressHook:
  push {lr}
@@Font12x12:
  cmp r1, 0
  bne @@Font8x16Bold
  ldr r1, =Font3_CacheArea
  bl Font3_LoadCharacterFromCacheOrRead
  ldr r0, =Font12x12Zero
  pop {pc}
@@Font8x16Bold:
  cmp r1, 1
  bne @@Font8x16
  ldr r1, =FontCache_Font_CacheArea_00000002
  bl FontCommon_LoadCharacterFromCacheOrRead
  ldr r0, =Font8x16BoldZero
  pop {pc}
@@Font8x16:
  cmp r1, 2
  bne @@Font8x8
  ldr r1, =FontCache_Font_CacheArea_00000001
  bl FontCommon_LoadCharacterFromCacheOrRead
  ldr r0, =Font8x16Zero
  pop {pc}
@@Font8x8:
  cmp r1, 3
  bne @@UnknownFontId
  ldr r1, =FontCache_Font_CacheArea_00000000
  bl FontCommon_LoadCharacterFromCacheOrRead
  ldr r0, =Font8x8Zero
  pop {pc}
@@UnknownFontId:
  mov r0, 0
  pop {pc}
.pool
.endautoregion
