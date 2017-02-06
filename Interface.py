from mpd import MPDClient, MPDError, ConnectionError
from select import select

client=MPDClient()
connected=False
state=None

def end_idle():
	canRead=select([client],[],[],0)[0]

	if(canRead):
		return client.fetch_idle()
	else:
		client.noidle()
		return None
def connect():
	global connected
	if not connected:
		try:
			client.connect("localhost",6600)
			client.send_idle()
			connected=True
		except MPDError as e:
			print("MPDError: "+str(e))
		except Exception as e:
			print("Exception: "+str(e))

def disconnect():
	global connected
	try:
		connected=False
		client.disconnect()
	except MPDError as e:
		print("MPDError: "+str(e))
	except Exception as e:
		print("Exception: "+str(e))

def update():
	connect()

	try:
		ret=end_idle()
		client.send_idle()
		return ret
	except ConnectionError as e:
		disconnect()
	except MPDError as e:
		print("MPDError: "+str(e))
	except Exception as e:
		print("Exception: "+str(e))
		disconnect()
	return None

def _command(command):
	ret=None
	try:
		end_idle()
		try:
			ret=command(client)
		except MPDError as e:
			print("Command failed: "+str(e))
		client.send_idle()
	except ConnectionError as e:
		disconnect()
	except MPDError as e:
		print("MPDError: "+str(e))
	except Exception as e:
		print("Exception: "+str(e))
		disconnect()
	return ret

def currentsong():
	return _command(MPDClient.currentsong)

def playlist():
	return _command(MPDClient.playlistinfo)

def play():
	return _command(MPDClient.play)

def toggle():
	if(state and state in ["play"]):
		_command(MPDClient.pause)
	else:
		_command(MPDClient.play)

def status():
	global state
	s=_command(MPDClient.status)
	if "state" in s:
		state=s["state"]
	return s

def next():
	return _command(MPDClient.next)

def prev():
	return _command(MPDClient.previous)

def close():
	end_idle()
	client.close()

