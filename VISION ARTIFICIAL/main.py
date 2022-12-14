#importar paquetes necesarios
from imutils.video import VideoStream
from pyzbar import pyzbar
from pygame import mixer
import argparse
import datetime
import imutils
import time
import cv2
import pandas as pd

datos1 = {'Fecha':[]}
datos = {}

form =set()
used_codes = []
with open('barcodes.csv') as f:
    form = f.read().splitlines()
print(form)    

#used_codes = []




#construye nuestro parser de argumentos y hace el parseo de los argumentos
ap = argparse.ArgumentParser()
#ap.add_argument("-d", "--dataset", type=str, default="barcodes2.csv", help="path to output CSV file containing barcodes")
ap.add_argument("-o", "--output", type=str, default="barcodes.csv", help="path to output CSV file containing barcodes")


args = vars(ap.parse_args())

#inicializa el video y permite que el sensor de la camara comience a escanear
print ("[INFO] Iniciando video...")
# para webcam usa este>
#src=0 es la camara de la lap, src=1 es una webcam externa
vs = VideoStream(src=0).start()
#para camara de raspberri usa este otro>
#vs = VideoStream(usePiCamera=True).start()
time.sleep(0)

#abre un CSV para escribir la informacion de fecha y hora donde se detecta el codigo QR
csv = open(args["output"],"w")

datos1 = pd.read_csv('C:/Users/zaval/Desktop/Python Visual Code/barcodes2.csv', index_col=0)
datos1.to_csv('C:/Users/zaval/Desktop/Python Visual Code/barcodes.csv')
print(datos1.head())


#csv.write(used_codes)
#used_codes = []
#found = set()
#loop de frames del video
while True:
    #toma el cuadro(frame) del video y le cambia el tama;o a un maximo de 400 pixeles
    frame = vs.read()
    frame = imutils.resize(frame, width=1280, height=720)


    #Encuentra los barcodes o QR y los decodifica:
    barcodes = pyzbar.decode(frame)

#loop de los barcodes detectados
    for barcode in barcodes:
        #extrae los limites de la imagen del codigo de barras y crea una caja alrededor
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
        #los datos del codigo de barras estan en bytes, si queremos escribirlo en una imagen debemos convertirlo a string primero
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        
        

        #Si el texto de nuestro codigo de barras no esta en nuestro archivo CSV, escribe
        #la marca de tiempo + el barcode al disco y actualiza el set de datos.
        if barcodeData not in used_codes:
            #escribe los datos y el tipo de codigo de barras en la imagen
            text = "{} ({}) NO. CONTROL LEIDO".format(barcodeData, barcodeType)
            cv2.putText(frame, text, (x, y -10),

           cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,0),2)
            csv.write("{}, {}\n".format(datetime.datetime.now(),
                barcodeData))
            used_codes.append(barcodeData)
            time.sleep(0)

            #plays sound, la libreria playsound es incompatible con OPENCV porque opencv se detiene cuando hay un sonido
            #aunque se hagan threads.
            #playsound('notifa440.wav')

            #vamos a intentar con mixer *UPDATE* SI FUNCIONA y no se detiene el video.
            mixer.init()
            sound = mixer.Sound('notifa440.wav')
            sound.play()
            #cv2.waitKey(500)
            #limpia csv cuando vuelve a iniciar
            csv.flush()
            #found.add(barcodeData)
            #used_codes.add(barcodeData)

        elif barcodeData in used_codes:
            #csv.write("Ya esta el codigo")
            
            text1 = "CODIGO YA REGISTRADO"
            cv2.putText(frame, text1, (x, y -10),
            cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,0),2)
            time.sleep(0)

            mixer.init()
            sound = mixer.Sound('timbre_de_una_bici.wav')
            sound.play()
            
        else: 
            #escribe los datos de nuevo porque los alumnos pueden entrar mas de una vez a la biblioteca
            #if barcodeData in found:
                contador = 0
                while contador<=0:
                    csv.write("{},{}\n".format(datetime.datetime.now(),barcodeData))
                    mixer.init()
                    sound = mixer.Sound('notifa440.wav')
                    sound.play()
                    #cv2.waitKey(500)
                    contador += 1
                
                pass

            #break
            
        
        
        

        #muestra el cuadro de output
    cv2.imshow("BarcodeScanner", frame)

    key = cv2.waitKey(1) & 0xFF
    #waitkey originalmente ten??a valor =1
    

    #si la tecla 'q' se puls[o, break del loop
    if key == ord("q"):
        break
#cierra el archivo CSV de salida y hace limpieza
print("[INFO] limpiando...")


datos = pd.read_csv('C:/Users/Rogelio Ojeda/Desktop/Python Visual Code/barcodes.csv', index_col=0)
datos.to_csv('C:/Users/Rogelio Ojeda/Desktop/Python Visual Code/barcodes2.csv')
print(datos.head())

csv.close()
cv2.destroyAllWindows()
vs.stop()


