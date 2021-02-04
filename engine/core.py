import synthizer
import random
from . import ai, ball, player, prefs, var
from framework3d import framework, rotation
import pygame
import time
import sys
import os
import platform
global compiled
compiled=getattr(sys, 'frozen', False)
if platform.system()=="Darwin":
	savepath=os.path.expanduser("~/.pong")
else:
	savepath="data"
if not os.path.exists(savepath):
	os.makedirs(savepath)

prefs.p3d=framework.sound_manager()
prefs.p3d.max_distance=30
prefs.p3d.hrtf=True
prefs.g=None
prefs.b=None
prefs.comp=None
prefs.pref=prefs.prefs(savepath)

def reset():
	prefs.p3d.destroy_all()
	prefs.me.x=10
	prefs.me.y=0

def get_download_folder():
	home = os.path.expanduser("~")
	return os.path.join(home, "Downloads")

def setupmenu(music=""):
	return framework.menu3d(pool=prefs.p3d,click_sound="sounds/menu/click.flac",enter_sound="sounds/menu/select.flac",music=music,fade_music=True)

def mainmenu():
	m=setupmenu("sounds/music/menu.flac")
	if prefs.pref.voice!="":
		m.add_item_tts("Play","play")
	m.add_item_tts("Set default character","char")
	m.add_item_tts("Test speakers","test")
	m.add_item_tts("Exit","exit")
	result=m.run("Pong Main Menu.")
	if result==0 or result==-1:
		sys.exit()
	if result.name=="play":
		m=modemenu()
		if m>0:
			l=lengthmenu()
			if l>0:
				gm=apmenu()
				if gm>0:
					game(m, l,gm)
		else:
			mainmenu()
	elif result.name=="char":
		charmenu()
	elif result.name=="test":
		framework.dlg_play("sounds/menu/test.flac","sound3d",context=prefs.p3d.context)
		mainmenu()
	else:
		sys.exit()

def charmenu():
	m=framework.menu3d(pool=prefs.p3d,click_sound="sounds/CharSelect/click.flac",enter_sound="sounds/CharSelect/enter.flac",music="sounds/music/charselect.flac",fade_music=True,up_and_down=False,left_and_right=True)
	for i in os.listdir("sounds/chars"):
		m.add_item_tts(i,i)
	result=m.run("sounds/CharSelect/0.flac",False)
	try:
		if result.name!="":
			prefs.pref.voice=result.name
			framework.dlg_play("sounds/chars/"+prefs.pref.voice+"/name.flac","sound3d",context=prefs.p3d.context)
			prefs.pref.save()
			mainmenu()
		else:
			mainmenu()
	except:
		mainmenu()

def lengthmenu():
	m=setupmenu()
	m.add_item_tts("Shortest",6)
	m.add_item_tts("Short",11)
	m.add_item_tts("Medium",16)
	m.add_item_tts("Long",21)
	m.add_item_tts("Longest",26)
	result=m.run("Select a game length.")
	if result==0:
		return 0
	else:
		try:
			return result.name
		except:
			return result

def modemenu():
	m=setupmenu()
	m.add_item_tts("Normal",1)
	m.add_item_tts("Classic",2)
	result=m.run("Select a game type.")
	if result==0:
		return 0
	else:
		try:
			return result.name
		except:
			return result

def apmenu():
	m=setupmenu()
	m.add_item_tts("Normal",1)
	m.add_item_tts("Autopilot",2)
	result=m.run("Select a game mode.")
	if result==0:
		return 0
	else:
		try:
			return result.name
		except:
			return result

def game(mode, length,gm):
	reset()
	prefs.p3d.z=4
#	prefs.p3d.context.distance_model=prefs.p3d.context.distance_model.INVERSE
	prefs.p3d.internal_reverb.gain=0.3
	prefs.p3d.internal_reverb.mean_free_path=0.07
	prefs.p3d.internal_reverb.t60=0.8
	cl=prefs.p3d.play_stationary("sounds/crowd/loop.flac",True)
	cl.volume=-15
	prefs.g=var.var()
	prefs.b=ball.ball()
	prefs.comp=ai.ai()
	voices=os.listdir("sounds/chars")
	prefs.comp.voice=voices[random.randint(0,len(voices)-1)]
	prefs.g.length=length
	prefs.g.mode=mode
	prefs.g.ap=gm
	prefs.p3d.reverb=True
	music=prefs.p3d.play_stationary("sounds/music/InGame.flac",True,False)
	music.volume=-30
	prefs.me.randx=random.randint(1,20)
	prefs.p3d.play_2d("sounds/chars/"+prefs.comp.voice+"/start.flac",prefs.comp.x,prefs.comp.y,False)
	framework.dlg_play("sounds/chars/"+prefs.pref.voice+"/start.flac","sound3d",context=prefs.p3d.context)
	while 1:
		framework.process_events()
		time.sleep(0.005)
		prefs.b.loop()
		prefs.me.loop()
		prefs.comp.loop()
		if framework.key_pressed(pygame.K_PAGEUP):
			music.handle.volume+=2
		if framework.key_pressed(pygame.K_PAGEDOWN):
			music.handle.volume-=2
		if prefs.g.yourscore>=prefs.g.length:
			prefs.p3d.play_2d("sounds/chars/"+prefs.comp.voice+"/lose.flac",prefs.comp.x,prefs.comp.y,False)
			framework.dlg_play("sounds/chars/"+prefs.pref.voice+"/win.flac","sound3d",False,context=prefs.p3d.context)
			framework.dlg_play("sounds/music/game_won.flac","sound3d",context=prefs.p3d.context)
			reset()
			mainmenu()
		if prefs.g.opscore>=prefs.g.length:
			framework.dlg_play("sounds/music/game_lost.flac","sound3d",False,context=prefs.p3d.context)
			reset()
			mainmenu()

		if framework.key_pressed(pygame.K_ESCAPE):
			prefs.p3d.destroy_all()
			prefs.p3d.reverb=False
			mainmenu()

		if framework.key_pressed(pygame.K_s):
			framework.speak(f"{prefs.g.yourscore}, {prefs.g.opscore}")
		if prefs.g.ap==1:
			if framework.key_pressed(pygame.K_UP):
				if prefs.g.serving==True and prefs.g.server==1:
					prefs.b.serve(prefs.me.x,prefs.me.y)
				elif prefs.g.turn==1 and rotation.get_2d_distance(prefs.me.x,prefs.me.y,prefs.b.x,prefs.b.y)<=5 and prefs.g.serving==False:
					prefs.b.hit(prefs.me.y,prefs.me.x)
			if framework.key_pressed(pygame.K_LEFT):
				prefs.me.move(1)
			if framework.key_pressed(pygame.K_RIGHT):
				prefs.me.move(2)
