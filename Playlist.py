from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from Interface import iFace
from kivy.properties import StringProperty,ObjectProperty

class PlaylistItem(BoxLayout):
	id=StringProperty("-1")
	artist=StringProperty()
	title=StringProperty()
	file=StringProperty()
	background=ObjectProperty((0,0,0))
	def __init__(self, **kwargs):
		iFace.bind(currentId=self.updateCurrent)
		self.bind(id=self.updateCurrent)
		super(PlaylistItem, self).__init__(**kwargs)
	def displayText(self,artist,title,fileName):
		if(artist != "" and title != ""):
			return artist + " - " + title
		else:
			return fileName
	def playAction(self):
		iFace.playid(int(self.id))
	def delAction(self):
		iFace.deleteid(int(self.id))
	def updateCurrent(self,instance,value):
		if(int(iFace.currentId)==int(self.id)):
			self.background=(.1,.1,.1)
		else:
			self.background=(0,0,0)
class PlaylistWidget(Screen):
	pass
