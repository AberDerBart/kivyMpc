from kivy.uix.screenmanager import Screen
from kivy.uix.listview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from Interface import iFace

class PlaylistItem(SelectableView,BoxLayout):
	songDict={}
	songId=-1
	def __init__(self, **kwargs):
		self.songDict = kwargs.pop('text', None)
		self.songId=self.songDict["id"]
		super(PlaylistItem, self).__init__(**kwargs)

	def displayText(self):
		text=""
		if("artist" in self.songDict):
			text+=self.songDict["artist"]+" - "
		text+=self.songDict.get("title", self.songDict.get("file"))
		return text
	def playAction(self):
		iFace.playid(self.songId)
	def delAction(self):
		iFace.deleteid(self.songId)

class PlaylistWidget(Screen):
	def __init__(self,**kwargs):
		super(PlaylistWidget,self).__init__(**kwargs)
