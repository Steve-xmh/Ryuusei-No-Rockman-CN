.thumb

// 天马版的代码所需插入位置，我们要在这里捕获脚本数据
// TODO: 测出其他版本的插入位置，否则其他版本会出大问题

// 过场动画的逐字打印函数
@OriginalPrintFontConditionStart equ 0x0201B158
@OriginalPrintFontConditionEnd equ 0x0201B192

// 过场动画的逐字打印函数 的前面的一个判断
@OriginalAdditionalConditionStart equ 0x0201B114
@OriginalAdditionalConditionEnd equ 0x0201B130

// 某些小字体的常用打印函数
@OriginalPrintAnotherFontConditionStart equ 0x02020060
@OriginalPrintAnotherFontConditionEnd equ 0x0202007A

// 过场动画的瞬间打印的函数
@OriginalPrintInstantFontConditionStart equ 0x0201B254
@OriginalPrintInstantFontConditionEnd equ 0x0201B2A2

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

.org @OriginalPrintFontConditionStart // 判断 0xE4 开始的那个位置
.area @OriginalPrintFontConditionEnd-. , 0x00
@@OriginalPrintFontConditionStart:
  push {r0-r7}

  // r1 = a1->dword34;
  ldr r1, [r5, #0x34]
  
  // a1->dword34 = r1 | 0x2000;
  ldr r0, =0x2000
  orr r0, r1
  str r0, [r5, #0x34]
  b @@End
  .pool
@@End:

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
.endarea

.org 0x0201B88C
.area 0x0201B8B4-., 0x00
  push {r0-r7, lr}
  mov r0, r5
  bl ReadScript_extended
  ldr r1, [r4]
  add r1, r0
  str r1, [r4]

  mov r0, 0x1
  strh r0, [r5, #0x28]

  pop {r0-r7, pc}
.endarea


.org 0x0201B9C4
.area 0x0201B9EC-., 0x00
  mov r0, r5
  bl ReadScript_extended
  ldr r1, [r4]
  add r0, r1
  str r0, [r4]

  mov r0, 0x1
  strh r0, [r5, #0x28]

  mov r0, r5
  bl 0x0201E554
.endarea

