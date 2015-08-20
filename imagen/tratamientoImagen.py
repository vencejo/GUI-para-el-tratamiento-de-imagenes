from SimpleCV import Camera, Display, Image, ColorCurve, Color, cv2
import time
from math import sqrt, atan2, degrees, pi
import numpy as np
import funcionesAuxiliares as aux
from ajustes import Ajustes 

class ImagenTratada():
	
	def __init__(self ):
		self.camara = Camera()
		self.archivoAjustesPorDefecto = '/home/cubie/Guhorus/Brazo mas Vision/GUI-para-el-control-visual-de-brazo-robotico/imagen/MisAjustes/ajustesBuenos.json'
		self.cargaAjustes()
		self.rutaImagenOriginal = 'imagen/imagenesGuardadas/ImagenOriginal.jpg'
		self.rutaImagenReducida = 'imagen/imagenesGuardadas/imagenReducida.jpg'
		self.rutaImagenBlobs = 'imagen/imagenesGuardadas/imagenBlobs.jpg'
		self.rutaImagenTratada_Fase1 = 'imagen/imagenesGuardadas/imagenTratada_fase1.jpg'
		self.rutaImagenTratada_Fase2 = 'imagen/imagenesGuardadas/imagenTratada_fase2.jpg'
		self.angulosHuesos = []		
		self.articulaciones = []
		self.blobsFiltradosPorForma = []
		self.todosLosCandidatos = []	 
		self.AreaBlobs = []
 		self.numBlobsCandidatosPorArea = 0
 		self.enDepuracion = False
 		
 	def cargaAjustes(self, archivo='/home/cubie/Guhorus/Brazo mas Vision/GUI-para-el-control-visual-de-brazo-robotico/imagen/MisAjustes/ajustesBuenos.json'):	
		self.ajustes = Ajustes()
		self.ajustes.cargaAjustes(archivo)
		
	def capturaImagen(self):
		img = self.camara.getImage()
		img.save(self.rutaImagenOriginal)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
		imgReducida = img.resize(320, 240)
		imgReducida.save(self.rutaImagenReducida)
		return imgReducida

	def trataImagen(self):
		
		img = Image(self.rutaImagenReducida)
		result = img.colorDistance((self.ajustes.r, self.ajustes.g, self.ajustes.b))
		result.save(self.rutaImagenTratada_Fase1) 
		result = result.invert()
		result = result.binarize(float(self.ajustes.umbralBinarizado)).invert()
		result.save(self.rutaImagenTratada_Fase2) 
		
		#self.depuracion()
				
	def capturaYTrataLaImagen(self):
		img = self.capturaImagen()
		self.trataImagen()
		return Image(self.rutaImagenTratada_Fase1)
		
	def encuentraYFiltraBlobs(self, tipoDibujo):
		
		imagenBlobs = Image(self.rutaImagenTratada_Fase2).copy()
		blobs = imagenBlobs.findBlobs()
		self.todosLosCandidatos = blobs
		
		if blobs != []:	
			
			blobs.image = imagenBlobs
			
			self.areaBlobs = blobs.area()
			blobs = self.filtroPorArea(blobs)
			self.numBlobsCandidatosPorArea = len(blobs)
			
			# Busca los blobs de forma circular , los blobs que pasan el filtro
			# se guardan en la lista self.articulaciones
			blobs = self.filtroPorForma(blobs)
			
			if tipoDibujo == 'blobs':
				self.dibujaBlobs(blobs)
			elif tipoDibujo == 'estructura':
				self.dibujaEstructura(imagenBlobs)
		
		# La imagen tratada tiene que ser guardada porque sino no funciona
		# la integracion con Tkinter
		imagenBlobs.save(self.rutaImagenBlobs)
		return Image(self.rutaImagenBlobs)
		
	def filtroPorArea(self, blobs):
		return blobs.filter((blobs.area()> self.ajustes.areaMin) & (blobs.area()< self.ajustes.areaMax))
		
	def filtroPorForma(self, blobs ):
		""" Busca los blobs de forma circular , los blobs que pasan el filtro
		se guardan en la lista self.articulaciones"""
		
		numero_Iteraciones = 2 
		
		self.articulaciones = []
                self.todosLosCandidatos = []
                self.blobsFiltradosPorForma = []
		for blob in blobs:
			candidato = blob.blobMask()
			hayCirculo, errorCode = aux.esCirculo(candidato, self.ajustes.toleranciaWH,
												  self.ajustes.toleranciaLP, 
												  self.ajustes.desviacionD, 
												  numero_Iteraciones)
                        self.todosLosCandidatos.append(blob)
			if not hayCirculo and self.enDepuracion :
				print errorCode
			if hayCirculo:
				self.articulaciones.append((blob.x, blob.y))
                self.blobsFiltradosPorForma.append(blob)
                
	def capturaTrataYFiltraBlobsDeImagen(self,tipoDibujo):
		img = self.capturaImagen()
		self.trataImagen()
		self.encuentraYFiltraBlobs(tipoDibujo)
		return Image(self.rutaImagenBlobs)
	
	def dibujaBlobs(self, blobs):
		if self.todosLosCandidatos:
				for blob in self.todosLosCandidatos:
						blob.draw(width=2, color=Color.YELLOW)
			
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

