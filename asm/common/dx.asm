// 一些 Mega Man Star Force DX 的优化
// https://github.com/Prof9/Mega-Man-Star-Force-DX

.thumb

.autoregion
.align
field_walkThroughNPC:
	push	r14

	mov	r1,0x2
	bl	0x02174408
	cmp	r0,0x1
	bne	@@canWalk

	ldrb	r0,[r4,0xF]
	cmp	r0,0x28
	bge	@@passThrough

	add	r0,0x1
	strb	r0,[r4,0xF]

@@cannotWalk:
	mov	r0,0x1
	b	@@end

@@canWalk:
	mov	r0,0x0
	strb	r0,[r4,0xF]
	b	@@end

@@passThrough:
	mov	r0,0x0

@@end:
	pop	r15
.endautoregion

.autoregion
.align
field_walkThroughNPCStop:
	push	r0,r14

	// Check if inside NPC
	// r0 already set
	mov	r1,0x2
	bl	0x02174280
	cmp	r0,0x0
	bne	@@end

	// Reset walk through NPC counter
	mov	r0,0x0
	strb	r0,[r4,0xF]

@@end:
	ldrh	r1,[r4,0xC]
	strb	r1,[r4,0x1]
	pop	r0,r15
.endautoregion
