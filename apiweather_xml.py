import requests
from lxml import etree
from jinja2 import Template
import webbrowser


def orientacion (direccion):
	if (direccion > 337.5 and direccion <= 360) or (direccion >= 0 and direccion < 22.5):
		return 'N'
	if direccion >= 22.5 and direccion <= 67.5:
		return 'NE'
	if direccion > 67.5 and direccion < 112.5:
		return 'E'
	if direccion >= 112.5 and direccion <= 157.5:
		return 'SE'
	if direccion > 157.5 and direccion < 202.5:
		return 'S'
	if direccion >= 202.5 and direccion <= 247.5:
		return 'SO'
	if direccion > 247.5 and direccion < 292.5:
		return 'O'
	if direccion >= 292.5 and direccion <= 337.5:
		return 'NO'


provincias = ['Almeria','Cadiz', 'Cordoba','Granada','Huelva','Jaen','Malaga','Sevilla']
plantilla = open('plantilla.html','r')
salidahtml = open('salidahtml.html','w')
html = ''
ltemp_min = []
ltemp_max = []
lviento = []
ldireccion = []
pais = 'es'
for linea in plantilla:
	html += linea

for provincia in provincias:
	dicc_params = {'q':provincia, 'mode':'xml', 'units':'metric', 'lang':'sp'}
	pronostico = requests.get(url='http://api.openweathermap.org/data/2.5/weather', params = dicc_params)
	pronostico = etree.fromstring(pronostico.text.encode("utf-8"))
	temp_min = pronostico.find("temperature")
	temp_min = int(float(temp_min.attrib["min"]))
	temp_max = pronostico.find("temperature")
	temp_max = int(float(temp_max.attrib["max"]))
	viento = pronostico.find("wind/speed")
	viento = viento.attrib["value"]
	direccion = pronostico.find("wind/direction")
	direccion = float(direccion.attrib["value"])
	direccion = orientacion(direccion)
	ltemp_min.append(temp_min)
	ltemp_max.append(temp_max)
	lviento.append(viento)
	ldireccion.append(direccion)

salida = Template(html)
salida = salida.render(provincias = provincias, temp_min = ltemp_min, temp_max = ltemp_max, viento = lviento, direccion = ldireccion)
salidahtml.write(salida)

webbrowser.open("salidahtml.html")