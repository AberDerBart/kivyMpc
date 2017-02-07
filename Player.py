from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

import Interface

class PlaybackButtons(Widget):
	pass

class PlayerWidget(Screen):
	drawer=ObjectProperty(None)
	def on_pre_enter(self):
		self.clock=Clock.schedule_interval(self.update,.1)
	def on_leave(self):
		self.clock.cancel()
		self.drawer.state="closed"
	def update(self,dt):
		Interface.iFace.update()
		pass
		#this is to be adapted for the new mpc interface
