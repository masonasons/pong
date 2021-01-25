import lucia
import random
from . import prefs, rotation
from framework3d import timer
class player(object):
	def __init__(self):
		self.x=10
		self.y=0
		self.shielded=False
		self.shieldtimer=timer.Timer()
		self.shieldtime=30000
		self.shieldsnd=None
		self.randx=-1
		self.randy=-1
		self.movetimer=timer.Timer()
		self.movetime=0

	def move(self,dir):
		if dir==1:
			self.x-=1
		elif dir==2:
			self.x+=1
		if self.x<=0 or self.x>20:
			prefs.p3d.play_stationary("sounds/pong/border.flac",False)
			self.bounce(dir)
		else:
			prefs.p3d.play_stationary("sounds/pong/move.flac",False)
			prefs.p3d.x=prefs.me.x
#			prefs.p3d.y=prefs.me.y

	def bounce(self,dir):
		if dir==1:
			self.x+=1
		else:
			self.x-=1

	def shield(self):
		prefs.p3d.play_stationary("sounds/misc/shieldon.flac",False)
		if self.shielded==False:
			self.shieldsnd=prefs.p3d.play_stationary("sounds/misc/shieldloop.flac",True)
		self.shieldtimer.restart()
		self.shielded=True

	def loop(self):
		if prefs.g.ap==2:
			if self.movetimer.elapsed>=self.movetime:
				self.movetime=random.randint(80,160)
				self.movetimer.restart()
				if prefs.g.serving==True and prefs.g.server==1 or prefs.b.invisible==True and prefs.g.turn==1:
					if self.x>self.randx:
						self.move(1)
					elif self.x<self.randx:
						self.move(2)
					elif self.x==self.randx:
						if prefs.g.serving==True and prefs.g.server==1:
							prefs.b.serve(self.x,self.y)
						else:
							self.randx=random.randint(1,20)
				if prefs.g.turn==1 and prefs.g.serving==False:
					if prefs.b.invisible==False:
						if self.x>prefs.b.x:
							self.move(1)
						elif self.x<prefs.b.x:
							self.move(2)
					if rotation.get_2d_distance(self.x,self.y,prefs.b.x,prefs.b.y)<=5:
						prefs.b.hit(self.y,self.x)
						prefs.g.turn=2
		if self.shielded==True and self.shieldtimer.elapsed>=self.shieldtime:
			self.shielded=False
			prefs.p3d.destroy_sound(self.shieldsnd)
			prefs.p3d.play_stationary("sounds/misc/shieldoff.flac",False)

prefs.me=player()