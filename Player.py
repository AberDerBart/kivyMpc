from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import Interface

class PlaybackButtons(Widget):
	pass

class PlayerWidget(Screen):
	drawer=ObjectProperty(None)
	def on_leave(self):
		self.drawer.state="closed"
