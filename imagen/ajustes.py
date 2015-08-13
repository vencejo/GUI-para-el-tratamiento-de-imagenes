import json


class Ajustes():
	""" En esta clase pondremos los ajustes realizados sobre la imagen 
	para poder detectar los blobs que nos interesan asi como tambien
	pondremos los metodos para guardar y cargar estos ajustes """
	
	def __init__(self):
		self.r = 127
		self.g = 127
		self.b = 127
		self.umbralBinarizado = 180
		self.areaMin = 100
		self.areaMax = 1000
		self.toleranciaWH = 0.20
		self.desviacionD = 1.0
		self.toleranciaLP = 0.20
		
	def actualizaAjustes(self, r, g , b, umbralBinarizado, 
							 areaMin, areaMax, toleranciaWH,
							 desviacionD, toleranciaLP ):
		self.r = r
		self.g = g
		self.b = b
		self.umbralBinarizado = umbralBinarizado
		self.areaMin = areaMin
		self.areaMax = areaMax
		self.toleranciaWH = toleranciaWH
		self.desviacionD = desviacionD
		self.toleranciaLP = toleranciaLP
		
	def guardaAjustes(self, nombreArchivo):
		datos = json.dumps(self, cls=CodificadorAjustes)
		with open(nombreArchivo, 'w') as archivoSalida:
			archivoSalida.write(datos)
			
	
def cargaAjustes(nombreArchivo):
	with open(nombreArchivo, 'r') as archivoEntrada:
			datos = archivoEntrada.read()
			ajustes = json.loads(datos, object_hook=decodificaAjustes)
	return ajustes
			
		
class CodificadorAjustes(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Ajustes):
			return {'r': str(obj.r), 
					'g': str(obj.g), 
					'b': str(obj.b), 
					'umbralBinarizado': str(obj.umbralBinarizado), 
					'areaMin': str(obj.areaMin), 
					'areaMax': str(obj.areaMax) ,
					'toleranciaWH': str(obj.toleranciaWH),
					'desviacionD': str(obj.desviacionD),
					'toleranciaLP': str(obj.toleranciaLP) }
		return super().default(obj)
		
def decodificaAjustes(dic):
	if dic.get('r'):
		ajustes = Ajustes()
		ajustes.actualizaAjustes( dic['r'], dic['g'] , dic['b'], 
								  dic['umbralBinarizado'], 
								  dic['areaMin'], dic['areaMax'], 
								  dic['toleranciaWH'],
								  dic['desviacionD'], 
								  dic['toleranciaLP'] )
		return ajustes
	else:
		return dic
