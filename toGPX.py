# Flightaware tracklog to gpx
# use wget to get tracklog
# http://flightaware.com/live/flight/EVA7/history/20160508/0800Z/KSFO/RCTP/tracklog
# python toGPX tracklog > output.gpx 
import sys
from bs4 import BeautifulSoup
import codecs

step = 10000.0

def parse_gps_position(sp, name):
	data = []
	result1 = sp.find_all(lambda tag: tag.name == 'tr' and tag.get('class') ==  [name])
	if result1 == None:
		f.close()
		return	
	for ele in result1:
		tr_ary = ele.find_all('td')
		count = 0
		for td_ele in tr_ary:
			count += 1
			if count <= 3:
				data.append(td_ele.contents[0])
	return data

def plot2gpx(x, y):
	#pass
	#print("      <trkpt lat=\"" + str(float(y/step)) + "\" lon=\"" + str(float(x/step)) + "\"></trkpt>")
	print('      <trkpt lat="{0}" lon="{1}"></trkpt>'.format(float(y/step), float(x/step)))

def plot2svg(x, y):
	print('<circle cx="{0}" cy="{1}" r="10000" stroke="black" stroke-width"500" fill="red" />'.format(x, y))

def bresenham_line(x0, y0, x1, y1, flag):
	#print('draw ({0}, {1}) to ({2}, {3})'.format(x0, y0, x1, y1)) 
	steep = abs(y1- y0) > abs(x1 -x0)
	if steep:
		# swap x0 y0
		x0, y0 = y0, x0
		# swap x1 y1
		x1, y1 = y1, x1
	if x0 > x1:
		# swap x0 x1
		x0, x1 = x1, x0
		# swap y0 y1
		y0, y1 = y1, y0
	deltax = x1 - x0
	deltay = abs(y1 - y0)
	error = deltax / 2
	y = y0
	ystep = -1
	if y0 < y1:
		ystep = 1
	#print('x0={0}, x1={1}'.format(x0, x1)) 
	for x in range(x0, x1):
		if steep:
			#print('x={0}, y={1}'.format(y, x)) 
			if flag:
				plot2gpx(y, x)
			else:
				plot2svg(y, x)
		else:
			#print('x={0}, y={1}'.format(x, y)) 
			if flag:
				plot2gpx(x, y)
			else:
				plot2svg(x, y)
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax

def gpx_lol(ary, enable_inter):
	print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
	print("<gpx>")
	print("  <trk><name>GG</name><src>tracelog to gps</src>")
	print("    <trkseg>")
	for i in range(0, len(ary) - 1):
		y0 = int(float(ary[i][1]) * step)
		x0 = int(float(ary[i][2]) * step)
		y1 = int(float(ary[i+1][1]) * step)
		x1 = int(float(ary[i+1][2]) * step)
	 	gg = int(180.0 * step)
		if (enable_inter):
			if x0 * x1 < 0 and x0 != x1:
				y2 = ((y1 - y0) * (x1 - 180) - (x1 - x0) * y1) / (x0 - x1)
				if x0 < 0:
					bresenham_line(x0, y0, int(-179.9999 * step), y2, True)
					bresenham_line(gg, y2, x1, y1, True)
				else:
					bresenham_line(x0, y0, gg, y2, True)
					bresenham_line(int(-179.9999 * step), y2, x1, y1, True)
			else:
				bresenham_line(x0, y0, x1, y1, True)
		else:
			plot2gpx(x0, y0)
	print("    </trkseg>")
	print("  </trk>")
	print("</gpx>")

def svg_lol(ary, minX, minY, maxX, maxY, enable_inter):
	print('<svg width="1920" height="1080" viewbox="{0} {1} {2} {3}">'.format(str(minX), str(minY), str(maxX-minX), str(maxY-minY)))
	for i in range(0, len(ary) - 1):
		y0 = int(float(ary[i][1]) * step)
		x0 = int(float(ary[i][2]) * step)
		y1 = int(float(ary[i+1][1]) * step)
		x1 = int(float(ary[i+1][2]) * step)
		if enable_inter:
			bresenham_line(x0, y0, x1, y1, False)
		else:
			plot2svg(x0, y0)
	print("</svg>")

def main(filename):
	f = codecs.open(filename, "r", "utf-8")
	if f == None:
		exit(0)
	content = f.read()
	soup = BeautifulSoup(content)

	data1 = parse_gps_position(soup, 'smallrow1')
	data2 = parse_gps_position(soup, 'smallrow2')

	data = data1 + data2
	ary = []
	minX = 99999999
	minY = 99999999
	maxX = -99999999
	maxY = -99999999

	for i in range(0, len(data), 3):
		tup = (str(data[i]), str(data[i+1]), str(data[i+2]))
		y = int(float(data[i+1]) * step)
		x = int(float(data[i+2]) * step)
		if x < minX:
			minX = x
		if y < minY:
			minY = y
		if x > maxX:
			maxX = x
		if y > maxY:
			maxY = y
		ary.append(tup)
	ary.sort()
	enable_inter = True
	gpx_lol(ary, enable_inter)
	#svg_lol(ary, minX, minY, maxX, maxY, False)

	f.close()

main(sys.argv[1])
