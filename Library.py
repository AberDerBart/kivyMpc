from kivy.uix.screenmanager import Screen
from Interface import iFace
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

class LibraryItem(BoxLayout):
	artist=StringProperty()
	title=StringProperty()
	file=StringProperty()
	def __init__(self, **kwargs):
		super(LibraryItem, self).__init__(**kwargs)

	def displayText(self,artist,title,fileName):
		if(artist != "" and title != ""):
			return artist + " - " + title
		else:
			return fileName
	def addAction(self):
		iFace.add(self.file)

class LibraryWidget(Screen):
	pass
