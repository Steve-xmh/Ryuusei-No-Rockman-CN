/*

全新的文字打印代码，扩宽了 0xD0 - 0xE4 的字库到二字节，足以容纳五千左右的新字体
新的编码方式以满 0xE3 进一，在 0xD0 - 0xE4 间扩宽到第二字节，如此进一是为了调试时避开指令编码以防脚本行为出现问题，而且即时出错也只会显示成两个字符，不会有过大的影响
为了防止以后自己看不懂，几乎每行都加了注释
原解析文字的函数位置在 0x0201B0BC

从 IDA 中逆向出来的部分代码片段，这一段主要在剧情过场动画中的对话框里被调用执行。

int __fastcall sub_201B0BC(ScriptCtx *ctx)
{
  unsigned __int16 *v2; // r4
  int v3; // r1
  unsigned __int8 *v4; // r0

  v2 = &ctx->current_script_code;
  while ( 1 )
  {
    ctx->current_script_code = *ctx->current_script_data;
    if ( ctx->current_script_code < 0xE5u )
      break;
    *v2 -= 229;
    if ( sub_201ED8C(ctx, ctx->current_script_code) == 1 )
      goto LABEL_22;
  }
  --ctx->char33;
  if ( sub_201ED10(ctx, 0x10000000) )
    --ctx->char33;
  ctx->word52 = ctx->current_script_code;
  if ( ctx->word52 == 0xE4 )
    ctx->word52 += ctx->current_script_data[1];
  if ( ctx->char33 <= 0 )
  {
    if ( ++ctx->word72 > 0x10u )
      ctx->byte63 = 1;
    v3 = ctx->dword34;
    if ( ctx->current_script_code == 0xE4 ) // 判断当前字节是否为 0xE4，正好是第二个码表区域的先行字节，所以等会我们要改动这个
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
    ctx->current_script_data = v4;
    ctx->char33 = ctx->byte32;
    if ( !sub_201ED10(ctx, 64) )
    {
      if ( sub_201ED10(ctx, 0x10000000) )
      {
        if ( !ctx->byte7F )
          sub_2025C5C(*off_201B218, *(*off_201B214[0] + 52));
        ctx->byte7F ^= 1u;
      }
      else
      {
        sub_2025C5C(*off_201B218, *(*off_201B214[0] + 52));
      }
    }
    sub_201E698(ctx);
    sub_201B53C(ctx);
  }
LABEL_22:
  sub_201B2F4(ctx);
  sub_201B62C(ctx);
  sub_201B718(ctx);
  return sub_201B83C(ctx);
}

0x0201B21C

*/

/*
int __fastcall sub_201B21C(struct_a1 *a1)
{
  unsigned __int16 *v2; // r4
  _DWORD *v3; // r6
  _WORD *v4; // r7
  unsigned int v5; // r0
  unsigned __int8 **v7; // [sp+0h] [bp-18h]

  v2 = &a1->current_script_code;
  v3 = &a1->dword34;
  v4 = &a1->word72;
  v7 = &a1->current_script_pointer;
  while ( (a1->dword34 & 1) != 0 )
  {
    a1->current_script_code = *a1->current_script_pointer;
    v5 = a1->current_script_code;
    if ( v5 < 0xE5 )
    {
      *v3 |= 0x2000u;
      if ( v5 == 228 )
      {
        *v2 += a1->current_script_pointer[1];
        copy_font_graph(a1);
        ++*v4;
        *v7 += 2;
      }
      else
      {
        copy_font_graph(a1);
        ++*v4;
        ++*v7;
      }
    }
    else
    {
      *v2 -= 229;
      if ( sub_201ED8C(a1, a1->current_script_code) == 1 )
        break;
    }
    if ( (unsigned __int16)a1->word72 > 0x10u )
      a1->byte63 = 1;
  }
  sub_201E698(a1);
  sub_201B2F4(a1);
  sub_201B53C(a1);
  sub_201B62C((int)a1);
  sub_201B718(a1);
  sub_201B83C(a1);
  return sub_201661C(a1, *(_DWORD *)off_201B2EC, *((_DWORD *)off_201B2EC + 1));
}

 */

.thumb


.autoregion
.align
@FontFileLoadedVar: // 是否加载完毕
  .dw 0
.endautoregion


.autoregion
.align
ReadScript_Init:
  push {r0-r7, lr}

  // 初始化文件对象
  // 0x0209842C void FS_InitFile( FSFile *p_file );
  // 打开文件
  // 0x020980DC BOOL FS_OpenFile( FSFile *p_file, const char *path );
  
  // 8x8 字库
  ldr r0,=Font0FileVar
  blx FS_InitFile
  // ldr r0,=Font0FileVar
  ldr r1,=@Font0FileName
  blx FS_OpenFile
  
  cmp r0,#1
  beq @@LoadFont1
  
  .msg "Failed to open datbin/fonts/font0.bin!"
  b .
  
@@LoadFont1:

  // 8x16 细字库
  ldr r0,=Font1FileVar
  blx FS_InitFile
  // ldr r0,=Font1FileVar
  ldr r1,=@Font1FileName
  blx FS_OpenFile
  
  cmp r0,#1
  beq @@LoadFont2
  
  .msg "Failed to open datbin/fonts/font1.bin!"
  b .
  
@@LoadFont2:

  // 8x16 粗字库
  ldr r0,=Font2FileVar
  blx FS_InitFile
  // ldr r0,=Font2FileVar
  ldr r1,=@Font2FileName
  blx FS_OpenFile

  cmp r0,#1
  beq @@LoadFont3
  
  .msg "Failed to open datbin/fonts/font2.bin!"
  b .
  
@@LoadFont3:

  // 16x16 字库
  ldr r0,=Font3FileVar
  blx FS_InitFile
  // ldr r0,=Font3FileVar
  ldr r1,=@Font3FileName
  blx FS_OpenFile
  
  cmp r0,#1
  beq @@LoadFont3Width
  
  .msg "Failed to open datbin/fonts/font3.bin!"
  b .
  
@@LoadFont3Width:

  // 16x16 字库宽度表
  ldr r0,=Font3WidthFileVar
  blx FS_InitFile
  // ldr r0,=Font3WidthFileVar
  ldr r1,=@Font3WidthFileName
  blx FS_OpenFile
  
  cmp r0,#1
  beq @@End
  
  .msg "Failed to open datbin/fonts/font3_width.bin!"
  b .
  
@@End:

  pop {r0-r7, pc}
.pool
.endautoregion

.autoregion
.align

// 脚本上下文结构的一些比较重要的位移变量：
// 0x10 : 当前脚本指针（所指向的位置为当前字符编码）
// 0x1C : 所使用的字库位置
// 0x28 : 当前字符编码

// 我们自己的文字打印的代码
// 大致步骤如下（毫无优化的版本）：
// 1. 如果没有打开的话，打开对应的字库文件
// 2. 确认当前编码是否在第二码表范围内
// 3. 如果不在范围，则不动，否则，换算成字库中的相对位置
// 4. 读取字库文件，移动文件头到相应的文字位置，读取一个字形到原字库的 0 字位置
// 5. 将编码设置成 1（对应原字库的 0 字） 然鹅并没有
// 6. 调用原有的字符读取程序，打印那个位置的文字（也就是我们读取进去的内容）
// 7. 返回到原先的执行位置
ReadScript_extended:
  // 参数 r0：文字打印上下文结构指针
  // 返回值：r0 字符编码长度，1 或 2
  // r5 = 文字打印上下文结构指针
  push {r1-r7, lr}
  ; bl Debug_PrintScriptContext
  // 我怕了 bl 指令了（）就先推到栈里存着了（）
  push {r0}
  mov r5, r0
  
  // 检查字体是否初始化
  ; ldr r6, =@FontFileLoadedVar
  ; ldr r6, [r6]
  ; cmp r6,0x0
  ; bne @@LoadCharacter_Loaded

  // 尚未初始化，开始打开字库

; @@Success:
  ; ldr r1,=@FontFileLoadedVar
  ; mov r0, 0x1
  ; str r0, [r1]
  
@@LoadCharacter_Loaded:
  // 检测指向的编码是否在 0xD0 - 0xE4 之间，有则进入第二码表
  // R5 寄存器

  // 取出脚本上下文结构，开始处理编码
  pop {r5}

  ldrh r1, [r5, #0x28] // 当前文字编码

  mov r7, 0x1

  cmp r1, 0xD0
  blt @@NotInSecondTable
  cmp r1, 0xE4
  bgt @@NotInSecondTable

  mov r7, 0x2

  cmp r1, 0xE4
  beq @@InOriginalSecondTable
  b @@InSecondTable
@@InOriginalSecondTable:
  // 还在原始的第二码表里
  ldr r0, [r5, #0x10] // 当前脚本指针位置
  ldrb r0, [r0, #0x1] // 脚本指针的下一个位置——下一个字符
  add r1, r0 // 与其相加
  b @@NotInSecondTable
@@InSecondTable:
  // 确认在内，计算正确的字符位置
  sub r1, 0xD0 // r1 -= 0xD0
  mov r2, 0xE4
  mul r1, r2 // r1 *= r2 // 0xE3

  // 加载下一个编码
  ldr r0, [r5, #0x10] // 当前脚本指针位置
  ldrb r0, [r0, #0x1] // 脚本指针的下一个位置——下一个字符
  add r1, r0 // 与其相加
  add r1, 0xD0 // 再加上 0xD0 位移

  // 那么现在 r1 的结果就是真正的码表位置了
@@NotInSecondTable:
  mov r0, r5
  bl @LoadCharacterFromFile

  // 将字体放在了原先 0 的位置，然后再把码表设置成 01，让其绘制上面的字形
  // 关闭文件（应该不需要吧）
  // 0x02098094 BOOL FS_CloseFile( FSFile *p_file );

@@LoadCharacterEnd:
  mov r0, r7
  pop {r1-r7, pc}
  .pool
.endautoregion

.autoregion
.align
@LoadCharacterFromFile:
  // r0 脚本上下文
  // r1 字符的位置
  push {r0-r7, lr}
  ldr r2, [r0, #0x1C] // 脚本所使用的字库位置
  ldr r3,=Font8x8Zero - 0x20
  cmp r3, r2
  beq @@Size8x8
  ldr r3,=Font8x16Zero - 0x40
  cmp r3, r2
  beq @@Size8x16
  ldr r3,=Font8x16BoldZero - 0x40
  cmp r3, r2
  beq @@Size8x16Bold
  ldr r3,=Font12x12Zero - 0x80
  cmp r3, r2
  beq @@Size16x16
  // 错误的参数，在这里死循环
@@WrongArgument:
  b @@WrongArgument
  ; 使用缓存版本
@@Size8x8:
  mov r0, r1
  ldr r1, =FontCache_Font_CacheArea_00000000
  bl FontCommon_LoadCharacterFromCacheOrRead
  pop {r0-r7, pc}
@@Size8x16:
  mov r0, r1
  ldr r1, =FontCache_Font_CacheArea_00000001
  bl FontCommon_LoadCharacterFromCacheOrRead
  pop {r0-r7, pc}
@@Size8x16Bold:
  mov r0, r1
  ldr r1, =FontCache_Font_CacheArea_00000002
  bl FontCommon_LoadCharacterFromCacheOrRead
  pop {r0-r7, pc}
@@Size16x16:
  mov r0, r1
  ldr r1, =Font3_CacheArea
  bl Font3_LoadCharacterFromCacheOrRead
  pop {r0-r7, pc}
  .pool
.endautoregion

.autoregion
.align
@Font0FileName:
  .asciiz "datbin/fonts/font0.bin" // 8x8
.endautoregion

.autoregion
.align
@Font1FileName:
  .asciiz "/datbin/fonts/font1.bin" // 8x16 细
.endautoregion

.autoregion
.align
@Font2FileName:
  .asciiz "/datbin/fonts/font2.bin" // 8x16 粗
.endautoregion

.autoregion
.align
@Font3FileName:
  .asciiz "/datbin/fonts/font3.bin" // 12x12 粗
.endautoregion

.autoregion
.align
@Font3WidthFileName:
  .asciiz "/datbin/fonts/font3_width.bin" // 12x12 字宽
.endautoregion

.autoregion
.align
Font0FileVar: // 一个 FSFile 的内存区域
  .fill 0x3C
.endautoregion

.autoregion
.align
Font1FileVar: // 一个 FSFile 的内存区域
  .fill 0x3C
.endautoregion

.autoregion
.align
Font2FileVar: // 一个 FSFile 的内存区域
  .fill 0x3C
.endautoregion

.autoregion
.align
Font3FileVar: // 一个 FSFile 的内存区域
  .fill 0x3C
.endautoregion

.autoregion
.align
Font3WidthFileVar: // 一个 FSFile 的内存区域
  .fill 0x3C
.endautoregion
