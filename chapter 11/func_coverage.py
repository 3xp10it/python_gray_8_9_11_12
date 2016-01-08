from idaapi import * 
class FuncCoverage(DBG_Hooks):
	def dbg_set(self,tid,ea):
		print "hit:0x%08x" % ea
		return 1 
debugger=FuncCoverage()
debugger.hook()
current_addr=ScreenEA()
for function in Functions(SegStart(current_addr),SegEnd(current_addr)):
	AddBpt(function)
	SetBpAttr(function,BPTATTR_FLAGS,0x0)
num_breakpoints=GetBptOty()
print "set %d breakpoints" % num_breakpoints