name="Masonasons Pong"
version="4.0"
author="Masonasons Productions"
beta=False
betanum=1
if beta==True:
	versionstring=str(version)+" Pre"+str(betanum)
else:
	versionstring=str(version)
from engine import core
import os
import platform
if platform.system()=="Darwin":
	shortname="pongmac"
	update_url="http://masonasons.me/softs/PongMac.zip"
#	update_path=core.get_download_folder()+"/PongMac.zip"
else:
	shortname="pong"
	update_url="http://masonasons.me/softs/Pong.zip"
	update_path="Pong.zip"
version_url="http://masonasons.me/projects/pongversion.txt"
