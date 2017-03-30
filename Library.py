from kivy.uix.screenmanager import Screen
from Interface import iFace
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty

class LibraryItem(BoxLayout):
	artist=StringProperty()
	title=StringProperty()
	file=StringProperty()
	background=ObjectProperty((0,0,0))
	def __init__(self, **kwargs):
		iFace.bind(playlist=self.updatePlaylist)
		self.bind(file=self.updatePlaylist)
		super(LibraryItem, self).__init__(**kwargs)

	def displayText(self,artist,title,fileName):
		if(artist != "" and title != ""):
			return artist + " - " + title
		else:
			return fileName
	def addAction(self):
		iFace.add(self.file)
	def updatePlaylist(self,instance,value):
		contained=False
		for item in iFace.playlist:
			if item.get("file")==self.file:
				contained=True
		
		if(contained):
			self.background=(.1,.1,.1)
		else:
			self.background=(0,0,0)


class LibraryWidget(Screen):
	pass
