from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from Interface import iFace
from kivy.properties import StringProperty

class PlaylistItem(BoxLayout):
	id=StringProperty("-1")
	artist=StringProperty()
	title=StringProperty()
	file=StringProperty()
	def __init__(self, **kwargs):
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

class PlaylistWidget(Screen):
	pass
