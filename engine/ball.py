import random
from . import prefs
from framework import framework
class ball(object):
	def __init__(self):
		self.x=0
		self.y=0
		self.snd=None
		self.dir=3
		self.dir2=0
		self.speed=100
		self.bfspeed=300
		self.moving=False
		self.movetimer=framework.Timer()
		self.movetimer2=framework.Timer()
		self.invisible=False
		self.hits=0

	def serve(self,x,y):
		self.hits=0
		self.x=x
		self.y=y
		self.dir2=random.randint(1,2)
		prefs.p3d.play_2d("sounds/pong/hit.flac",self.x,self.y,False)
		self.snd=prefs.p3d.play_2d("sounds/pong/rolling.flac",self.x,self.y,True)
		if self.y==0:
			self.dir=3
			prefs.g.turn=2
		else:
			self.dir=4
			prefs.g.turn=1
		self.moving=True
		self.speed=500
		self.bfspeed=300
		prefs.g.serving=False

	def hit(self,y,x,silent=False):
		if silent==False:
			prefs.p3d.play_2d("sounds/pong/hit.flac",self.x,self.y,False)
		else:
			prefs.p3d.play_2d("sounds/misc/shieldhit.flac",self.x,self.y,False)
		self.hits+=1
		if self.hits>=15:
			prefs.p3d.play_stationary("sounds/crowd/cheer"+str(random.randint(1,5))+".flac",False)

		if self.dir==4:
			self.dir=3
			prefs.g.turn=2
		else:
			self.dir=4
			prefs.g.turn=1
		if self.invisible==True and silent==False:
			self.invisible=False
			prefs.p3d.play_2d("sounds/misc/appear.flac",self.x,self.y,False)
			self.snd=prefs.p3d.play_2d("sounds/pong/rolling.flac",self.x,self.y,True)

		prefs.random_event()
		if x>self.x:
			self.dir2=1
		elif x<self.x:
			self.dir2=2
		self.speed-=10
		if self.speed<=80:
			self.speed=80
		self.bfspeed-=5
		if self.bfspeed<=50:
			self.bfspeed=50

	def destroy(self):
		self.moving=False
		prefs.p3d.destroy_sound(self.snd)
		prefs.p3d.play_stationary(f"sounds/pong/goal{random.randint(1,8)}.flac",False)

		if self.y>=20:
			prefs.p3d.play_stationary(f"sounds/crowd/clap{random.randint(1,2)}.flac",False)
			prefs.p3d.play_2d("sounds/chars/"+prefs.comp.voice+"/lose"+str(random.randint(1,8))+".flac",prefs.comp.x,prefs.comp.y,False)
			framework.dlg_play("sounds/chars/"+prefs.pref.voice+"/taunt"+str(random.randint(1,8))+".flac",context=prefs.p3d.context)
		else:
			prefs.p3d.play_stationary(f"sounds/crowd/epicfail{random.randint(1,2)}.flac",False)
			prefs.p3d.play_2d("sounds/chars/"+prefs.comp.voice+"/taunt"+str(random.randint(1,8))+".flac",prefs.comp.x,prefs.comp.y,False)
			framework.dlg_play("sounds/chars/"+prefs.pref.voice+"/lose"+str(random.randint(1,8))+".flac",context=prefs.p3d.context)
		self.moving=False
		prefs.g.serving=True
		if prefs.g.server==1:
			prefs.g.server=2
			prefs.comp.randx=random.randint(1,20)
		else:
			prefs.g.server=1
			prefs.me.randx=random.randint(1,20)
		self.invisible=False

	def disappear(self):
		prefs.p3d.destroy_sound(self.snd)
		prefs.p3d.play_2d("sounds/misc/disappear.flac",self.x,self.y,False)
		self.invisible=True

	def loop(self):
		if self.moving==True and self.dir2>0 and self.movetimer2.elapsed>=self.bfspeed:
			self.movetimer2.restart()
			if self.dir2==2:
				self.x+=1
				if self.x>=20:
					self.dir2=1
					prefs.p3d.play_2d("sounds/pong/ballborder"+str(random.randint(1,5))+".flac",self.x,self.y,False)
			elif self.dir2==1:
				self.x-=1
				if self.x<=0:
					self.dir2=2
					prefs.p3d.play_2d("sounds/pong/ballborder"+str(random.randint(1,5))+".flac",self.x,self.y,False)

		if self.moving==True and self.movetimer.elapsed>=self.speed:
			self.movetimer.restart()
			if self.dir==3 and self.y<20:
				self.y+=1
			elif self.dir==4 and self.y>=0:
				self.y-=1
			if self.invisible==False:
				prefs.p3d.update_2d(self.snd,self.x,self.y)
			if prefs.g.turn==2 and self.y>=20:
				if prefs.comp.shielded==False:
					self.destroy()
					prefs.g.yourscore+=1
					prefs.g.turn=prefs.g.server
				else:
					self.hit(self.y,self.x,True)
			elif prefs.g.turn==1 and self.y<=0:
				if prefs.me.shielded==False:
					self.destroy()
					prefs.g.opscore+=1
					prefs.g.turn=prefs.g.server
				else:
					self.hit(self.y,self.x,True)