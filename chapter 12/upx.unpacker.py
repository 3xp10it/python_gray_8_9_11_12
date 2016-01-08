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







def dump_unpacked(emu):
	global outputfile
	fh=open(outputfile,"wb")
	print "dumping upx0 section"
	base=emu.sections["UPX0"]["base"]
	length=emu.sections["UPX0"]["vsize"]
	print "base:0x%08x vsize:%08x" % (base,length)
	for x in range(length):
		fh.write("%c" % emu.get_memory(base+x,1))
	print " "
