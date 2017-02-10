from kivy.uix.screenmanager import Screen
from kivy.uix.listview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from Interface import iFace
from kivy.properties import ObjectProperty,NumericProperty

class PlaylistItem(SelectableView,BoxLayout):
	songDict={}
	songId=NumericProperty(-1)
	def __init__(self, **kwargs):
		self.songDict = kwargs.pop('text', {})
		self.songId=int(self.songDict.get("id",-1))
		super(PlaylistItem, self).__init__(**kwargs)

	def displayText(self):
		text=""
		if("artist" in self.songDict):
			text+=self.songDict["artist"]+" - "
		text+=self.songDict.get("title", self.songDict.get("file"))
		return text
	def playAction(self):
		iFace.playid(int(self.songId))
	def delAction(self):
		iFace.deleteid(int(self.songId))

class PlaylistWidget(Screen):
	def __init__(self,**kwargs):
		super(PlaylistWidget,self).__init__(**kwargs)
