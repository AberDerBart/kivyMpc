import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from Player import PlayerWidget

class MpdApp(App):

	def build(self):
		sm=ScreenManager()
		sm.transition=NoTransition()
		sm.add_widget(PlayerWidget(name="player"))
		return sm
	def build_config(self,config):
		config.setdefaults("Connection",{"host":"localhost","port":6600})
	def build_settings(self,settings):
		settings.add_json_panel("Connection", self.config, "connectionSettings.json")

if __name__ == '__main__':
	app=MpdApp()
	app.run()
