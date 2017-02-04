import mpd
import threading
from select import select

client=mpd.MPDClient()
client.connect("localhost",6600)
lock=threading.Lock()
client.send_idle()

def end_idle():
	canRead=select([client],[],[],0)[0]

	if(canRead):
		return client.fetch_idle()
	else:
		client.noidle()
		return None

def update():
	ret=end_idle()
	client.send_idle()
	return ret

def play():
	end_idle()
	client.play()
	print("play")
	client.send_idle()
def next():
	end_idle()
	client.next()
	print("next")
	client.send_idle()
def prev():
	end_idle()
	client.previous()
	print("prev")
	client.send_idle()
def close():
	end_idle()
	client.close()

