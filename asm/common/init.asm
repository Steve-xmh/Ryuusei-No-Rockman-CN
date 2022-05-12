.thumb

.autoregion
.align
; 拦截正常的文件系统初始化函数
; 在这里初始化我们需要的东西
Fake_FS_Init:
	push {lr}
	blx FS_Init
	.msg "Ryuusei No Rockman 1 CN Patch by SteveXMH!"
	.msg "Special thanks to:"
	.msg "  - Enler"
	.msg "  - Prof. 9"
	.msg ""
	.msg "Initializing fonts..."
	bl ReadScript_Init
	.msg "Patch initialization finished!"
	pop {pc}
.endautoregion