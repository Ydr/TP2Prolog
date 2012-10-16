from Tkinter import *  
from tkMessageBox import *
from pyswip import Functor, Variable, Query, call 
     
class Principal:
     
    
    def __init__(self,master):
        self.fondoinicio=PhotoImage(file="Imagenes/Fondo Inicio.gif")
        self.fondos=PhotoImage(file="Imagenes/Fondoo.gif")
        self.fondo=PhotoImage(file='Imagenes/fondo.gif') #Fondo blanco
        self.ingreso=PhotoImage(file="Imagenes/Ingresar recetas.gif")
        self.consult=PhotoImage(file="Imagenes/Consultas.gif")
        self.ing=PhotoImage(file="Imagenes/Ingresar.gif")
        self.consultar=PhotoImage(file="Imagenes/Consultar.gif")
        self.bienvenido=PhotoImage(file="Imagenes/inicio.gif")
	self.ayuda=PhotoImage(file="Imagenes/ayuda.gif")
        self.ventana_principal_general() #Llama a la ventana principal
        self.creomenu() #Ejecuta la barra de menu
        
    
    def ventana_principal_general(self):
        root.geometry("800x600") 
        self.lbfondo=Label(root, image=self.fondo).place(x=0,y=0) 
        self.lb1=Label(root,image=self.fondoinicio,bg='white').place(x=0,y=67) #Posicion del logo
        self.but1=Button(root,image=self.bienvenido,command=self.ventana_principal_general).place(x=0,y=0)
        self.but1=Button(root,image=self.ingreso,bg='white',command=self.ventana_ingreso).place(x=256,y=0)
        self.but2=Button(root,image=self.consult,bg='white',command=self.ventana_consulta).place(x=512,y=0)
        if not self: root.quit()  

    def ingresar_receta(self):
        self.ingredientes = self.entry_ingredientes.get()
        self.pasos = self.entry_pasos.get()
        self.nombre = self.entry_nombre.get()
        self.autor = self.entry_autor.get()
        self.estilo = self.entry_estilo.get()
        
        #Se convierte a minuscula todo el string de entrada para ser almacenado en la bc
        self.ingredientes = self.ingredientes.lower()
        self.pasos = self.pasos.lower()
        self.nombre = self.nombre.lower()
        self.autor = self.autor.lower()
        self.estilo = self.estilo.lower()
        
        if ((self.ingredientes!= "") and (self.pasos!="") and (self.nombre!="") and (self.autor !="") and (self.estilo!="")): #El entry de raza no debe ser vacio
            showinfo("Nueva Receta", "Se ha anadido una nueva receta a la base de conocimiento")
            self.entry_ingredientes.delete(0, END)   #Se limpian todos los entry
            self.entry_pasos.delete(0, END)
            self.entry_nombre.delete(0,END)
            self.entry_autor.delete(0, END)
            self.entry_estilo.delete(0, END)       
            return self.guardar_cont(self.ingredientes, self.pasos, self.nombre, self.autor, self.estilo ) #Guarda el contenido que se ingresa 

        else:
            showwarning("Error", "Es obligatorio poner todos los campos de la receta")


    #Funcion que guarda en la bc y en un archivo txt las recetas 
    def guardar_cont(self,ingredientes, pasos, nombre, autor, estilo):     
	assertz = Functor("assertz", 1)
	receta = Functor("receta", 5)
	call(assertz(receta(self.ingredientes,self.pasos,self.nombre,self.autor,self.estilo)))
        try:                # Se lee el txt
            infousuario=("receta("+self.ingredientes, self.pasos, self.nombre, self.autor, self.estilo +").")
            info=open("Base_Conocimiento.txt","r")              
            info=open("Base_Conocimiento.txt","a") #Abre la informacion guardada del txt
            info.write(",".join(infousuario)+"\n")
            info.close()
           

        except IOError:     #Creacion del archivo si no esta creado
            info=open("Base_Conocimiento.txt","w")
            info.write(",".join(infousuario)) 
            self.guardar_cont(self.ingredientes, self.pasos, self.nombre, self.autor, self.estilo)
            info.close()

    # Funcion que obtiene datos del entry y consulta en la bc
    def consultar_receta(self):
        self.ingredientesc = self.entry_ingredientesc.get()
        self.pasosc = self.entry_pasosc.get()
        self.nombrec = self.entry_nombrec.get()
        self.autorc = self.entry_autorc.get()
        self.estiloc = self.entry_estiloc.get()
        
        self.ingredientesc = self.ingredientesc.lower() 
        self.pasosc = self.pasosc.lower()
        self.nombrec = self.nombrec.lower()
        self.autorc = self.estiloc.lower()
        self.estiloc = self.estiloc.lower()
        
	receta = Functor("receta", 5)
	Var1 = Variable()
	Var2 = Variable()
	Var3 = Variable()
	Var4 = Variable()
	Var5 = Variable()
	
	banderas = ["0","0","0","0","0"] #Arreglo de banderas, nos sirve para saber si el usuario ingreso o no valores en 
									 #los entry
	if self.ingredientesc != "":
		Var1 = self.ingredientesc
		banderas[0]="1"
	if self.pasosc != "":
		Var2 = self.pasosc
		banderas[1]="1"
	if self.nombrec !="":
		Var3 = self.nombrec
		banderas[2]="1"
	if self.autorc != "":
		Var4 = self.autorc
		banderas[3]="1"
	if self.estiloc != "":
		Var5 = self.estiloc
		banderas[4]="1"

	consulta = Query(receta(Var1, Var2, Var3, Var4, Var5))
	
	contadorConsulta = consulta.nextSolution()      
        self.entry_ingredientesc.delete(0, END)
        self.entry_pasosc.delete(0, END)
        self.entry_nombrec.delete(0,END)
        self.entry_autorc.delete(0, END)
        self.entry_estiloc.delete(0, END)

	if contadorConsulta == 0: #Si no hay coincidencias con la busqueda
		showinfo("Consulta", "No se encontraron coincidencias")   
	else:         			  #Sino se llama a la funcion de muestra de datos
         	return self.mostrar_resultados_de_BC (Var1, Var2, Var3, Var4, Var5, banderas) #
     
    
    def mostrar_resultados_de_BC (self, Var1, Var2, Var3, Var4, Var5, banderas):
	ventconsulta = Toplevel()
	ventconsulta.resizable(width=NO,height=NO)
	
	ventconsulta.title("Consulta")
	ventconsulta.geometry('570x600')
	
	self.s = Scrollbar(ventconsulta)
	self.TextoResultado = Text(ventconsulta)
	self.TextoResultado.focus_set()
	self.s.pack(side=RIGHT, fill=Y)
	self.TextoResultado.pack(side=LEFT, fill=Y)
	self.s.config(command=self.TextoResultado.yview)
	self.TextoResultado.config(yscrollcommand=self.s.set)
	self.TextoResultado.insert(END, "Coincidencias\n")
	receta = Functor("receta", 5)
	q = Query(receta(Var1, Var2, Var3, Var4, Var5)) 
	
	while q.nextSolution(): 	 #Mientras existan soluciones en la base de conocimientos
		if banderas[0] == "1":   #Se verifican las banderas del arreglo, estas se realizan con el fin de verificar
								 #la unificacion de la consulta, si en la bandera existe un 1, quiere decir que este
								 #argumento se uso para consultar, los demas tienen que ser sacados de la bc por medio
								 #de Varn.value
			self.TextoResultado.insert(END, "\nIngredientes: "+Var1+" ")
		if banderas[1] == "1":
			self.TextoResultado.insert(END, "Pasos: "+Var2+" ")
		if banderas[2] == "1":
			self.TextoResultado.insert(END, "Receta: "+Var3+" ")
		if banderas[3] == "1":
			self.TextoResultado.insert(END, "Nombre: "+Var4+" ")
		if banderas[4] == "1":
			self.TextoResultado.insert(END, "Estilo: "+Var5+" ")
			
		if banderas[0] != "1":
			self.TextoResultado.insert(END, "\nIngredientes: %s " %(Var1.value))
		if banderas[1] != "1":
			self.TextoResultado.insert(END, "Pasos: %s " %(Var2.value))
		if banderas[2] != "1":
			self.TextoResultado.insert(END, "Nombre: %s " %(Var3.value))
		if banderas[3] != "1":
			self.TextoResultado.insert(END, "Autor: %s " %(Var4.value))
		if banderas[4] != "1":
			self.TextoResultado.insert(END, "Estilo: %s " %(Var5.value))
	
	q.closeQuery()
   
	ventconsulta.mainloop()

    # Ventana de ingreso
    def ventana_ingreso(self):
       
        root.geometry("800x600") #Tamano estandar de la raiz
        self.lbfondo=Label(root, image=self.fondo).place(x=0,y=67) #Fondo blanco para tapar
        self.lb1=Label(root,image=self.fondos,bg='white').place(x=0,y=67) #Posicion del logo
        
        
        self.label_ingredientes = Label (root, text= "Ingredientes",fg = 'black', font = ('arial',15,'bold'))
        self.label_ingredientes.place(x=350,y=220)
        
        self.entry_ingredientes = Entry (root, width=22 ,font=("arial", 15))
        self.entry_ingredientes.place(x=480,y=220)
        
        self.label_pasos = Label(root, text= "Pasos", font = ('arial',15,'bold'))
        self.label_pasos.place(x=350,y=260)
        
        self.entry_pasos = Entry (root, width=22, font=("arial", 15))
        self.entry_pasos.place(x=480,y=260)
        
        self.label_nombre = Label(root, text= "Nombre",  font = ('arial',15,'bold'))
        self.label_nombre.place(x=350,y=300)
        
        self.entry_nombre = Entry (root, width=22,font=("arial", 15))
        self.entry_nombre.place(x=480,y=300)
        
        self.label_autor = Label(root, text= "Autor",  font = ('arial',15,'bold'))
        self.label_autor.place(x=350,y=340)
        
        self.entry_autor = Entry (root, width=22, font=("arial", 15))
        self.entry_autor.place(x=480,y=340)
        
        self.label_estilo = Label(root, text= "Estilo",  font = ('arial',15,'bold'))
        self.label_estilo.place(x=350,y=380)
        
        self.entry_estilo = Entry (root, width=22 ,font=("arial", 15))
        self.entry_estilo.place(x=480,y=380)
        
        self.boton_ingresar = Button(root, image= self.ing,  font = ('arial',15,'bold'), cursor = "hand2", command = self.ingresar_receta )
        self.boton_ingresar.place(x=100,y=460)

   
    # Ventana de consultas
    def ventana_consulta(self):
        root.geometry("800x600") #Tamano estandar de la raiz
        self.lbfondo=Label(root, image=self.fondo).place(x=0,y=67) #Fondo blanco para tapar
        self.lb1=Label(root,image=self.fondos,bg='white').place(x=0,y=67) #Posicion del logo
        
        self.label_ingredientesc = Label (root, text= "Ingredientes", font = ('arial',15,'bold'))
        self.label_ingredientesc.place(x=350,y=220)
        self.entry_ingredientesc = Entry (root, width=22,font=("arial", 15))
        self.entry_ingredientesc.place(x=480,y=220)
        
        self.label_pasosc = Label(root, text= "Pasos", borderwidth = 0,  font = ('arial',15,'bold'))
        self.label_pasosc.place(x=350,y=260)
        self.entry_pasosc = Entry (root, width=22,font=("arial", 15))
        self.entry_pasosc.place(x=480,y=260)
        
        self.label_nombrec = Label(root, text= "Nombre",  font = ('arial',15,'bold'))
        self.label_nombrec.place(x=350,y=300)
        self.entry_nombrec = Entry (root, width=22,font=("arial", 15))
        self.entry_nombrec.place(x=480,y=300)
        
        self.label_autorc = Label(root, text= "Autor",  font = ('arial',15,'bold'))
        self.label_autorc.place(x=350,y=340)
        self.entry_autorc = Entry (root, width=22, font=("arial", 15))
        self.entry_autorc.place(x=480,y=340)
        
        self.label_estiloc = Label(root, text= "Estilo", font = ('arial',15,'bold'))
        self.label_estiloc.place(x=350,y=380)
        self.entry_estiloc = Entry (root, width=22 ,font=("arial", 15))
        self.entry_estiloc.place(x=480,y=380)
        
        self.boton_consultar = Button(root, image= self.consultar,  font = ('arial',15,'bold'), borderwidth = 0, cursor = "hand2", command = self.consultar_receta )
        self.boton_consultar.place(x=100,y=460)

 
    # Funcion que muestra mensaje acerca de del programa
    def info(self):
       	showinfo("Acerca del Programa", 'Instituto Tecnologico de Costa Rica\n\nPrograma Restaurante Le Puolet\n\nCreacion:\n\t Octubre 2012\n\nDesarrolladores:\n\tYader Morales Lopez\n\tFrank Brenes Alvarado\n\tMercedes Escalante Karr\n')
 
   # Funcion para salir del programa
    def salir(self):
        if askokcancel("Cerrar", "Realmante desea salir?"):
            root.quit()
            root.destroy()

    # Funcion que crea la barra de menu del programa          
    def creomenu(self):

        self.barra = Menu(root)
        root.config(menu = self.barra)
        self.Ayuda = Menu(self.barra)
        self.Salida = Menu(self.barra)
        self.barra.add_command(label="Ayuda", command=self.info) 
        self.barra.add_command(label="Salir", command=self.salir)

root=Tk()
root.resizable(width=NO,height=NO)
app=Principal(root) #Asigna un espacio de memoria para ejecutar la clase Principal
root.title('Restaurant Le Poulet') #Nombre de la raiz
root.geometry('810x600') #Tamano estandar de la raiz
root.mainloop() #Ejecuta la ventana
