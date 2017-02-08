from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import Interface

class PlaylistWidget(Screen):
	playlistWidget=ObjectProperty(None)
	def update(self):
		if(Interface.update() or True):
			playlist=Interface.playlist()
			if(playlist):
				self.playlistWidget.item_strings=[item["artist"]+ " - "+ item["title"] for item in playlist]
			else:
				self.playlistWidget.item_strings=[]

