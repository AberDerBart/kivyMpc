from kivy.uix.screenmanager import Screen
from kivy.uix.listview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from Interface import iFace

class PlaylistItem(SelectableView,BoxLayout):
	songDict={}
	def __init__(self, **kwargs):
		self.songDict = kwargs.pop('text', None)
		super(PlaylistItem, self).__init__(**kwargs)

	def displayText(self):
		return self.songDict["artist"] + " - " + self.songDict["title"]
	def playAction(self):
		print("play "+self.displayText())
	def delAction(self):
		print("del "+self.displayText())

class PlaylistWidget(Screen):
	def __init__(self,**kwargs):
		super(PlaylistWidget,self).__init__(**kwargs)
