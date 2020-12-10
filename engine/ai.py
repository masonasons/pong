import random
from . import prefs, player
from lucia.utils import rotation
from framework import timer
class ai(object):
	def __init__(self):
		self.ax=10
		self.y=20
		self.movetimer=timer.Timer()
		self.movetime=0
		self.randx=0
		self.randy=0
		self.shielded=False
		self.shieldtimer=timer.Timer()
		self.shieldtime=30000
		self.shieldsnd=None
		self.voice=""

	def get_x(self):
		return self.ax

	def set_x(self,x):
		self.ax=x
		prefs.p3d.play_2d("sounds/pong/move.flac",self.x,self.y,False)
	x=property(get_x,set_x)

	def shield(self):
		prefs.p3d.play_2d("sounds/misc/shieldon.flac",self.x,self.y,False)
		if self.shielded==False:
			self.shieldsnd=prefs.p3d.play_2d("sounds/misc/shieldloop.flac",self.x,self.y,True)
		self.shieldtimer.restart()
		self.shielded=True

	def loop(self):
		if self.shielded==True and self.shieldtimer.elapsed>=self.shieldtime:
			self.shielded=False
			prefs.p3d.play_2d("sounds/misc/shieldoff.flac",self.x,self.y,False)
			prefs.p3d.destroy_sound(self.shieldsnd)
		if self.movetimer.elapsed>=self.movetime:
			self.movetime=random.randint(150,300)
			self.movetimer.restart()
			if prefs.g.serving==True and prefs.g.server==2 or prefs.b.invisible==True and prefs.g.turn==2:
				if self.x>self.randx:
					self.x-=1
				elif self.x<self.randx:
					self.x+=1
				elif self.x==self.randx:
					if prefs.g.serving==True and prefs.g.server==2:
						prefs.b.serve(self.x,self.y)
					else:
						self.randx=random.randint(1,20)
			if prefs.g.turn==2 and prefs.g.serving==False:
				if prefs.b.invisible==False:
					if self.x>prefs.b.x:
						self.x-=1
					elif self.x<prefs.b.x:
						self.x+=1
				if rotation.get_2d_distance(self.x,self.y,prefs.b.x,prefs.b.y)<=5 and prefs.g.turn==2:
					prefs.b.hit(self.y,self.x)