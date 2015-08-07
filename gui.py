from Tkinter import *
from tkMessageBox import *
import ImageTk
from vision.tratamientoImagen import ImagenTratada

imagenTratada = ImagenTratada()

class GUI(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.creaElementos()
		self.iniciaVisoresImagenes()
		self.master.title('Control Experimental Brazo Robotico')
		self.master.iconname('Brazo Robot')
			
	def creaElementos(self):
		self.creaBarraMenus()
		self.creaAreaVisores()
		self.creaAreaControlesImagenOriginal()
		self.creaAreaControlesImagenTratada()
		self.creaAreaControlesVisualizacion()
			
	def creaBarraMenus(self):
		self.menubar = Menu(self.master)
		self.master.config(menu=self.menubar)
		self.menuArchivo()
		self.menuEditar()
		self.menuImagen()
		
	def menuArchivo(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Abrir...', command=self.aunPorHacer)
		miniMenu.add_command(label='Guardar...', command=self.aunPorHacer)
		miniMenu.add_command(label='Salir...', command=self.quit)
		self.menubar.add_cascade(label='Archivo', underline=0, menu=miniMenu)
		
	def menuEditar(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Copiar...', command=self.aunPorHacer)
		miniMenu.add_command(label='Pegar...', command=self.aunPorHacer)
		self.menubar.add_cascade(label='Editar', underline=0, menu=miniMenu)
			
	def menuImagen(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Zoom +...', command=self.aunPorHacer)
		miniMenu.add_command(label='Zoom -...', command=self.aunPorHacer)
		miniMenu.add_command(label='Capturar Imagen...', command=self.quit)
		self.menubar.add_cascade(label='Imagen', underline=0, menu=miniMenu)
		
	def aunPorHacer(self):
		print "Funcion aun por implementar"
		
	def quit(self):
		if askyesno('Verificacion de Salida', 'Estas seguro de querer salir?'):
			Frame.quit(self)
			
	def creaAreaVisores(self):
		self.areaVisores = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaVisores.pack()
		self.creaVisorImagenOriginal(self.areaVisores )
		self.creaVisorImagenBlobs(self.areaVisores )
		self.creaVisorImagenTratada(self.areaVisores )
			
	def creaVisorImagenOriginal(self, frame):
		self.imagenOriginal = Label(frame)
		self.imagenOriginal.pack(side=LEFT)
		
	def creaVisorImagenTratada(self, frame):
		self.imagenTratada = Label(frame)
		self.imagenTratada.pack(side=TOP)
		
	def creaVisorImagenBlobs(self, frame):
		self.imagenBlobs = Label(frame)
		self.imagenBlobs.pack(side=RIGHT)
		
	def creaAreaControlesImagenOriginal(self):
		self.areaControlesImg = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesImg.pack(side=LEFT, fill=X)
		self.creaDeslizablesRGB(self.areaControlesImg)
		self.creaDeslizableBinarizado(self.areaControlesImg)
		
	def creaAreaControlesImagenTratada(self):
		self.areaControlesTratada = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesTratada.pack(side=RIGHT, fill=X)
		self.creaDeslizablesArea(self.areaControlesTratada)
		self.creaDeslizablesCirculo(self.areaControlesTratada)
		
	def creaAreaControlesVisualizacion(self):
		self.areaControlesTratada = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesTratada.pack(side=TOP, fill=X)
		self.creaSelectorVisualizacion(self.areaControlesTratada)
		
		
	def creaDeslizablesRGB(self, frame):
		self.nivelR = IntVar()
		self.nivelG = IntVar()
		self.nivelB = IntVar()
		self.deslizableR = Scale(frame, label = 'R ',
											variable=self.nivelR,
											from_=0, to=254,
											tickinterval=40,
											resolution=1,
											orient='horizontal',
											length=320)
		self.deslizableR.pack()
		self.nivelR.set(125)
		
		self.deslizableG = Scale(frame, label = 'G ',
											variable=self.nivelG,
											from_=0, to=254,
											tickinterval=40,
											resolution=1,
											orient='horizontal',
											length=320)
		self.deslizableG.pack()
		self.nivelG.set(125)
		
		self.deslizableB = Scale(frame, label = 'B ',
											variable=self.nivelB,
											from_=0, to=254,
											tickinterval=40,
											resolution=1,
											orient='horizontal',
											length=320)
		self.deslizableB.pack()
		self.nivelB.set(125)
		
	def creaDeslizableBinarizado(self, frame):
		self.nivelBinarizado = IntVar()
		self.deslizableBinarizado = Scale(frame, label = 'Binarizado ',
											variable=self.nivelBinarizado,
											from_=0, to=254,
											tickinterval=40,
											resolution=1,
											orient='horizontal',
											length=320)
		self.deslizableBinarizado.pack()
		self.nivelBinarizado.set(125)
		
		
	def creaDeslizablesArea(self, frame):
		self.areaMin = IntVar()
		self.areaMax = IntVar()
		self.deslizableAreaMin = Scale(frame, label = 'Area Minima ',
											variable=self.areaMin,
											from_=0, to=1000,
											tickinterval=250,
											resolution=20,
											orient='horizontal',
											length=320)
		self.deslizableAreaMin.pack()
		self.areaMin.set(100)
		
		self.deslizableAreaMax = Scale(frame, label = 'Area Maxima ',
											variable=self.areaMax,
											from_=0, to=1000,
											tickinterval=250,
											resolution=20,
											orient='horizontal',
											length=320)
		self.deslizableAreaMax.pack()
		self.areaMax.set(300)
		
		
	def creaDeslizablesCirculo(self, frame):
		self.toleranciaWH = DoubleVar()
		self.desviacionD = DoubleVar()
		self.toleranciaLP = DoubleVar()
		self.deslizableToleranciaWH = Scale(frame, label = 'toleranciaWH ',
											variable=self.toleranciaWH,
											from_=0, to=1,
											resolution=0.05,
											orient='horizontal',
											length=320)
		self.deslizableToleranciaWH.pack()
		
		self.deslizableDesviacionD = Scale(frame, label = 'desviacionD ',
											variable=self.desviacionD,
											from_=0, to=1,
											resolution=0.05,
											orient='horizontal',
											length=320)
		self.deslizableDesviacionD.pack()
		self.deslizableToleranciaLP = Scale(frame, label = 'toleranciaLP ',
											variable=self.toleranciaLP,
											from_=0, to=1,
											resolution=0.05,
											orient='horizontal',
											length=320)
		self.deslizableToleranciaLP.pack()
		
	def creaSelectorVisualizacion(self, frame):
		self.tipoVisualizacion = StringVar()
		self.selectorVisualizacionBlobs = Radiobutton(frame, 
												 text= 'Ver blobs',
												 variable=self.tipoVisualizacion,
												 value='blobs')
		self.selectorVisualizacionBlobs.pack(anchor=NW)	
		self.selectorVisualizacionEstructura = Radiobutton(frame, 
												 text= 'Ver Estructura',
												 variable=self.tipoVisualizacion,
												 value='estructura')
		self.selectorVisualizacionEstructura.pack(anchor=NW)										 
		self.tipoVisualizacion.set('blobs')
	
		
	def iniciaVisoresImagenes(self):
		self.actualizaVisorImagenOriginal()
		
	def actualizaVisorImagenOriginal(self):
		img = imagenTratada.capturaImagen()
		photo = ImageTk.PhotoImage(img.getPIL())
		self.imagenOriginal.photo = photo
		self.imagenOriginal.configure(image=photo)
		self.imagenOriginal.after(10, self.actualizaVisorImagenTratada)
		
	def actualizaVisorImagenTratada(self):
		img = imagenTratada.capturaYTrataLaImagen(self.nivelR.get(), 
												  self.nivelG.get(),
												  self.nivelB.get(),
												  self.nivelBinarizado.get()
												  )
		photo = ImageTk.PhotoImage(img.getPIL())
		self.imagenTratada.photo = photo
		self.imagenTratada.configure(image=photo)
		self.imagenTratada.after(10, self.actualizaVisorImagenBlobs)
		
	def actualizaVisorImagenBlobs(self):
		if self.tipoVisualizacion.get()  == 'blobs':
			verBlobs = True
		else:
			verBlobs = False
					
		img = imagenTratada.encuentraYFiltraBlobs(self.areaMin.get(),
												  self.areaMax.get(),
												  self.toleranciaWH.get(), 
												  self.desviacionD.get(),
												  self.toleranciaLP.get(),
												  verBlobs)
		photo = ImageTk.PhotoImage(img.getPIL())
		self.imagenBlobs.photo = photo
		self.imagenBlobs.configure(image=photo)
		self.imagenBlobs.after(10, self.actualizaVisorImagenOriginal)
		
		
if __name__ == '__main__':
	
	GUI().mainloop()
		