from mpd import MPDClient, MPDError, ConnectionError
from select import select
from kivy.event import EventDispatcher
from kivy.properties import StringProperty,NumericProperty

class Interface(EventDispatcher):
	artist=StringProperty("")
	title=StringProperty("")
	elapsed=NumericProperty(0)
	duration=NumericProperty(1)
	state=StringProperty("")
	
	
	def __init__(self):
		self.client=MPDClient()
		self.connected=False
		self.status=None
		self.host="localhost"
		self.port=6600
	def _end_idle(self):
		canRead=select([self.client],[],[],0)[0]

		if(canRead):
			return self.client.fetch_idle()
		else:
			self.client.noidle()
			return None
	def connect(self):
		if not self.connected:
			try:
				self.client.connect(self.host,self.port)
				self.connected=True
				self._fetch()
				self.client.send_idle()
			except MPDError as e:
				print("MPDError: "+str(e))
			except Exception as e:
				print("Exception: "+str(e))

	def disconnect(self):
		try:
			self.connected=False
			self.client.disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
	def _fetch(self):
		print("fetch")
		status=self.client.status()
		if(status):
			print("status")
			self.duration=float(status.get("duration","1"))
			self.elapsed=float(status.get("elapsed","0"))
			self.state=status.get("state","")

		current=self.client.currentsong()
		if current:
			print("current")
			self.artist=current.get("artist","")
			self.title=current.get("title","")
	def update(self):
		self.connect()
		try:
			ret=self._end_idle()

			if ret:
				self._fetch()
			self.client.send_idle()
		except ConnectionError as e:
			self.disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
			self.disconnect()
		return None
	def _command(self,command):
		ret=None
		try:
			self._end_idle()
			try:
				ret=command(self.client)
			except MPDError as e:
				print("Command failed: "+str(e))
			self.client.send_idle()
		except ConnectionError as e:
			self.disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
			self.disconnect()
		return ret
	def play(self):
		return self._command(MPDClient.play)

	def toggle(self):
		if(self.state):
			if(self.state=="play"):
				self._command(MPDClient.pause)
			else:
				self._command(MPDClient.play)
	def next(self):
		return self._command(MPDClient.next)
	def prev(self):
		return self._command(MPDClient.previous)

iFace=Interface()
