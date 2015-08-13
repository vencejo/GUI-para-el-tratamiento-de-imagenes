from Tkinter import *
from tkColorChooser import askcolor
from tkMessageBox import *
import ImageTk
from imagen.tratamientoImagen import ImagenTratada
from imagen.ajustes import Ajustes , cargaAjustes


class GUI(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.nivelR = IntVar()
		self.nivelR.set(125)
		self.nivelG = IntVar() 
		self.nivelG.set(125)
		self.nivelB = IntVar()
		self.nivelB.set(125)
		self.ajustes = Ajustes()
		self.imagenTratada = ImagenTratada()
		self.creaElementos()
		self.iniciaAjustesyVisoresImagenes()
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
		miniMenu.add_command(label='Abrir...', command=self.cargaAjustes)
		miniMenu.add_command(label='Guardar...', command=self.guardaAjustes)
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
	
	def guardaAjustes(self):
		self.ajustes.guardaAjustes('ajustes.json')
	
	def cargaAjustes(self):	
		self.ajustes = cargaAjustes('ajustes.json')
		self.actualizaControlesSegunAjustes()
		
	def actualizaControlesSegunAjustes(self):
		self.nivelR.set(self.ajustes.r)
		self.nivelG.set(self.ajustes.g)
		self.nivelB.set(self.ajustes.b)
		self.nivelBinarizado.set(self.ajustes.umbralBinarizado)
		self.areaMin.set(self.ajustes.areaMin)
		self.areaMax.set(self.ajustes.areaMax)
		self.toleranciaWH.set(self.ajustes.toleranciaWH)
		self.desviacionD.set(self.ajustes.desviacionD)
		self.toleranciaLP.set(self.ajustes.toleranciaLP)
		self.visorColor.config(  bg= self.conversorRGBaHEX() )
	
	def conversorRGBaHEX(self):
		rgb = (self.nivelR.get(),self.nivelG.get(),self.nivelB.get())
		return '#' + "".join(map(chr, rgb)).encode('hex')
			
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
		self.visorImagenOriginal = Label(frame)
		self.visorImagenOriginal.pack(side=LEFT)
		
	def creaVisorImagenTratada(self, frame):
		self.visorImagenTratada = Label(frame)
		self.visorImagenTratada.pack(side=TOP)
		
	def creaVisorImagenBlobs(self, frame):
		self.visorImagenBlobs = Label(frame)
		self.visorImagenBlobs.pack(side=RIGHT)
		
	def creaAreaControlesImagenOriginal(self):
		self.areaControlesImg = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesImg.pack(side=LEFT, fill=X)
		self.creaAreaSeleccionColor(self.areaControlesImg)
		self.ponerSeparadores(self.areaControlesImg, 2)
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
	  
	def creaAreaSeleccionColor(self,frame):
		self.areaSeleccionColor = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaSeleccionColor.pack(side=TOP, fill=X)
		self.creaSelectorColor(self.areaSeleccionColor)
		self.creaVisorColor(self.areaSeleccionColor)
	
	def creaVisorColor(self,frame):
		self.visorColor = Label(frame, bg="#000000")
		self.visorColor.pack(side=RIGHT, expand=YES, fill=X)
		self.visorColor.bind('<Button-1>', self.preguntandoElColor)
	
	def actualizaVisorColor(self):
		self.visorColor.config(  bg=self.color[1] )
	
	def preguntandoElColor(self, event):
		self.preguntaElColor()
		
	def preguntaElColor(self):
		colorDevuelto = askcolor(color="#000000", title="Selector de color")
		
		if colorDevuelto[0] is not None:
			self.color = colorDevuelto		 
			self.nivelR.set(self.color[0][0])
			self.nivelG.set(self.color[0][1])
			self.nivelB.set(self.color[0][2])
			self.actualizaVisorColor()
			
	def creaSelectorColor(self, frame):
	   
		self.selectorColor = Button(frame, text = 'Selector Color ',
											command=self.preguntaElColor)
		self.selectorColor.pack(side=LEFT)
		
	
		     
	def creaDeslizableBinarizado(self, frame):
		self.nivelBinarizado = IntVar()
		self.deslizableBinarizado = Scale(frame, label = 'Binarizado ',
											variable=self.nivelBinarizado,
											from_=0, to=255,
											tickinterval=40,
											resolution=1,
											orient='horizontal',
											length=320)
		self.deslizableBinarizado.pack()
		self.nivelBinarizado.set(180)
		
		
	def creaDeslizablesArea(self, frame):
		self.areaMin = IntVar()
		self.areaMax = IntVar()
		self.deslizableAreaMin = Scale(frame, label = 'Area Minima ',
											variable=self.areaMin,
											from_=0, to=3500,
											tickinterval=500,
											resolution=20,
											orient='horizontal',
											length=320)
		self.deslizableAreaMin.pack()
		self.areaMin.set(100)
		
		self.deslizableAreaMax = Scale(frame, label = 'Area Maxima ',
											variable=self.areaMax,
											from_=0, to=3500,
											tickinterval=500,
											resolution=20,
											orient='horizontal',
											length=320)
		self.deslizableAreaMax.pack()
		self.areaMax.set(1000)
		
		
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
		self.toleranciaWH.set(0.15)
		
		self.deslizableDesviacionD = Scale(frame, label = 'desviacionD ',
											variable=self.desviacionD,
											from_=0, to=1,
											resolution=0.05,
											orient='horizontal',
											length=320)
		self.deslizableDesviacionD.pack()
		self.desviacionD.set(0.25)
	
		self.deslizableToleranciaLP = Scale(frame, label = 'toleranciaLP ',
											variable=self.toleranciaLP,
											from_=0, to=1,
											resolution=0.05,
											orient='horizontal',
											length=320)
		self.deslizableToleranciaLP.pack()
		self.toleranciaLP.set(0.15)
		
	def creaSelectorVisualizacion(self, frame):
		self.tipoVisualizacion = StringVar()
		self.selectorVisualizacionNada = Radiobutton(frame, 
												 text= 'Ver Nada',
												 variable=self.tipoVisualizacion,
												 value='nada')
		self.selectorVisualizacionNada.pack(anchor=NW) 
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
	
		
	def iniciaAjustesyVisoresImagenes(self):
		
		self.actualizaAjustes()
		
	# ------------------------------------------------------------------
	# Ejecucion en ciclica de las siguientes funciones
	
	# actualizaAjustes ->
	# actualizaVisorImagenOriginal ->
	# actualizaVisorImagenTratada ->
	# actualizaVisorImagenBlobs ->
	# actualizaAjustes -> etc ...
	# ------------------------------------------------------------------
	
	def actualizaAjustes(self):
		
		self.ajustes.actualizaAjustes(self.nivelR.get(),
									  self.nivelG.get() , 
									  self.nivelB.get(), 
									  self.nivelBinarizado.get(), 
									  self.areaMin.get(), 
									  self.areaMax.get(), 
									  self.toleranciaWH.get(), 
									  self.desviacionD.get(),
									  self.toleranciaLP.get() )
							 
		self.actualizaVisorImagenOriginal()
			
	def actualizaVisorImagenOriginal(self):
		img = self.imagenTratada.capturaImagen()
		photo = ImageTk.PhotoImage(img.getPIL())
		self.visorImagenOriginal.photo = photo
		self.visorImagenOriginal.configure(image=photo)
		self.visorImagenOriginal.after(10, self.actualizaVisorImagenTratada)
		
	def actualizaVisorImagenTratada(self):
		img = self.imagenTratada.capturaYTrataLaImagen(self.nivelR.get(), 
												  self.nivelG.get(),
												  self.nivelB.get(),
												  self.nivelBinarizado.get()
												  )
		photo = ImageTk.PhotoImage(img.getPIL())
		self.visorImagenTratada.photo = photo
		self.visorImagenTratada.configure(image=photo)
		self.visorImagenTratada.after(10, self.actualizaVisorImagenBlobs)
		
	def actualizaVisorImagenBlobs(self):
	  
		## print self.toleranciaWH.get(), self.desviacionD.get(), self.toleranciaLP.get()                    
		img = self.imagenTratada.encuentraYFiltraBlobs(self.areaMin.get(),
												  self.areaMax.get(),
												  self.toleranciaWH.get(), 
												  self.desviacionD.get(),
												  self.toleranciaLP.get(),
												  self.tipoVisualizacion.get())
		photo = ImageTk.PhotoImage(img.getPIL())
		self.visorImagenBlobs.photo = photo
		self.visorImagenBlobs.configure(image=photo)
		self.visorImagenBlobs.after(10, self.actualizaAjustes())
		
	# ------------------------------------------------------------------
	# Fin de un ciclo de ejecion
	# ------------------------------------------------------------------
		
	def ponerSeparadores(self, frame, num):
		for i in range(num):
			Label(frame, text = "                             ").pack(side=TOP, 
																	  expand=YES, 
																	  fill=X)
		
		
if __name__ == '__main__':
    
    GUI().mainloop()
        
