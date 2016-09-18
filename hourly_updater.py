#script to read data from a serial port and push it to a preconfigured plotly graph 


import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

import datetime
import serial
import json
from time import time
from collections import deque, Counter

names = ["Tank", "In", "Out"]
key_map = {"Tank" : "tank", "In" : "fire->tank", "Out" : "tank->fire"}

slow_update_interval = 60*60
fast_update_interval = 60

fast_streams = {name : py.Stream(stream_id=token) for name,token in zip(names, secrets.fast_stream_ids)}

slow_streams = {name : py.Stream(stream_id=token) for name,token in zip(names, secrets.slow_stream_ids)}

port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

for s in fast_streams.values():
	s.open()


for s in slow_streams.values():
	s.open()

last_fast_update = time() - 55
last_slow_update = time() - (60*60 - 10)

fast_sums = Counter()
slow_sums = Counter()

fast_count = 0
slow_count = 0

while True:
	string = port.readline()
	try: 
		data = json.loads(string)
	except:
		continue


	fast_sums.update(data)
	slow_sums.update(data)

	fast_count += 1
	slow_count += 1

	if(time() - last_fast_update > fast_update_interval):
		x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
		for name, stream in fast_streams.items():
			av = fast_sums[key_map[name]] / fast_count
			stream.write(dict(x=x, y=av))

		fast_sums = Counter()
		last_fast_update = time()
		fast_count = 0
		print("updated fast streams at ", time())

	if(time() - last_slow_update > slow_update_interval):
		x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
		for name, stream in slow_streams.items():
			av = slow_sums[key_map[name]] / slow_count
			stream.write(dict(x=x, y=av))

		slow_sums = Counter()
		last_slow_update = time()
		slow_count = 0
		print("updated slow streams at ", time())





for s in fast_streams.values():
	s.close()

for s in slow_streams.values():
	s.close()
