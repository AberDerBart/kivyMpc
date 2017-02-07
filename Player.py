from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import Interface

class PlaybackButtons(Widget):
	pass

class PlayerWidget(Screen):
	artist=ObjectProperty(None)
	title=ObjectProperty(None)
	progress=ObjectProperty(None)
	drawer=ObjectProperty(None)
	def on_pre_enter(self):
		self.clock=Clock.schedule_interval(self.update,.1)
	def on_leave(self):
		self.clock.cancel()
		self.drawer.state="closed"
	def update(self,dt):
		if(Interface.update() or self.title.text==""):
			"""if there is a current song, display it, else display nothing"""
			current=Interface.currentsong()
			if(current):
				self.artist.text=current["artist"]
				self.title.text=current["title"]
			else:
				self.artist.text=""
				self.title.text=""

			"""if the song updates, update the progressbar"""
			status=Interface.status()	
			if(status and "duration" in status and "elapsed" in status):
				self.progress.max=float(status["duration"])
				self.progress.value=float(status["elapsed"])
			else:
				self.progress.value=0
		else:
			"""if playing, let the progress bar run"""
			if(Interface.state=="play"):
				self.progress.value+=dt
