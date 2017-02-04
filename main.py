import kivy
import mpd
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.widget import Widget



class PlayerWidget(Widget):
	pass

class PlayButton(Widget):
	def on_touch_down(self,touch):
		if(self.collide_point(touch.x,touch.y)):
			print("play")

class NextButton(Widget):
	def on_touch_down(self,touch):
		if(self.collide_point(touch.x,touch.y)):
			print("next")

class PrevButton(Widget):
	def on_touch_down(self,touch):
		if(self.collide_point(touch.x,touch.y)):
			print("prev")

class ButtonBox(Widget):
	pass

class MpdApp(App):
	def build(self):
		return PlayerWidget()

if __name__ == '__main__':
	MpdApp().run()
