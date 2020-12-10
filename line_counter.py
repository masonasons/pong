import pyperclip
thedata=""
global lines
lines=0
fn="game.pyw"
includes="engine"
import os
f=open("game.pyw","r")
data=f.read()
lines=len(data.split("\n"))
size=len(data)
f.close()
thedata+=fn+": "+str(lines)+", "+str(round(size/1024,2))+" KB\r\n"
if includes!=None:
	for i in os.listdir(includes):
		if ".py" in i:
			f=open(includes+"/"+i,"r")
			data=f.read()
			l=len(data.split("\n"))
			size+=len(data)
			thedata+=i+": "+str(l)+", "+str(round(len(data)/1024,2))+" KB\r\n"
			lines+=l
thedata+="Total: "+str(lines)+", "+str(round(size/1024,2))+" KB"
pyperclip.copy(thedata)