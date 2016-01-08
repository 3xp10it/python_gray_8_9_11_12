import sys
sys.path.append("c:\\PyEmu")
sys.path.append("c:\\PyEmu\\lib")
from PyEmu import *
def ret_handler(emu,address):
	num1=emu.get_stack_argument("arg_0")
	num2=emu.get_stack_argument("arg_4")
	sum=emu.get_register("EAX")
	print "function took:%d,%d and the result is %d" % (num1,num2,sum)
	return True

emu=IDAPyEmu()
code_start=SegByName(".text")
code_end=SegEnd(code_start)
data_start=SegByName(".data")
data_end=SegEnd(data_start)
while code_start<code_end:
	emu.set_memory(code_start,GetOriginalByte(code_start),size=1)
	code_start+=1

print "finished loading  code section into memory"

while data_start<data_end:
	emu.set_memory(data_start,GetOriginalByte(data_start),size=1)
	data_start+=1

print "finished loading data section into memory"
emu.set_register("EIP",0x00401000)
emu.set_mnemonic_handler("ret",ret_handler)
emu.set_stack_argument(0x8,0x00000001,name="arg_0")
emu.set_stack_argument(0xc,0x00000002,name="arg_4")

emu.execute(steps=10)
print "finished function emulation run"

