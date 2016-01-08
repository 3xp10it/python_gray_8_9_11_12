from idaapi import *
danger_funcs=['strcpy','sprintf','strncpy']
for func in danger_funcs:
	func_addr=LocByName(func)
	if func_addr!=BADADDR:
		func_list_call=CodeRefsTo(func_addr,0)
		print "------------------------------------"
		for ref in func_list_call:
			print "0x%08x" % ref
			SetColor(ref,CIC_ITEM,0x0000ff)
			