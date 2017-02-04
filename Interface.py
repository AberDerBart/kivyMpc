from mpd import MPDClient, MPDError
import threading
from select import select

client=MPDClient()
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

def _command(command):
	ret=None
	try:
		end_idle()
		ret=command(client)
		client.send_idle()
	except MPDError as e:
		print("Error: "+str(e))
		
	return ret
def currentsong():
	return _command(MPDClient.currentsong)

def play():
	return _command(MPDClient.play)

def status():
	return _command(MPDClient.status)

def next():
	return _command(MPDClient.next)

def prev():
	return _command(MPDClient.previous)

def close():
	end_idle()
	client.close()

