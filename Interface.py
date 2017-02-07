from mpd import MPDClient, MPDError, ConnectionError
from select import select
from kivy.event import EventDispatcher
from kivy.properties import StringProperty,NumericProperty,OptionProperty
import threading

class InterfaceWorker():
	host="localhost"
	port=6600

	status={}
	currentsong={}

	def __init__(self):
		self.client=MPDClient()
		self.thread=threading.Thread(target=self.loop,args=())
		self.thread.daemon=True
		self.cmdLock=threading.Lock()
		self.dataLock=threading.Lock()
		self.connected=False
		self.queue=[]
		self.thread.start()
	def _connect(self):
		while not self.connected:
			try:
				self.dataLock.acquire()
				self.client.connect(self.host,self.port)
				self.connected=True
			except MPDError as e:
				print("MPDError: "+str(e))
			except Exception as e:
				print("Exception: "+str(e))
			self.dataLock.release()
	def _disconnect(self):
		try:
			self.connected=False
			self.client.disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
	def _handleQueue(self):
		try:
			#grab queue
			self.cmdLock.acquire()
			queue=self.queue
			self.queue=[]
			self.cmdLock.release()

			#process queue
			if len(queue)!=0:
				self.client.noidle()
				for cmd in queue:
					cmd(self.client)
				self._statusUpdate()
				self.client.send_idle()
		except ConnectionError as e:
			self._disconnect()
			self.connected=false
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
	def _statusUpdate(self):
		try:
			status=self.client.status()
			currentsong=self.client.currentsong()
			self.dataLock.acquire()
			self.currentsong=currentsong
			self.status=status
			self.dataLock.release()
		except ConnectionError as e:
			self._disconnect()
			self.connected=false
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
	def _update(self):
		canRead=select([self.client],[],[],0)[0]
		if(canRead):
			self.client.fetch_idle()
			self._statusUpdate()
			self.client.send_idle()
	def loop(self):
		while(True):
			self._connect()
			self._statusUpdate()
			self.client.send_idle()
			while(self.connected):
				self._handleQueue()
				self._update()
	def command(self,cmd):
		self.cmdLock.acquire()
		self.queue.append(cmd)
		self.cmdLock.release()
	def getData(self):
		self.dataLock.acquire()
		retn=(self.status,self.currentsong)
		self.dataLock.release()
		return retn

class KivyInterface(EventDispatcher):
	artist=StringProperty("")
	title=StringProperty("")
	elapsed=NumericProperty(0)
	duration=NumericProperty(0)
	state=StringProperty("")
	port=NumericProperty(6600)
	host=StringProperty("localhost")

	def __init__(self):
		self.worker=InterfaceWorker()
			
	def update(self,dt):
		(status,currentsong)=self.worker.getData()
		self.state=status.get("state","Error")
		self.artist=currentsong.get("artist","Artist")
		self.title=currentsong.get("title",currentsong.get("file","Title"))
	def play(self):
		return self.worker.command(MPDClient.play)

	def toggle(self):
		if(self.state):
			if(self.state=="play"):
				self.worker.command(MPDClient.pause)
			else:
				self.worker.command(MPDClient.play)
	def next(self):
		return self.worker.command(MPDClient.next)
	def prev(self):
		return self.worker.command(MPDClient.previous)

iFace=KivyInterface()
