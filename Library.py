from kivy.uix.screenmanager import Screen
from Interface import iFace
from kivy.properties import StringProperty
from kivy.uix.listview import SelectableView
from kivy.uix.boxlayout import BoxLayout

class LibraryItem(SelectableView,BoxLayout):
	infoDict={}
	dataType=StringProperty()
	def __init__(self, **kwargs):
		self.infoDict = kwargs.pop('text', {})
		self.dataType=kwargs.pop('type',"")
		super(PlaylistItem, self).__init__(**kwargs)

	def displayText(self):
		return "test"
	def addAction(self):
		print("add")
	def openAction(self):
		print("open")

class LibraryWidget(Screen):
	pass
