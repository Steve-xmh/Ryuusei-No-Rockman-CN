/*

处理文字输入的相关代码
输入名字时的相关内存地址：
姓：[0x021C5562..0x21C556E]?!
名：[0x021C5578..0x21C5584]?!

[0x021C5558..0x021C5561]!

スバル 25 77 50
0x19 0x4D 0x32

みょうじ

原编码里：BB E406 9D D2
输入编码里：BB EA 9D D2
汉化编码里：BB D01A 9D D002

星河 在输入内存里：31 01 B6 01
01 31 01 B6 [+85]
二进制： 0000000100110001 0000000110110110
原编码里：E44D E4D2 [+85]
二进制： 1110010001001101 1110010011010010
汉化编码里：D061 D102 [+A1]
二进制： 1101000001100001 1101000100000010

int __fastcall sub_2176B60(int result, _BYTE *a2, unsigned int a3)
{
  unsigned int i; // r5
  struct_v4 *v4; // r4
  unsigned int v5; // r7

  for ( i = 0; i < a3; i = (unsigned __int8)(i + 1) )
  {
    v4 = (struct_v4 *)(result + 2 * i);
    v5 = v4->unsigned___int161C;
    if ( v5 < 0xE4 ) // 从这里开始 Hook 0x02176B6E
    {
      *a2++ = v5;
    }
    else
    {
      if ( v5 < dword_2176BA0 )                 // v5 < 0x1E3
                                                // 恰好是字库末尾（字库总量）
      {
        *a2 = 0xE4;
        a2[1] = v4->unsigned___int161C - 0xE4;
      }
      else
      {
        *(_WORD *)a2 = (unsigned __int8)(v5 + 1);
      }
      a2 += 2;
    } // 到这里结束 0x02176B94
  }
  return result;
}

struct_v4 是一个输入上下文，其中比较重要的位移变量：
0x1C : 字符编码

在关闭窗口之后，先前输入的文字数据先是从 0x021C5558 复制到了 0x021C55DC 处

 */

.autoregion
; sub_2176B60
; 将字库编码转换回脚本编码的函数钩子
.align
sub_2176B60_hook:
  ; 此时 r7 是当前文字的字库编码
  ; r1 是需要写入脚本的地方
  ; 注意要处理超出编码的情况
  push {r0, lr}
  ; .msg "sub_2176B60_hook r0 = %r0% r1 = %r1% r7 = %r7%"
  ldr r0, =0x1E5 ; 虽然 0x1E5 确实是一个扩展字符编码，但是在编辑文字时不会出现，所以我们直接特判
  cmp r7, r0
  beq @@IsEnd
  mov r0, r1
  ; .msg "Font2Script ScriptPointer = %r0% FontEncode = %r7%"
  bl Script_FontEncodeToScriptEncodeHookLoop
  mov r1, r0
  b @@End
@@IsEnd:
  sub r7, #0xFF
  strb r7, [r1]
  add r1, 0x2
@@End:
  pop {r0, pc}
.pool
.endautoregion