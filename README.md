# SkyToGo
# 死開圖狗

Flightaware tracelog to gpx

 Use wget to get tracklog

```
	wget http://flightaware.com/live/flight/EVA7/history/20160508/0800Z/KSFO/RCTP/tracklog
```
 To generate gpx file
 
 set use_gpx = True to generate gpx file
 
```
	python toGPX.py tracklog > output.gpx 
```

 if use_gpx = False (generate html, for debug)
 

```	
	python toGPX.py tracklog > output.html
```
