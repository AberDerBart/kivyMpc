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
	def update(self,dt):
		if(Interface.update() or self.title.text==""):
			current=Interface.currentsong()
			if(current):
				self.artist.text=current["artist"]
				self.title.text=current["title"]
			else:
				self.artist.text=""
				self.title.text=""

class PlaybackButtons(Widget):
	def play(self):
		Interface.play()
	def next(self):
		Interface.next()
	def prev(self):
		Interface.prev()

class MpdApp(App):

	def build(self):
		widget=PlayerWidget()
		Clock.schedule_interval(widget.update, .1)
		return widget

if __name__ == '__main__':
	app=MpdApp()
	app.run()
