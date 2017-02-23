from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label

class MenuButton(Button):
	pass

class MenuIconButton(MenuButton):
	pass

class MenuLabel(Label):
	pass

class NavBar(BoxLayout):
	screen=ObjectProperty()

class VolumeDropDown(DropDown):
	pass

class VolumeButton(MenuButton):
	dropDown=ObjectProperty()
	def __init__(self, **kwargs):
		self.dropDown=VolumeDropDown()
		super(VolumeButton,self).__init__(**kwargs)
