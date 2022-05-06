.thumb

// 天马版的代码所需插入位置，我们要在这里捕获脚本数据

// 过场动画的逐字打印函数
OriginalPrintFontConditionStart equ 0x201b158
OriginalPrintFontConditionEnd equ 0x201b192

// 过场动画的逐字打印函数 的前面的一个判断
OriginalAdditionalConditionStart equ 0x201b114
OriginalAdditionalConditionEnd equ 0x201b130

// 某些小字体的常用打印函数
// sub_202002C
OriginalPrintAnotherFontConditionStart equ 0x02020060
OriginalPrintAnotherFontConditionEnd equ 0x0202007A

// 过场动画的瞬间打印的函数
OriginalPrintInstantFontConditionStart equ 0x201b254
OriginalPrintInstantFontConditionEnd equ 0x201b2a2

.include "asm/common/text_hooks.asm"
