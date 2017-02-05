import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty

import Interface

class PlayerWidget(Widget):
	artist=ObjectProperty(None)
	title=ObjectProperty(None)
	progress=ObjectProperty(None)
	def update(self,dt):
		if(Interface.update() or self.title.text==""):
			current=Interface.currentsong()
			if(current):
				self.artist.text=current["artist"]
				self.title.text=current["title"]
			else:
				self.artist.text=""
				self.title.text=""
			status=Interface.status()	
			if(status):
				self.progress.max=float(status["duration"])
				self.progress.value=float(status["elapsed"])
			else:
				self.progress.value=0
		else:
			self.progress.value+=.1

class PlaybackButtons(Widget):
	pass

class MpdApp(App):

	def build(self):
		widget=PlayerWidget()
		Clock.schedule_interval(widget.update, .1)
		return widget

if __name__ == '__main__':
	app=MpdApp()
	app.run()
