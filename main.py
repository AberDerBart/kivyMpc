import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition

from Player import PlayerWidget
from Interface import iFace

class MpdApp(App):

	def build(self):
		self.updateConfig()
		sm=ScreenManager()
		sm.transition=NoTransition()
		sm.add_widget(PlayerWidget(name="player"))
		return sm
	def build_config(self,config):
		config.setdefaults("Connection",{"host":"localhost","port":6600})
	def build_settings(self,settings):
		settings.add_json_panel("Connection", self.config, "connectionSettings.json")
	def close_settings(self,settings=None):
		self.updateConfig()
		super(MpdApp,self).close_settings(settings)
	def updateConfig(self):
		host=self.config.get("Connection","host")
		port=self.config.get("Connection","port")
		iFace.setConnectionSettings(host,port)


if __name__ == '__main__':
	app=MpdApp()
	app.run()
