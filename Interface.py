from mpd import MPDClient, MPDError, ConnectionError
from select import select
from kivy.event import EventDispatcher
from kivy.properties import StringProperty,NumericProperty,OptionProperty
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
				for cmd in queue:
					try:
						cmd(self.client)
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
		try:
			status=self.client.status()
			currentsong=self.client.currentsong()
			self.dataLock.acquire()
			self.currentsong=currentsong
			self.status=status
			self.dataTime=time.time()
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
				self.client.fetch_idle()
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
	def command(self,cmd):
		self.cmdLock.acquire()
		self.queue.append(cmd)
		self.cmdLock.release()
	def getData(self):
		self.dataLock.acquire()
		retn=(self.status,self.currentsong,self.dataTime)
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
	worker=None

	def setConnectionSettings(self,host,port):
		if(int(port)!=self.port or host!=str(self.host)):
			self.host=host
			self.port=int(port)
			
			if self.worker:
				self.worker.stop()
			self.worker=InterfaceWorker(host,port)
	def update(self,dt):
		if(self.worker):
			(status,currentsong,dataTime)=self.worker.getData()
			self.state=status.get("state","Error")
			self.artist=currentsong.get("artist","Artist")
			self.title=currentsong.get("title",currentsong.get("file","Title"))
			self.elapsed=float(status.get("elapsed","0"))
			self.duration=float(currentsong.get("time","0"))
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

iFace=KivyInterface()
