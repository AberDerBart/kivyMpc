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

		self._thread=None
		self._task=None
		self._task_reply=None
	def _exec_task(self,task):
		if not self._task_done():
			return False
		self._task=task
		self._thread=threading.Thread(target=self._task,args=())
		self._thread.start()
		return True
	def _task_done(self):
		if not self._thread:
			return True
		return not self._thread.is_alive()

	def _end_idle(self):
		canRead=select([self.client],[],[],0)[0]

		if(canRead):
			return self.client.fetch_idle()
		else:
			self.client.noidle()
			return None
	def connect(self):
		if(self.connectionState=="disconnected"):
			if self._task_done():
				self.connectionState="connecting"
				self._exec_task(self._connect)
		elif(self.connectionState=="connecting"):
			if(self._task_done()):
				if(self._task_reply):
					self.connectionState="connected"
				else:
					self.connectionState="disconnected"
	def _connect(self):
		self._task_reply=False
		try:
			self.client.connect(self.host,self.port)
			self._task_reply=True
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
