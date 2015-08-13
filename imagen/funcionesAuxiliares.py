from math import sqrt, atan2, degrees, pi
from SimpleCV import Camera, Display, Image, ColorCurve, Color, cv2
from scipy import ndimage

def ordenaListaPorDistanciaApunto(listaPuntos, punto):
	listaPuntos.sort(key=lambda p: sqrt((p[0]-punto[0])**2 + (p[1]-punto[1])**2))
	return listaPuntos
	
def anguloLineaEntreDosPuntos(p1, p2):
	x1, y1 = p1[0], p1[1]
	x2, y2 = p2[0], p2[1]
	
	dx = x2 - x1
	dy = y2 - y1
	
	rads = atan2(-dy, dx)
	rads %= 2*pi
	degs = degrees(rads)
	return degs
	
def esCirculo(fichero, toleranciaWH, toleranciaLP, desviacionD, iteraciones = 1):

    '''
    ** fichero: Nombre del fichero que contiene un blob unico en
        blanco sobre negro para el que hacer la comprobacion.

    ** toleranciaWH: Ratio de los valores Alto y Ancho del blob.
       toleranciaLP: ratio entre la longitud del circulo ideal y el
       perimetro real del blob

    ** desviacionD: Desviacion del circulo ideal. (funcion interna)

    ** iteraciones: numero de busquedas sobre un mismo objeto
       para mejorar la deteccion de falsos positivos
       El parametro puede tomar valores entre 0 y 3.
       Valores mayores de 3 no producen error en la funcion,
       pero enlentecen el proceso  y no mejora en nada la deteccion.
    '''
    
    i = 0
    imgObj = fichero
    anguloRotacion = 15
    if iteraciones > 0:
        anguloRotacion = int(45/iteraciones)

    while i <= (iteraciones):
        bb = imgObj.findBlobs()
        if bb == None:
            return (False, 'None ')
        b = bb[-1]
        aspectRadio = float(b.height())/ float(b.width())
        if aspectRadio > (1 + toleranciaWH) or aspectRadio < (1 - toleranciaWH):
            if aspectRadio > 1:
                aspectRadio -= 1
            else:
                aspectRadio = 1 - aspectRadio
            return (False,'WH ' + str(aspectRadio)[:4])
        if b.circleDistance() > desviacionD:
            return(False,'D ' + str(b.circleDistance())[:4])

        # longitudIdeal: Longitud que tendria el perimetro del objeto
        # si fuese una circunferencia de radio el radio medio devuelto
        # por blob.radius()
        longitudIdeal = 2 * 3.1415627 * b.radius()

        perimetro = b.perimeter() #perimetro real del blob detestado
        ratioLP = float(longitudIdeal / perimetro)
        if ratioLP > (1 + toleranciaLP) or ratioLP < (1 - toleranciaLP):
            if ratioLP > 1:
                ratioLP -= 1
            else:
                ratioLP = 1 - ratioLP
            return (False, 'LP ' + str(ratioLP)[:4])
        
        imgObj = rotarBlob_RAM(imgObj, anguloRotacion)
        i += 1
    return (True,'OK')
# --------------------------------------------

def rotarBlob_RAM(imgOrigen, angulo_Rotacion):

    '''
    Realiza sobre el canvas de 'imgOrigen' una rotacion de
    un cierto numero de grados y lo devuelve una vez rotado.
    OpenCV = ficheroSimpleCV.getNumpyCv2()
    ficheroSimpleCV = Image(OpenCV,cv2image=True)
    '''
    
    OpenCV = imgOrigen.getNumpyCv2()
    OpenCV = ndimage.rotate(OpenCV, angulo_Rotacion)
    ficheroSimpleCV = Image(OpenCV,cv2image=True)
    return(ficheroSimpleCV)
	
