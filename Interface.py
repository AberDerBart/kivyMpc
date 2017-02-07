from mpd import MPDClient, MPDError, ConnectionError
from select import select
from kivy.event import EventDispatcher
from kivy.properties import StringProperty,NumericProperty,OptionProperty
import threading

class Interface(EventDispatcher):
	artist=StringProperty("")
	title=StringProperty("")
	elapsed=NumericProperty(0)
	duration=NumericProperty(1)
	state=StringProperty("")
	port=NumericProperty(6600)
	host=StringProperty("localhost")

	connectionState=OptionProperty("disconnected", options=["disconnected","connecting","connected"])
	
	def __init__(self):
		self.client=MPDClient()
		self.thread=None
		self.connected=True
		self.status=None
		self.propLock=threading.Lock()
	def _end_idle(self):
		canRead=select([self.client],[],[],0)[0]

		if(canRead):
			return self.client.fetch_idle()
		else:
			self.client.noidle()
			return None
	def connect(self):
		if(self.connectionState=="disconnected"):
			if (not self.thread) or (not self.thread.is_alive()):
				self.thread=threading.Thread(target=self._connect,args=())
				self.connectionState="connecting"
				self.thread.start()
		elif(self.connectionState=="connecting"):
			if(self.thread and not self.thread.is_alive()):
				self.connectionState="connected"
	def _connect(self):
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
		status=self.client.status()
		if(status):
			self.duration=float(status.get("duration","1"))
			self.elapsed=float(status.get("elapsed","0"))
			self.state=status.get("state","")

		current=self.client.currentsong()
		if current:
			self.artist=current.get("artist","")
			self.title=current.get("title","")
	def update(self,dt):
		self.connect()
		try:
			ret=self._end_idle()

			if ret:
				print(str(ret))
				self._fetch()
			self.client.send_idle()
		except ConnectionError as e:
			self.disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
			self.disconnect()
		if(self.state=="play"):
			self.elapsed+=dt
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
