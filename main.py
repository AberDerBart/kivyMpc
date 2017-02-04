import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty

import Interface

class PlayerWidget(Widget):
	pass

class PlayButton(Widget):
	def on_touch_down(self,touch):
		if(self.collide_point(touch.x,touch.y)):
			Interface.play()

class NextButton(Widget):
	def on_touch_down(self,touch):
		if(self.collide_point(touch.x,touch.y)):
			Interface.next()

class PrevButton(Widget):
	def on_touch_down(self,touch):
		if(self.collide_point(touch.x,touch.y)):
			Interface.prev()

class ButtonBox(Widget):
	pass

class MpdApp(App):
	artist=ObjectProperty(None)
	title=ObjectProperty(None)

	def build(self):
		return PlayerWidget()
	def update(self,dt):
		current=Interface.currentsong()
		if(current):
			self.artist.text=current["artist"]
			self.title.text=current["title"]
if __name__ == '__main__':
	app=MpdApp()
	Clock.schedule_interval(app.update, .1)
	app.run()
