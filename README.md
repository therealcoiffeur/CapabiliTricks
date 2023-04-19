# CapabiliTricks

Let's imagine that during a pentest you managed to root a box, it can be interesting to come back 
later and perform actions as root user. To do this, many public techniques already exist and I just 
want to introduce to you, or re-introduce, techniques mixing Linux capabilities and Python.

Here is the list of capabilities that will be presented to you:

- CAP_CHOWN
- CAP_DAC_OVERRIDE
- CAP_FOWNER
- CAP_SETFCAP
- CAP_SETGID
- CAP_SETUID
- CAP_SYS_ADMIN
- CAP_SYS_PTRACE

## References

- https://man7.org/linux/man-pages/man7/capabilities.7.html
- https://docs.python.org/fr/3/library/os.html
- https://docs.python.org/fr/3/library/ctypes.html

