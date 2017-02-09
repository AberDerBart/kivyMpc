from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import Interface
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.uix.listview import ListItemButton
from kivy.uix.listview import SelectableView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class PlaylistItem(SelectableView,BoxLayout):
	def __init__(self, **kwargs):
		text = kwargs.pop('text', None)
		index = kwargs['index']

		super(PlaylistItem, self).__init__(**kwargs)
		self.add_widget(ListItemButton(size_hint_x=4))
		self.add_widget(ListItemButton())

class PlaylistWidget(Screen):
	pass
