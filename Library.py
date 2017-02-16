from kivy.uix.screenmanager import Screen
from Interface import iFace
from kivy.uix.listview import SelectableView
from kivy.uix.boxlayout import BoxLayout

class LibraryItem(SelectableView,BoxLayout):
	songDict={}
	def __init__(self, **kwargs):
		self.songDict = kwargs.pop('text', {})
		super(LibraryItem, self).__init__(**kwargs)

	def displayText(self):
		text=""
		if("artist" in self.songDict):
			text+=self.songDict["artist"]+" - "
		text+=self.songDict.get("title", self.songDict.get("file"))
		return text
	def addAction(self):
		iFace.add(self.songDict["file"])

class LibraryWidget(Screen):
	pass
