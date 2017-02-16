from mpd import MPDClient, MPDError, ConnectionError
from select import select
from kivy.event import EventDispatcher
from kivy.properties import StringProperty,NumericProperty,OptionProperty,ListProperty
from kivy.clock import Clock
import threading
import time

class InterfaceWorker():
	host=""
	port=0

	status={}
	currentsong={}
	connectionChange=False
	queue=[]
	connected=False
	dataTime=0
	playlist=[]
	playlistId=0

	def __init__(self,host,port):
		self.host=host
		self.port=port
		self.client=MPDClient()
		self.thread=threading.Thread(target=self.loop,args=())
		self.thread.daemon=True
		self.cmdLock=threading.Lock()
		self.dataLock=threading.Lock()
		self.runLock=threading.Lock()
		self.thread.start()
	def _connect(self):
		while not self.connected and self.runLock.acquire(False):
			self.runLock.release()
			try:
				self.client.connect(self.host,self.port)
				self.connected=True
				print("Connection to "+self.host+" on port "+str(self.port)+" established.")
			except MPDError as e:
				print("_connect: MPDError: "+str(e))
				time.sleep(5)
			except Exception as e:
				print("_connect: Exception: "+str(e))
				time.sleep(5)
	def _disconnect(self):
		try:
			self.connected=False
			self.client.disconnect()
			self.status={}
			self.currentsong={}
			self.queue=[]
			self.dataTime=0
			print("Connection closed.")
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
				for (cmd,args) in queue:
					try:
						cmd(self.client,*args)
					except MPDError as e:
						print("MPDError:",e)
				self._statusUpdate()
				self.client.send_idle()
		except ConnectionError as e:
			self._disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
	def _statusUpdate(self):
		print("Updating status")
		try:
			status=self.client.status()
			currentsong=self.client.currentsong()
			playlistId=status.get("playlist",0)

			self.dataLock.acquire()
			self.currentsong=currentsong
			self.status=status
			self.dataTime=time.time()

			newPlaylist=(self.playlistId != playlistId)
			self.playlistId=playlistId
			self.dataLock.release()

			if(newPlaylist):
				self._playlistUpdate()
		except ConnectionError as e:
			self._disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
	def _playlistUpdate(self):
		print("Updating playlist")
		try:
			playlist=self.client.playlistinfo()
			self.dataLock.acquire()
			self.playlist=playlist
			self.dataLock.release()
		except ConnectionError as e:
			self._disconnect()
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))
	def _update(self):
		canRead=select([self.client],[],[],0)[0]
		if(canRead):
			try:
				updates=self.client.fetch_idle()
				if updates:
					print(updates)
					self._statusUpdate()
				self.client.send_idle()
			except ConnectionError as e:
				self._disconnect()
			except MPDError as e:
				print("MPDError: "+str(e))
			except Exception as e:
				print("Exception: "+str(e))
	def loop(self):
		while(self.runLock.acquire(False)):
			self.runLock.release()
			self._connect()
			self._statusUpdate()
			self._playlistUpdate()
			try:
				self.client.send_idle()
			except ConnectionError as e:
				self._disconnect()
			except MPDError as e:
				print("MPDError: "+str(e))
			except Exception as e:
				print("Exception: "+str(e))

			while(self.connected and self.runLock.acquire(False)):
				self.runLock.release()
				self._handleQueue()
				self._update()
				time.sleep(.1)
		self._disconnect()
	def stop(self):
		self.runLock.acquire()
	def command(self,cmd,args=()):
		self.cmdLock.acquire()
		self.queue.append((cmd,args))
		self.cmdLock.release()
	def getData(self):
		self.dataLock.acquire()
		retn={"status":self.status,
		"currentsong":self.currentsong,
		"dataTime":self.dataTime,
		"playlist":self.playlist
		}
		self.dataLock.release()
		return retn

class KivyInterface(EventDispatcher):
	artist=StringProperty("")
	title=StringProperty("")
	elapsed=NumericProperty(0)
	duration=NumericProperty(0)
	state=StringProperty("")
	port=NumericProperty(6600)
	host=StringProperty()
	playlist=ListProperty()
	currentId=NumericProperty(0)
	worker=None

	def __init__(self,**kwargs):
		self.clock=Clock.schedule_interval(self.update,.1)
		super(KivyInterface,self).__init__(**kwargs)

	def setConnectionSettings(self,host,port):
		if(int(port)!=self.port or host!=str(self.host)):
			self.host=host
			self.port=int(port)
			
			if self.worker:
				self.worker.stop()
			self.worker=InterfaceWorker(host,port)
	def update(self,dt):
		if(self.worker):
			data=self.worker.getData()
			
			status=data["status"]
			currentsong=data["currentsong"]
			dataTime=data["dataTime"]

			self.playlist=data["playlist"]

			self.state=status.get("state","Error")
			self.artist=currentsong.get("artist","Artist")
			self.title=currentsong.get("title",currentsong.get("file","Title"))
			self.elapsed=float(status.get("elapsed","0"))
			self.duration=float(currentsong.get("time","0"))
			self.currentId=int(status.get("songid",-1))
			if(self.state=="play"):
				self.elapsed+=time.time()-dataTime
	def play(self):
		if self.worker:
			self.worker.command(MPDClient.play)
	def toggle(self):
		if(self.worker and self.state):
			if(self.state=="play"):
				self.worker.command(MPDClient.pause)
			else:
				self.worker.command(MPDClient.play)
	def next(self):
		if self.worker:
			return self.worker.command(MPDClient.next)
	def prev(self):
		if self.worker:
			return self.worker.command(MPDClient.previous)
	def stop(self):
		if self.worker:
			return self.worker.command(MPDClient.stop)
	def playid(self,index):
		if self.worker:
			return self.worker.command(MPDClient.playid,(index,))
	def deleteid(self,index):
		if self.worker:
			return self.worker.command(MPDClient.deleteid,(index,))
		

iFace=KivyInterface()
