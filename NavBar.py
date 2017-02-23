from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

class NavBar(BoxLayout):
	screen=ObjectProperty()

class VolumeDropDown(DropDown):
	pass

class VolumeButton(Button):
	dropDown=ObjectProperty()
	def __init__(self, **kwargs):
		self.dropDown=VolumeDropDown()
		super(VolumeButton,self).__init__(**kwargs)
