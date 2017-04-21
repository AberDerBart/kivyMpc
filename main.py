import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from Player import PlayerWidget
from Interface import iFace
from Playlist import PlaylistWidget
from Library import LibraryWidget
from Scheduler import SchedulerWidget

class MpcApp(App):

	def build(self):
		self.updateConfig()
		sm=ScreenManager()
		sm.transition=NoTransition()
		sm.add_widget(PlayerWidget(name="player"))
		sm.add_widget(PlaylistWidget(name="playlist"))
		sm.add_widget(LibraryWidget(name="library"))
		sm.add_widget(SchedulerWidget(name="scheduler"))
		return sm
	def build_config(self,config):
		config.setdefaults("Connection",{"host":"localhost","port":6600})
	def build_settings(self,settings):
		settings.add_json_panel("Connection", self.config, "connectionSettings.json")
	def close_settings(self,settings=None):
		self.updateConfig()
		super(MpcApp,self).close_settings(settings)
	def updateConfig(self):
		host=self.config.get("Connection","host")
		port=self.config.get("Connection","port")
		iFace.setConnectionSettings(host,port)


if __name__ == '__main__':
	app=MpcApp()
	app.run()
