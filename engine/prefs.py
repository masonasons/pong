import random
from framework3d import framework
global p
p=None
global p3d
p3d=None
global me
me=None
global pref
pref=None
global b
b=None
global g
g=None
global comp
comp=None
class prefs(object):
	def __init__(self,path):
		self.sd=framework.savedata(path+"/pong.dat","fuckerball")
		self.sd.load()
		self.voice=self.sd.dic.get("voice","")

	def save(self):
		self.sd.add("voice",self.voice)
		self.sd.save()


def random_event():
	if g.mode==2:
		return
	event=random.randint(1,20)
	if event==1:
		b.disappear()
	if event==2:
		if g.turn==1:
			comp.shield()
		else:
			me.shield()