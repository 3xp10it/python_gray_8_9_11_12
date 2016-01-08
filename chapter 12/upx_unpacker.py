from ctypes import *
sys.path.append("c:\\PyEmu")
sys.path.append("c:\\PyEmu\\Lib")
exename=sys.argv[1]
outputfile=sys.argv[2]
emu=PEPyEmu()
if exename:
	if not emu.load(exename):
		print "load problem"
		sys.exit(2)
else:
	print "blank filename specified"
	sys.exit(3)
emu.set_library_handler("LoadLibraryA",loadlibrary)
emu.set_library_handler("GetProcAddress",getprocaddress)
emu.set_library_handler("VirtualProtect",virtualprotect)
emu.set_mnemonic_handler("jmp",jmp_handler)
emu.execute(start=emu.entry_point)

from PyEmu improt PEPyEmu
def loadlibrary(name,address):
	dllname=emu.get_memory_string(emu.get_memory(emu.get_register("ESP")+4))
	dllhandle=windll.kernel32.LoadLibraryA(dllname)
	emu.set_register("EAX",dllhandle)
	return_address=emu.get_memory(emu.get_register("ESP"))
	emu.set_register("ESP",emu.get_register("ESP")+8)
	emu.set_register("EIP",return_address)
 	return True

def getprocaddress(name,address):
	handle=emu.get_memory(emu.get_register("ESP")+4)
	proc_name=emu.get_memory(emu.get_register("ESP")+8)
	if (proc_name>>16):
		procname=emu.get_memory_string(emu.get_memory(emu.get_register("ESP")+8))
	else:
		procname=arg2
	emu.os.add_library(handle,procname)
	import_address=emu.os.get_library_address(procname)

	emu.set_register("EAX",import_address)
	return_address=emu.get_memory(emu.get_register("ESP"))
	emu.set_register("ESP",emu.get_register("ESP")+8)
	emu.set_register("EIP",return_address)
	return True


def virtualproctect(name,address):
	emu.set_register("EAX",1)
	return_address=emu.get_memory(emu.get_register("ESP"))
	emu.set_register("ESP",emu.get_register("ESP")+16)
	emu.set_register("EIP",return_address)
	return True


def jmp_handler(emu,mnemonic,eip,op1,op2,op3):
	if eip<emu.sections["UPX1"]["base"]:
		print "we are jumping out of the unpacking routine."
		print "oep=0x%08x" % eip
		dump_unpacked(emu)
		emu.emulating=False
		return True





def dump_unpacked(emu):
	global outputfile
	fh=open(outputfile,"wb")
	print "dumping upx0 section"
	base=emu.sections["UPX0"]["base"]
	length=emu.sections["UPX0"]["vsize"]
	print "base:0x%08x vsize:%08x" % (base,length)
	for x in range(length):
		fh.write("%c" % emu.get_memory(base+x,1))
	print "dumping upx1 section"

	base=emu.sections["UPX1"]["base"]
	length=emu.sections["UPX1"]["vsize"]
	print "base:0x%08x vsize:%08x" % (base,length)

	for x in range(length):
		fh.write("%c" % emu.get_memory(base+x,1))
	print "finished"


