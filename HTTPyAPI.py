import requests
import json
import tkinter as tk
from PIL import ImageTk, Image

# Variables 
tamanioPantalla = {"width":360, "height":640}
listaDeAmiibos = []
listaDeImagenes = []
RangoInicialExtra = 0
RangoFinalExtra = 10


class amiibo:
    def __init__(self, nombrePersonaje, nombreAmiibo, seriePersonaje, serieAmiibo, fechaDeLanzamiento, imagen):
        self.nombrePersonaje = nombrePersonaje
        self.nombreAmiibo = nombreAmiibo
        self.seriePersonaje = seriePersonaje
        self.serieAmiibo = serieAmiibo
        self.fechaDeLanzamiento = fechaDeLanzamiento
        self.imagen = imagen


def ObtenerInformacionAMIIBO(URL, RangoInicio, RangoFinal):
    global listaDeAmiibos, listaDeImagenes
    response = requests.get(URL)

    if response.status_code == 200:
        payload = response.json() 
        Informacion = payload.get("amiibo")

        for i in range(RangoInicio, RangoFinal):
            Objeto = Informacion[i] # Obtener informacion de un amiibo  
            NombrePersonaje = Objeto["character"] # Obtener el Nombre
            NombreAmiibo = Objeto["name"] # Obtener el nombre registrado en el amiibo
            SeriePersonaje = Objeto["gameSeries"] # Obtener la serie del personaje
            SerieAmiibo = Objeto["amiiboSeries"] # Obtener la serie del amiibo
            fechasLanzamientos = Objeto["release"] # Acceder a todas las fechas registradas en el amiibo
            FechaDeLanzamiento = fechasLanzamientos["na"] # Obtener solamente la fecha de Norte America
            Imagen = Objeto["image"] # Obtener el url de la imagen del amiibo

            # Crear un objeto en base a toda la informacion recuperada
            AmiiboObjeto = amiibo(NombrePersonaje, NombreAmiibo, SeriePersonaje, SerieAmiibo, FechaDeLanzamiento, Imagen)
            listaDeAmiibos.append(AmiiboObjeto) # Agregar a mi Amiibo a mi lista de amiibos

        # Crear una imagen base la cual sera actualizada constantemente (El archivo se llama amiibo.jpg)
        RespuestaImagen = requests.get(listaDeAmiibos[0].imagen, stream=True)
        with open("Amiibo.jpg", "wb") as archivo:
            for chunk in RespuestaImagen.iter_content(1024):
                archivo.write(chunk)
        RespuestaImagen.close()

        
    else:
        print("Error: ")
        print(response.status_code)
ObtenerInformacionAMIIBO("https://www.amiiboapi.com/api/amiibo/", 0,10)


# Crear una ventana TK -----------------------------------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Amiibos")
ventana.minsize(tamanioPantalla["width"], tamanioPantalla["height"])
ventana.resizable(False, False)

# Imagenes -----------------------------------------------------------------------------------------------------
imagenGoLeft = ImageTk.PhotoImage(Image.open("LeftArrow.png").resize((40,40)))
imagenGoRight = ImageTk.PhotoImage(Image.open("RightArrow.png").resize((40,40)))
imagenConexion = ImageTk.PhotoImage(Image.open("Conexion.png").resize((19,15)))
imagenBateria = ImageTk.PhotoImage(Image.open("Battery.png").resize((15,15)))
imagenBoton = ImageTk.PhotoImage(Image.open("NintendoBlock.png").resize((40,40)))
ImagenAmiibo = ImageTk.PhotoImage(Image.open("Amiibo.jpg").resize((178,259)))

# Crear una funcion cuando se presione algun amiibo
def OnBottonClick(ID_AMIIBO):
    global ImagenAmiibo
    
    # canvas Header ------------------------------------------------------------------------------------------------
    seccionHeaderArchivos = tk.Canvas(master=ventana, bg="#009789", highlightthickness=0, height=56, width=360)
    seccionHeaderArchivos.place(x=0, y=24)

    # Crear boton para regresar a la pagina principal
    botonRegresar2 = tk.Button(master=ventana, bd=0, bg="#009789", image=imagenGoLeft, command=PaginaPrincipal)
    botonRegresar2.place(anchor=tk.CENTER, x=50, y=52)

    # Crear el texto del amiibo
    seccionHeaderArchivos.create_text(180,28, text=ID_AMIIBO.nombreAmiibo, font=("Roboto", 14), fill="white")

    # canvas MENU --------------------------------------------------------------------------------------------------
    seccionMenuArchivos = tk.Canvas(master=ventana, bg="#FFFFFF", highlightthickness=0, height=570, width=360)
    seccionMenuArchivos.place(x=0, y=80)


    # TODO LO QUE TIENE QUE VER CON LA IMAGEN 
    RespuestaImagen = requests.get(ID_AMIIBO.imagen, stream=True)
    with open("Amiibo.jpg", "wb") as archivo:
        for chunk in RespuestaImagen.iter_content(1024):
            archivo.write(chunk)
    RespuestaImagen.close()

    ImagenAmiibo = ImageTk.PhotoImage(Image.open("Amiibo.jpg").resize((178,259)))

    label = tk.Label(image=ImagenAmiibo, bg="#FFFFFF")
    label.image = ImagenAmiibo # keep a reference!
    label.place(anchor=tk.CENTER, x=180, y=240)


    stringNombre = "Nombre: " + ID_AMIIBO.nombrePersonaje
    stringSeriePersonaje = "Serie del personaje: " + ID_AMIIBO.seriePersonaje
    stringSerieAmiibo = "Serie del Amiibo: " + ID_AMIIBO.serieAmiibo
    stringFechaDeLanzamiento = "Fecha de lanzamiento: " + ID_AMIIBO.fechaDeLanzamiento

    seccionMenuArchivos.create_text(30,330, anchor=tk.W, font=("Roboto",12), text=stringNombre)
    seccionMenuArchivos.create_text(30,360, anchor=tk.W, font=("Roboto",12), text=stringSeriePersonaje)
    seccionMenuArchivos.create_text(30,390, anchor=tk.W, font=("Roboto",12), text=stringSerieAmiibo)
    seccionMenuArchivos.create_text(30,420, anchor=tk.W, font=("Roboto",12), text=stringFechaDeLanzamiento)
    





# Crear una funcion para mi pagina principal
def PaginaPrincipal():
    global listaDeAmiibos, RangoInicialExtra
    
    # Igualar la variable 120 para poder hacer separaciones de un mismo tamanio entre amiibos
    posicionYAmiibos = 120

    # canvas Notificaciones ----------------------------------------------------------------------------------------
    seccionNotificaciones = tk.Canvas(master=ventana, bg="#000000", highlightthickness=0, height=24, width=360)
    seccionNotificaciones.place(anchor=tk.NW, relx=0, rely=0)
    seccionNotificaciones.create_image(260,12, image=imagenConexion, anchor=tk.CENTER)
    seccionNotificaciones.create_image(285,12, image=imagenBateria, anchor=tk.CENTER)
    seccionNotificaciones.create_text(320,12, text="12:30", font=("Roboto", 11), fill="white",anchor=tk.CENTER)

    # canvas Header ------------------------------------------------------------------------------------------------
    seccionHeader = tk.Canvas(master=ventana, bg="#009789", highlightthickness=0, height=56, width=360)
    seccionHeader.place(x=0, y=24)
    seccionHeader.create_text(180,28, text="Amiibos", font=("Roboto", 14), fill="white")
    stringCantidad = str(RangoInicialExtra) + "/730"
    seccionHeader.create_text(300,28, text=stringCantidad, font=("Roboto", 14), fill="white")

    # canvas MENU --------------------------------------------------------------------------------------------------
    seccionMenu = tk.Canvas(master=ventana, bg="#FFFFFF", highlightthickness=0, height=570, width=360)
    seccionMenu.place(x=0, y=80)

    


    # Revisar si mi lista no esta vacia
    if listaDeAmiibos != []:
        for i in listaDeAmiibos:
            # Crear un canvas para cada seccion de amiibo
            seccionAmiiboIndividual = tk.Canvas(master=ventana, bg="white", highlightthickness=0, height=40, width=360)
            seccionAmiiboIndividual.place(anchor=tk.NW, x=0, y=posicionYAmiibos)

            # Adjuntar imagen de la carpeta como botones
            botonAmiibo = tk.Button(master=ventana, image=imagenBoton, border=0, bg="white", text=i.nombreAmiibo, command=lambda x=i:OnBottonClick(x))
            botonAmiibo.place(anchor=tk.CENTER, x=46, y=posicionYAmiibos + 20)
            seccionAmiiboIndividual.create_text(90,12 , anchor=tk.NW, text=i.nombreAmiibo, font=("Roboto", 10), fill="black") # Adjuntar el nombre del amiibo

            # Aumentar mi variable de posicion (Esto ocasiona la separacion entre secciones)
            posicionYAmiibos = posicionYAmiibos + 45

    # Crear un boton para regresar
    def RegresarPantalla():
        global listaDeAmiibos, RangoInicialExtra, RangoFinalExtra
        if RangoInicialExtra == 0:
            # No hacer nada
            pass
        else:
            listaDeAmiibos = [] # Reinicio mi listaDeAmiibos que quiero mostrar
            RangoInicialExtra = RangoInicialExtra - 10
            RangoFinalExtra = RangoFinalExtra - 10
            ObtenerInformacionAMIIBO("https://www.amiiboapi.com/api/amiibo/", RangoInicialExtra, RangoFinalExtra) # Agarro los datos que quiero en dicho rango
        PaginaPrincipal()


    # Crear un boton para continuar
    def ContinuarPantalla():
        global listaDeAmiibos, RangoInicialExtra, RangoFinalExtra
        if RangoFinalExtra == 740:
            # No hacer nada
            pass
        else:
            listaDeAmiibos = []
            RangoInicialExtra = RangoInicialExtra + 10
            RangoFinalExtra = RangoFinalExtra + 10
            ObtenerInformacionAMIIBO("https://www.amiiboapi.com/api/amiibo/", RangoInicialExtra, RangoFinalExtra)
        PaginaPrincipal()

    # Crear mis botones de inicio y regreso
    BotonRegresarPantalla = tk.Button(master=ventana, image=imagenGoLeft, border=0, bg="#FFFFFF", command=RegresarPantalla)
    BotonRegresarPantalla.place(anchor=tk.CENTER, x=120, y=600)

    BotonContinuarPantalla = tk.Button(master=ventana, image=imagenGoRight, border=0, bg="#FFFFFF", command=ContinuarPantalla)
    BotonContinuarPantalla.place(anchor=tk.CENTER, x=240, y=600)



# INICIO DEL PROGRAMA ------------------------------------------------------------------------------------------------
PaginaPrincipal()


ventana.mainloop()



