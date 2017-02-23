from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty,NumericProperty
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
	screenManager=ObjectProperty()

class NavBarFrame(BoxLayout):
	screenManager=ObjectProperty()

class VolumeDropDown(DropDown):
	itemHeight=NumericProperty(50)

class VolumeButton(MenuButton):
	dropDown=ObjectProperty()
	def __init__(self, **kwargs):
		self.dropDown=VolumeDropDown()
		self.dropDown.itemHeight=self.height
		super(VolumeButton,self).__init__(**kwargs)
