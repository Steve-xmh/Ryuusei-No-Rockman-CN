.nds

// 缩小 ARM9 的大小
.create TEMP+"/arm9.dec",0
.import TEMP+"/arm9.bin",0,readu32(TEMP+"/header.bin",0x2C)
.close