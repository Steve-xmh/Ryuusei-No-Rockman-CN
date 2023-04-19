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
  mov r0, 0
  strb r0, [r1, #0x1]
  add r1, 0x2
@@End:
  pop {r0, pc}
.pool
.endautoregion
