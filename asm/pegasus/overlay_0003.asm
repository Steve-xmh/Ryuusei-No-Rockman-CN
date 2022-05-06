.nds
.open TEMP+"/overlay/overlay_0003.bin",readu32(TEMP+"/y9.bin", 3 * 0x20 + 0x4)
.thumb

// Walk through NPCs
// 穿过 NPC
.org 0x2170A2A
	bl	field_walkThroughNPC
.org 0x21709B4
	bl	field_walkThroughNPCStop
.org 0x2171120
	bx	r14
.area 0x8E,0x00
field_walkThroughNPC:
	push	r14

	mov	r1,0x2
	bl	0x21713A4
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

field_walkThroughNPCStop:
	push	r0,r14

	// Check if inside NPC
	// r0 already set
	mov	r1,0x2
	bl	0x217121C
	cmp	r0,0x0
	bne	@@end

	// Reset walk through NPC counter
	mov	r0,0x0
	strb	r0,[r4,0xF]

@@end:
	ldrh	r1,[r4,0xC]
	strb	r1,[r4,0x1]
	pop	r0,r15
.endarea

	bx	r14

.close