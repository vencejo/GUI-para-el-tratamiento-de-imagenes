from SimpleCV import Camera, Display, Image, ColorCurve, Color, cv2
import time
from math import sqrt, atan2, degrees, pi
import numpy as np
import time
import funcionesAuxiliares as aux


class ImagenTratada():
	
	def __init__(self):
		self.camara = Camera()
		self.rutaImagenOriginal = 'ImagenOriginal.jpg'
		self.rutaImagenReducida = 'imagenReducida.jpg'
		self.rutaImagenBlobs = 'imagenBlobs.jpg'
		self.rutaImagenTratada = 'imagenTratada.jpg'
		self.angulosHuesos = []		
		self.articulaciones = []	 
		self.AreaBlobs = []
 		self.tiempoTratamiento = 0
 		self.numBlobsCandidatosPorArea = 0
 		self.enDepuracion = False
		
	def capturaImagen(self):
		img = self.camara.getImage()
		img.save(self.rutaImagenOriginal)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
		imgReducida = img.resize(320, 240)
		imgReducida.save(self.rutaImagenReducida)
		return imgReducida

	def trataImagen(self,img, r, g, b, umbralBinarizado):
		
		inicio = time.time()
		
		img = Image(self.rutaImagenReducida)
		result = img.colorDistance((r, g, b)).invert()
		result = result.binarize(umbralBinarizado).invert()
		result.save(self.rutaImagenTratada)
		
		fin = time.time()
		self.tiempoTratamiento = fin - inicio
		#self.depuracion()
				
	def capturaYTrataLaImagen(self, r, g, b,umbralBinarizado):
		img = self.capturaImagen()
		self.trataImagen(img, r, g, b, umbralBinarizado)
		return Image(self.rutaImagenTratada)
		
	def encuentraYFiltraBlobs(self,areaMin, areaMax, 
								   toleranciaWH, desviacionD,
								   toleranciaLP, dibujarBlobs):
		
		imagenBlobs = Image(self.rutaImagenTratada).copy()
		blobs = imagenBlobs.findBlobs()
		
		if blobs:	
			
			blobs.image = imagenBlobs
			
			self.areaBlobs = blobs.area()
			blobs = self.filtroPorArea(blobs, areaMin, areaMax)
			self.numBlobsCandidatosPorArea = len(blobs)
			
			# Busca los blobs de forma circular , los blobs que pasan el filtro
			# se guardan en la lista self.articulaciones
			self.filtroPorForma(blobs, toleranciaWH, desviacionD,toleranciaLP)
			
			if dibujarBlobs:
				self.dibujaBlobs(blobs)
			else:
				self.dibujaEstructura(imagenBlobs)
		
		# La imagen tratada tiene que ser guardada porque sino no funciona
		# la integracion con Tkinter
		imagenBlobs.save(self.rutaImagenBlobs)
		return Image(self.rutaImagenBlobs)
		
	def filtroPorArea(self, blobs, areaMin, areaMax):
		return blobs.filter((blobs.area()> areaMin) & (blobs.area()< areaMax))
		
	def filtroPorForma(self, blobs, toleranciaWH, desviacionD,toleranciaLP ):
		""" Busca los blobs de forma circular , los blobs que pasan el filtro
		se guardan en la lista self.articulaciones"""
		#toleranciaWH = 0.10    # 0.25 Tolerancia para el 'AspectRadio' del blob
		#desviacionD  = 0.10    # 0.40 desviacion para la funcion interna circleDistance()
		#toleranciaLP = 0.10    # 0.30 Ratio entre la Longitud del circulo ideal y el Perimetro real del blob
		numero_Iteraciones = 2 
		
		self.articulaciones = []
		for blob in blobs:
			candidato = blob.blobMask()
			hayCirculo, errorCode = aux.esCirculo(candidato, toleranciaWH, toleranciaLP, desviacionD, numero_Iteraciones)
			if not hayCirculo and self.enDepuracion :
				print errorCode
			else:
				self.articulaciones.append((blob.x, blob.y))
	
	def dibujaBlobs(self,blobs):		
		for blob in blobs:
			blob.draw(width=4, color=Color.YELLOW)
			
	def dibujaEstructura(self, img):
		if self.articulaciones != []:
			self.articulaciones = aux.ordenaListaPorDistanciaApunto(self.articulaciones, [0,480])
			puntoInicial = self.articulaciones.pop()
			img.dl().circle(puntoInicial, 10, Color.BLUE, width=5)
			while self.articulaciones != []:
				p = self.articulaciones.pop()
				img.dl().line(puntoInicial, p, Color.BLUE, width=5)
				img.dl().circle(p, 10, Color.BLUE, width=5)
				img.applyLayers()
				self.angulosHuesos.append(aux.anguloLineaEntreDosPuntos(p, puntoInicial))
				puntoInicial = p	
		
	def depuracion(self):
		self.enDepuracion = True
		print " ---------------------"
		print "Areas: "
		print self.AreaBlobs  
		print "Numero de blobs candidatos por area: "
		print self.numBlobsCandidatosPorArea
		print "Tiempo de tratamiento de imagen: "
 		print self.tiempoTratamiento 
 		print "Numero Articulaciones detectadas: "
 		print len(self.articulaciones) 
		print " ---------------------"
		time.sleep(1)
		
if __name__ == '__main__':
	
	display = Display() 
	imgT = ImagenTratada()
	
	while not display.isDone():
		img = imgT.capturaYTrataLaImagen(150)
		img.save(display)

