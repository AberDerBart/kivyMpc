from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import Interface

class PlaylistWidget(Widget):
	playlistWidget=ObjectProperty(None)
	def update(self):
		if(Interface.update() or True):
			playlist=Interface.playlist()
			if(playlist):
				self.playlistWidget.item_strings=[item["artist"]+ " - "+ item["title"] for item in playlist]
			else:
				self.playlistWidget.item_strings=[]

