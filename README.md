# Temperature-logger
Hardware: an arduino with three temperature sensors connected to various places on hot water heater, a raspberry pi connected though a level converter to the arduino's serial port.

Software: an arduino sketch collects the data, displays it on an LCD display and does the conversion from resistance to temperature for the thermistors.

the raspberry pi reads data from the serial port and sends it to plotly, an online graphing service. 