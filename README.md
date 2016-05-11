Flightaware tracelog to gpx

開圖狗

 Use wget to get tracklog
 e.g.
	wget http://flightaware.com/live/flight/EVA7/history/20160508/0800Z/KSFO/RCTP/tracklog
 To generate gpx file
 set use_gpx = True to generate gpx file
 e.g 
	python toGPX.py tracklog > output.gpx 
 if use_gpx = False
 e.g 
	python toGPX.py tracklog > output.html
