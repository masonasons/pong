import platform
import os
import sys
f2=open("errors.log","a")
sys.stderr=f2
from framework3d import window
window.initialize()
from engine import core
import application

window.show_window(f"{application.name} {application.versionstring}")
core.mainmenu()