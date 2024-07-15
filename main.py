import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import SistemaMembrana
import Regla
from Generador import generador
from utils import regla_a_string
from utils import split_string
from utils import transformar_objetos
from utils import split_and_sort_numbers
from utils import m_queens_of_the_hill
from utils import agrupar_valquirias
from utils import obtener_estructura
from tkinter import filedialog
from utils import leer_archivo_y_guardar_informacion
from utils import exportar_txt
from utils import parse_personalizado
import Objeto

from collections import Counter

import random
random.seed(42)



def mostrar_pop(mensaje):
    messagebox.showinfo("No tan deprisa", mensaje)

class Interfaz:
    def __init__(self, ventana, lista_sistemas = [], lista_reglas = []):
        self.ventana = ventana
        self.ventana.title("Queens of the Hill")
        
        # Dividir la ventana principal en dos secciones
        self.frame_izquierdo = tk.Frame(ventana)
        self.frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.frame_derecho = tk.Frame(ventana)
        self.frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Crear el cuadro de texto en el frame derecho para mostrar las listas de sistemas y reglas
        self.scrollbar = tk.Scrollbar(self.frame_derecho)
        

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.cuadro_texto = tk.Text(self.frame_derecho, height=40, width=50, yscrollcommand=self.scrollbar.set)
        self.cuadro_texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar.config(command=self.cuadro_texto.yview)
        
        # Inicializar el estado de la interfaz
        self.estado = 3
        
        # Crear el botón para cambiar la estructura en el frame izquierdo
        self.boton_siguiente = tk.Button(self.frame_izquierdo, text="Siguiente", command=self.cambiar_estructura, height=3, width=20, font=("Arial", 16))
        self.boton_siguiente.pack(pady=(10, 0))
        
        # Crear el botón para simular en el frame izquierdo
        self.boton_simular = tk.Button(self.frame_izquierdo, text="Simular", command=self.simular, height=3, width=20, font=("Arial", 16), bg='green')
        self.boton_simular.pack(pady=(10, 0))
        self.boton_simular.pack_forget()
        
        self.boton_eliminar = tk.Button(self.frame_izquierdo, text="Eliminar valquiria", command=self.eliminar, height=3, width=20, font=("Arial", 16), bg='red')
        self.boton_eliminar.pack(pady=(10, 0))
        self.boton_eliminar.pack_forget()
        
        self.boton_generador = tk.Button(self.frame_izquierdo, text="Utilizar generador", command=self.crear_estructura_generador, height=3, width=20, font=("Arial", 16))
        self.boton_generador.pack(pady=(10, 0))
        self.boton_generador.pack_forget()
        
        
        self.boton_generar = tk.Button(self.frame_izquierdo, text="Generar valquirias", command=self.generar, height=3, width=20, font=("Arial", 16), bg="green")
        self.boton_generar.pack(pady=(10, 0))
        self.boton_generar.pack_forget()

        self.boton_importar = tk.Button(self.frame_izquierdo, text="Importar valquirias", command=self.abrir_explorador, height=3, width=20, font=("Arial", 16))
        self.boton_importar.pack(pady=(10, 0))
        self.boton_importar.pack_forget()


        self.boton_exportar = tk.Button(self.frame_izquierdo, text="Exportar valquirias", command=self.exportar, height=3, width=20, font=("Arial", 16))
        self.boton_exportar.pack(pady=(10, 0))
        self.boton_exportar.pack_forget()
                
    
        
        


        
        
        # Inicializar las variables para almacenar las respuestas
        self.respuesta1 = ""
        self.respuesta3 = ""
        self.estructura = []
        self.respuesta2 = {}

                
        self.lista_sistemas = lista_sistemas
        self.lista_reglas = lista_reglas
        
        if(self.lista_sistemas == []):
            # Inicializar la primera estructura
            self.crear_estructura_inicial()
            self.boton_siguiente.pack_forget()
        else:
            self.actualizar_cuadro_texto()
            self.crear_estructura4()
        
        
     
        
        
        


    def abrir_explorador(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos de texto", ".txt"), ("Todos los archivos", ".*"))
        )
        if archivo:
            listasistemas, listareglas = leer_archivo_y_guardar_informacion(archivo)
            self.lista_sistemas=self.lista_sistemas + listasistemas
            self.lista_reglas = self.lista_reglas + listareglas
            self.actualizar_cuadro_texto()
            self.crear_estructura4()
    
        
    def exportar(self):
        def on_option_select(event):
            selected_option = option_var.get()
            if selected_option == "TODAS":
                input_label.grid_remove()
                input_entry1.grid_remove()
                input_entry2.grid_remove()
            elif selected_option == "RANGO":
                input_label.config(text="Introduce el rango:")
                input_label.grid(row=1, column=0, padx=10, pady=10)
                input_entry1.grid(row=1, column=1, padx=10, pady=10)
                input_entry2.grid(row=1, column=2, padx=10, pady=10)
                input_entry2.grid()  # Mostrar la segunda casilla
            elif selected_option == "PERSONALIZADO":
                input_label.config(text="Introduce la lista personalizada:")
                input_label.grid(row=1, column=0, padx=10, pady=10)
                input_entry1.grid(row=1, column=1, padx=10, pady=10)
                input_entry2.grid_remove()  # Ocultar la segunda casilla

        def on_submit():
            selected_option = option_var.get()
            if selected_option == "TODAS":
                file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                 filetypes=[("Text files", ".txt"), ("All files", ".*")])
                exportar_txt(self.lista_sistemas, self.lista_reglas, file_path)
                menu_window.destroy()

            elif selected_option == "RANGO":
                try:
                    rango1 = input_entry1.get()
                    rango2 = input_entry2.get()
                    if rango1 and rango2:
                        if rango2 == 'end':
                            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                        filetypes=[("Text files", ".txt"), ("All files", ".*")])
                            exportar_txt(self.lista_sistemas[int(rango1)-1:len(self.lista_sistemas)], self.lista_reglas[int(rango1)-1:int(rango2)], file_path)   
                            menu_window.destroy()
                        else:
                            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                        filetypes=[("Text files", ".txt"), ("All files", ".*")])
                            exportar_txt(self.lista_sistemas[int(rango1)-1:int(rango2)], self.lista_reglas[int(rango1)-1:int(rango2)], file_path)   
                            menu_window.destroy()

                except: 
                    mostrar_pop("Rango inválido")

            elif selected_option == "PERSONALIZADO":
                personalizado = input_entry1.get()
                if personalizado:
                    try:
                        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                    filetypes=[("Text files", ".txt"), ("All files", ".*")])
                        indices = parse_personalizado(personalizado, len(self.lista_sistemas))
                        sistemas_seleccionados = [self.lista_sistemas[i] for i in indices]
                        reglas_seleccionadas = [self.lista_reglas[i] for i in indices]
                        exportar_txt(sistemas_seleccionados, reglas_seleccionadas, file_path)
                        menu_window.destroy()
                    except:
                        mostrar_pop("Selección inválida")
            


        
        # Crear la ventana principal para el menú
        menu_window = tk.Toplevel()
        menu_window.title("Seleccionar opción")

        # Variable para el selector
        option_var = tk.StringVar()

        # Crear el combobox (selector)
        option_label = tk.Label(menu_window, text="Seleccione una opción:")
        option_label.grid(row=0, column=0, padx=10, pady=10)
        option_combobox = ttk.Combobox(menu_window, textvariable=option_var)
        option_combobox['values'] = ("TODAS", "RANGO", "PERSONALIZADO")
        option_combobox.grid(row=0, column=1, padx=10, pady=10)
        option_combobox.bind("<<ComboboxSelected>>", on_option_select)

        # Celda de entrada para RANGO y PERSONALIZADO
        input_label = tk.Label(menu_window)
        input_entry1 = tk.Entry(menu_window)
        input_entry2 = tk.Entry(menu_window)

        # Botón para enviar la selección
        submit_button = tk.Button(menu_window, text="Exportar", command=on_submit)
        submit_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)



    def crear_estructura_inicial(self):
        self.boton_siguiente.pack_forget()
        self.limpiar_frame_izquierdo()
        self.boton_inicio = tk.Button(self.frame_izquierdo, text="Introducir valquiria", command=self.cambiar_estructura, height=3, width=20, font=("Arial", 16))
        self.boton_inicio.pack(pady=(10, 0))
        self.boton_generador = tk.Button(self.frame_izquierdo, text="Utilizar generador", command=self.crear_estructura_generador, height=3, width=20, font=("Arial", 16))
        self.boton_generador.pack(pady=(10, 0))

        self.boton_importar = tk.Button(self.frame_izquierdo, text="Importar valquirias", command=self.abrir_explorador, height=3, width=20, font=("Arial", 16))
        self.boton_importar.pack(pady=(10, 0))
        
        


    def limpiar_frame_izquierdo(self):
        # Limpiar el frame izquierdo excepto los botones de cambio y simular
        for widget in self.frame_izquierdo.winfo_children():
            if widget not in [self.boton_siguiente, self.boton_simular, self.boton_eliminar, self.boton_generador, self.boton_generar, self.boton_importar, self.boton_exportar]:
                self.boton_siguiente.pack_forget()
                self.boton_simular.pack_forget()
                self.boton_eliminar.pack_forget()
                self.boton_generador.pack_forget()
                self.boton_generar.pack_forget()
                self.boton_importar.pack_forget()
                self.boton_exportar.pack_forget()
                widget.destroy()
    
    def crear_estructura1(self):
        self.limpiar_frame_izquierdo()

        self.boton_generador.pack_forget()
        self.boton_siguiente.pack(side=tk.TOP, pady=10)
        self.boton_siguiente.config(text= "Siguiente")
        self.boton_importar.pack_forget()
        self.boton_exportar.pack_forget()
        # Crear la primera estructura de la interfaz
        self.label1 = tk.Label(self.frame_izquierdo, text="Introduce la estructura de la valquiria", font=("Arial", 14))  # Aumentar tamaño de la fuente
        self.label1.pack()
        self.entry1 = tk.Entry(self.frame_izquierdo, font=("Arial", 14), width=30)  # Aumentar tamaño de la fuente y el ancho del cuadro de entrada
        self.entry1.pack()


    def crear_estructura2(self):
        self.limpiar_frame_izquierdo()
        self.boton_siguiente.pack(side=tk.TOP, pady=10)

        # Obtener la estructura a partir del string
        numeros = split_and_sort_numbers(self.respuesta1)
        self.entries = {}
        
        # Crear un frame para las entradas y etiquetas
        frame_entradas = tk.Frame(self.frame_izquierdo)
        frame_entradas.pack()

        for idx, numero in enumerate(numeros):
            label = tk.Label(frame_entradas, text=f"Objetos de la membrana {numero}")
            entry = tk.Entry(frame_entradas)
            self.entries[numero] = entry

            # Organizar en dos columnas
            row = idx // 2
            col = (idx % 2) * 2
            label.grid(row=row, column=col, padx=5, pady=5)
            entry.grid(row=row, column=col + 1, padx=5, pady=5)

    def crear_estructura3(self):
        self.limpiar_frame_izquierdo()
        self.boton_siguiente.pack(side=tk.TOP, pady=10)

        # Crear la etiqueta
        self.label3 = tk.Label(self.frame_izquierdo, text="Estructura 3: Introduce las reglas")
        self.label3.pack()
        # Crear el cuadro de texto
        self.text3 = tk.Text(self.frame_izquierdo, height=40, width=70)
        self.text3.pack()

        
    def crear_estructura4(self):
        self.limpiar_frame_izquierdo()
        self.boton_siguiente.pack(side=tk.TOP, pady=5)  # Botón de siguiente

        self.boton_generador.pack(side=tk.TOP, pady=5)  # Botón de utilizar generador
        self.boton_siguiente.config(text="Nueva valquiria")

        # Crear espacio para los botones y el texto
        espacio = tk.Frame(self.frame_izquierdo, height=200, bg="lightgrey")
        espacio.pack(fill=tk.BOTH, expand=True)


        
        # Crear el texto "Valquiria a eliminar"
        texto_valquiria = tk.Label(espacio, text="Valquiria a eliminar", font=("Arial", 14))
        texto_valquiria.pack(side=tk.TOP, pady=5)

        # Crear el cuadro de texto para incluir un número (más pequeño)
        self.numero_entry = tk.Entry(espacio, width=30)  # Ajusta el ancho según sea necesario
        self.numero_entry.pack(side=tk.TOP, pady=5)
        self.boton_eliminar.pack(side=tk.TOP, pady=5)   # Botón de eliminar

        # Configurar los botones en el espacio intermedio
        self.boton_importar.pack(side=tk.TOP, pady=5)   # Botón de importar
        self.boton_exportar.pack(side=tk.TOP, pady=5)   # Botón de exportar

        # Botón de simular (verde) en la parte inferior
        self.boton_simular.pack(side=tk.BOTTOM, pady=5)


    def crear_estructura_generador(self):
        self.limpiar_frame_izquierdo()
        self.boton_simular.pack_forget()
        self.boton_siguiente.pack_forget()
        self.boton_generador.pack_forget()
        self.boton_importar.pack_forget()
        self.boton_exportar.pack_forget()

        self.boton_eliminar.pack_forget()
        
        
        self.entries_generador = {}
        # Crear un frame para las entradas y etiquetas
        frame_entradas_generador = tk.Frame(self.frame_izquierdo)
        frame_entradas_generador.pack()
        label_padx = 5
        label_pady = 10
        entry_padx = 5
        entry_pady = 10
        
        
        self.label1_generador = tk.Label(frame_entradas_generador, text="Número de valquirias", font=("Arial", 14))
        self.label1_generador.grid(row=0, column=0,padx=label_padx, pady=label_pady)
        self.entry1_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry1_generador.grid(row=0, column=1, padx=entry_padx, pady=entry_pady)

        self.label2_generador = tk.Label(frame_entradas_generador, text="Número máximo de membranas", font=("Arial", 14))
        self.label2_generador.grid(row=1, column=0, padx=label_padx, pady=label_pady)
        self.entry2_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry2_generador.grid(row=1, column=1, padx=entry_padx, pady=entry_pady)


        self.label3_generador = tk.Label(frame_entradas_generador, text="Número máximo de membranas hijas", font=("Arial", 14))
        self.label3_generador.grid(row=2, column=0, padx=label_padx, pady=label_pady)
        self.entry3_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry3_generador.grid(row=2, column=1, padx=entry_padx, pady=entry_pady)


        self.label4_generador = tk.Label(frame_entradas_generador, text="Alfabeto de entrada", font=("Arial", 14))
        self.label4_generador.grid(row=3, column=0, padx=label_padx, pady=label_pady)
        self.entry4_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry4_generador.grid(row=3, column=1, padx=entry_padx, pady=entry_pady)


        self.label5_generador = tk.Label(frame_entradas_generador, text="Número máximo de objetos por membrana", font=("Arial", 14))
        self.label5_generador.grid(row=4, column=0, padx=label_padx, pady=label_pady)
        self.entry5_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry5_generador.grid(row=4, column=1, padx=entry_padx, pady=entry_pady)


        self.label6_generador = tk.Label(frame_entradas_generador, text="Número máximo de objetos LHS", font=("Arial", 14))
        self.label6_generador.grid(row=5, column=0, padx=label_padx, pady=label_pady)
        self.entry6_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry6_generador.grid(row=5, column=1,padx=entry_padx, pady=entry_pady)


        self.label7_generador = tk.Label(frame_entradas_generador, text="Número máximo de objetos RHS misma membrana", font=("Arial", 14))
        self.label7_generador.grid(row=6, column=0, padx=label_padx, pady=label_pady)
        self.entry7_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry7_generador.grid(row=6, column=1, padx=entry_padx, pady=entry_pady)

        
        self.label8_generador = tk.Label(frame_entradas_generador, text="Número máximo de objetos RHS padre", font=("Arial", 14))
        self.label8_generador.grid(row=7, column=0, padx=label_padx, pady=label_pady)
        self.entry8_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry8_generador.grid(row=7, column=1, padx=entry_padx, pady=entry_pady)

        self.label9_generador = tk.Label(frame_entradas_generador, text="Número máximo de objetos RHS hijas", font=("Arial", 14))
        self.label9_generador.grid(row=8, column=0, padx=label_padx, pady=label_pady)
        self.entry9_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry9_generador.grid(row=8, column=1, padx=entry_padx, pady=entry_pady)


        self.label10_generador = tk.Label(frame_entradas_generador, text="Número máximo de reglas por membrana", font=("Arial", 14))
        self.label10_generador.grid(row=9, column=0, padx=label_padx, pady=label_pady)
        self.entry10_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry10_generador.grid(row=9, column=1, padx=entry_padx, pady=entry_pady)


        self.label11_generador = tk.Label(frame_entradas_generador, text="Máximo timer", font=("Arial", 14))
        self.label11_generador.grid(row=10, column=0, padx=label_padx, pady=label_pady)
        self.entry11_generador = tk.Entry(frame_entradas_generador, font=("Arial", 14), width=30)
        self.entry11_generador.grid(row=10, column=1, padx=entry_padx, pady=entry_pady)

        
        
        

        self.boton_generar.pack(side=tk.BOTTOM, pady=10)
        boton_salir_generador = tk.Button(self.frame_izquierdo, text="Salir generador", command=self.salir_generador, height=3, width=20, font=("Arial", 16), bg='red')
        boton_salir_generador.pack(pady=(10, 0))

            
        

    def salir_generador(self):
        if(self.lista_sistemas==[]):
            self.crear_estructura_inicial()
            self.boton_generador.pack(pady=(10, 0))
            self.boton_generar.pack_forget()
            
        else:
            self.crear_estructura4()
        

    def cambiar_estructura(self):
        if self.estado == 0:
            self.respuesta1 = self.entry1.get()
            if self.respuesta1 == '':
                mostrar_pop("Una valquiria no puede tener una estructura vacía.")
            else:
                try:
                    self.estructura = obtener_estructura(self.respuesta1)
                    self.crear_estructura2()
                    self.estado = 1
                except:
                    mostrar_pop("Estructura no válida")
                    
                
        elif self.estado == 1:
            try:
                for numero, entry in self.entries.items():
                    for i in range(len(entry.get())):
                        if not (entry.get()[i].isalpha() or entry.get()[i].isspace() or entry.get()[i] == ',' or entry.get()[i] == '{' or entry.get()[i] == '}' or entry.get()[i].isdigit()):
                            raise ValueError("Codificación incorrecta")
                        


                self.respuesta2 = {numero: transformar_objetos(entry.get().split(",")) for numero, entry in self.entries.items()}
                dict_0 = {0:[]}
                dict_0.update(self.respuesta2)
                self.respuesta2 = dict_0
                self.crear_estructura3()
                self.estado = 2
            except:
                mostrar_pop("Introduce una lista de objetos válida")
            
        elif self.estado == 2:
            self.respuesta3 = self.text3.get("1.0", tk.END)
            if(self.respuesta3 != '\n'):
                mensaje_error_reglas = ""
                lineas = self.respuesta3.splitlines()
                reglas = []
                for linea in lineas:
                    if linea != '':
                        try:
                            reglas = reglas + [split_string(linea)]
                        except:
                            mensaje_error_reglas = mensaje_error_reglas + "- " +  linea + " no es una regla bien definida \n"
                
                if (mensaje_error_reglas==""):
                    self.respuesta3 = reglas
                    self.crear_estructura4()
                    self.lista_sistemas=self.lista_sistemas + [SistemaMembrana.SistemaMembrana(self.estructura, self.respuesta2)]
                    self.lista_reglas = self.lista_reglas + [self.respuesta3]
                    self.actualizar_cuadro_texto()
                    self.estado = 3
                else:
                    mostrar_pop(mensaje_error_reglas)

            else:
                self.respuesta3 = []
                self.crear_estructura4()
                self.lista_sistemas=self.lista_sistemas + [SistemaMembrana.SistemaMembrana(self.estructura, self.respuesta2)]
                self.lista_reglas = self.lista_reglas + [self.respuesta3]
                self.actualizar_cuadro_texto()
                self.estado = 3
        elif self.estado == 3:
            self.boton_simular.pack_forget()
            self.boton_generador.pack_forget()
            self.boton_eliminar.pack_forget()
            self.estado = 0
            self.crear_estructura1()

    def actualizar_cuadro_texto(self):
        self.cuadro_texto.delete(1.0, tk.END)
        for valquiria in range(len(self.lista_sistemas)):
            self.cuadro_texto.insert(tk.END, f"Valquiria {valquiria + 1}:\n\n")
            self.cuadro_texto.insert(tk.END, self.lista_sistemas[valquiria])
            self.cuadro_texto.insert(tk.END, f"\n\nReglas:\n")
            for regla in self.lista_reglas[valquiria]:
                self.cuadro_texto.insert(tk.END, str(regla) + "\n")
            self.cuadro_texto.insert(tk.END, "\n\n")

            

            
            

    def simular(self):
        if(len(self.lista_sistemas)==0):
            mostrar_pop("No hay definida ninguna valquiria para la competición")
        elif(len(self.lista_sistemas)==1):
            mostrar_pop("Solo hay una valquiria, por lo que no hay competición")
        else:


            numero_simulaciones = int(simpledialog.askstring("Entrada", "Introduce el número de torneos:"))
            tiempo_computacion = int(simpledialog.askstring("Entrada", "Introduce el tiempo máximo de computación en cada torneo:"))
            pasos_maximo = int(simpledialog.askstring("Entrada", "Introduce el número máximo de pasos de cada torneo:"))
            timer_maximo = int(simpledialog.askstring("Entrada", "Introduce el timer máximo permitido en el torneos:"))

            boolean_supera_timer = False
            for valquiria in self.lista_sistemas:
                for membrana, objetosmembrana in valquiria.objetos.items():
                    for objeto in objetosmembrana:
                        try:
                            if(objeto.timer > timer_maximo):
                                objeto.timer = timer_maximo
                                boolean_supera_timer = True
                        except: 
                            pass
            
            for reglas_valquiria in self.lista_reglas:
                for regla in reglas_valquiria:
                    for objeto in regla.salida:
                        try:
                            if(objeto.timer > timer_maximo):
                                objeto.timer = timer_maximo
                                boolean_supera_timer = True
         
                        except:
                            pass
                    if regla.salida_membrana_padre is not None:
                        for objeto in regla.salida_membrana_padre:
                            try:
                                if(objeto.timer > timer_maximo):
                                    objeto.timer = timer_maximo
                                    boolean_supera_timer = True
                            except:
                                pass

                    if regla.salida_membrana_hija is not None:
                        for objeto in regla.salida_membrana_hija:
                            try:
                                if(objeto.timer > timer_maximo):
                                    objeto.timer = timer_maximo
                                    boolean_supera_timer = True
                            except:
                                pass

                 

            
            self.boton_simular.pack_forget()

            for widget in self.ventana.winfo_children():
                if widget != self.ventana:
                    widget.destroy()
            scrollbar_final = tk.Scrollbar(self.ventana)
            scrollbar_final.pack(side=tk.RIGHT, fill=tk.Y)
            self.frame_botones = ttk.Frame(self.ventana)
            self.frame_botones.pack(pady=10)

            # Botones de opciones
            opciones = ["Iniciar Nueva Competición", "Exportar Resultados", "Exportar Valquirias", "Editar Competición"]

            for opcion in opciones:
                ttk.Button(self.frame_botones, text=opcion, command=lambda o=opcion: self.ejecutar_opcion(o)).pack(side=tk.LEFT, padx=5)



            self.cuadro_texto_final = tk.Text(self.ventana, width=300, height=100, yscrollcommand=scrollbar_final.set)
            scrollbar_final.config(command=self.cuadro_texto_final.yview)
            
            if(boolean_supera_timer):
                mostrar_pop("Se han reducido los timers que superan el valor máximo permitido en el torneo")
            
            self.cuadro_texto_final.pack(padx=20, pady=20)
            self.cuadro_texto_final.delete(1.0, tk.END)  # Limpiar el cuadro de texto antes de mostrar la nueva frase
            self.cuadro_texto_final.insert(tk.END, "VALQUIRIAS PARA LA COMPUTACIÓN: \n")
            for valquiria in range(len(self.lista_sistemas)):
                self.cuadro_texto_final.insert(tk.END, f"\nValquiria {valquiria+1} :  {self.lista_sistemas[valquiria]} \n")
                for regla in self.lista_reglas[valquiria]:
                    self.cuadro_texto_final.insert(tk.END, "Regla " + str(regla.id) + ": " + regla_a_string(regla) + "\n")

            self.cuadro_texto_final.insert(tk.END, "\nPARÁMETROS DE LA SIMULACIÓN: \n")   
            self.cuadro_texto_final.insert(tk.END, f"Número de torneos: {numero_simulaciones} \n")
            self.cuadro_texto_final.insert(tk.END, f"Tiempo máximo de computación para cada torneo: {tiempo_computacion} \n")
            self.cuadro_texto_final.insert(tk.END, f"Número máximo de pasos de computación de cada torneo: {pasos_maximo} \n")
            self.cuadro_texto_final.insert(tk.END, f"Timer máximo permitido en el torneo: {timer_maximo} \n")



            
            sistema_inicial,reglas_comun,_, relacion_membranas = agrupar_valquirias(self.lista_sistemas, self.lista_reglas)
            self.cuadro_texto_final.insert(tk.END, "\n\n\n\n\nSISTEMA PARA LA COMPUTACIÓN: \n")
            self.cuadro_texto_final.insert(tk.END, sistema_inicial.to_string() + "\n\n")
            self.cuadro_texto_final.insert(tk.END, "REGLAS PARA LA COMPUTACIÓN: \n")
            for regla in reglas_comun:
                self.cuadro_texto_final.insert(tk.END, f"Regla {regla.id}:   {regla_a_string(regla)} \n")
                
            sistemas_agrupados, dict_computacion_agrupados, dict_aniquilacion_agrupados, vpm_agrupados, mpv_agrupados, diccionario_a_devolver_agrupados, mensaje_fin_agrupados, aniquiladas_por_paso_agrupados, lista_metricas_agrupados, lista_metricas_media = m_queens_of_the_hill(self.lista_sistemas, self.lista_reglas, tiempo_computacion, pasos_maximo, numero_simulaciones)
            for torneo in range(numero_simulaciones):
                sistema = sistemas_agrupados[torneo]
                dict_computacion = dict_computacion_agrupados[torneo]
                dict_aniquilacion = dict_aniquilacion_agrupados[torneo]
                vpm = vpm_agrupados[torneo]
                mpv = mpv_agrupados[torneo]
                diccionario_a_devolver = diccionario_a_devolver_agrupados[torneo]
                mensaje_fin = mensaje_fin_agrupados[torneo]
                if mensaje_fin != "NO SE PRODUCE NINGUNA EVOLUCIÓN DEL SISTEMA":
                    self.cuadro_texto_final.insert(tk.END, "\n\n\n--------------- SIMULACIÓN DEL TORNEO NÚMERO " + str(torneo + 1))
                    aniquiladas_por_paso = aniquiladas_por_paso_agrupados[torneo]
                    lista_metricas = lista_metricas_agrupados[torneo]
                    for paso in list(diccionario_a_devolver.keys()):
                        self.cuadro_texto_final.insert(tk.END, "\n------ PASO: " + str(paso) + "\n")
                        self.cuadro_texto_final.insert(tk.END, "Reglas aplicadas en el paso " + str(paso) + ": \n")
                        reglas_aplicadas_paso = Counter(diccionario_a_devolver[paso][0])
                        lines = []
                        for regla_aplicada in list(reglas_aplicadas_paso.keys()):
                            if isinstance(regla_aplicada, Regla.Regla):
                                membrana_aplicada = regla_aplicada.membrana
                                valquiria_aplicada = vpm[membrana_aplicada]
                                membrana_original_aplicada = relacion_membranas[membrana_aplicada][1]
                                lines = lines + ["--Valquiria " + str(valquiria_aplicada) + " membrana " + str(membrana_original_aplicada) + " (" + str(membrana_aplicada)+ "): " + str(reglas_aplicadas_paso[regla_aplicada])+ " x regla " + str(regla_aplicada.id)]
                            else:
                                if regla_aplicada[0] == "i":
                                    lines = lines + ["--Membrana 0: " + str(reglas_aplicadas_paso[regla_aplicada])+ " x " + regla_aplicada]
                                else:
                                    membrana_aplicada = int(regla_aplicada[regla_aplicada.find('[') + 1: regla_aplicada.find(']')])
                                    if membrana_aplicada!=0:
                                        valquiria_aplicada = vpm[membrana_aplicada]
                                        membrana_original_aplicada = relacion_membranas[membrana_aplicada][1]
                                        lines = lines + ["--Valquiria " + str(valquiria_aplicada) + " membrana " + str(membrana_original_aplicada) + " (" + str(membrana_aplicada)+ "): " + str(reglas_aplicadas_paso[regla_aplicada])+ " x " + regla_aplicada[:regla_aplicada.find(")") + 1]]
                                    else:
                                        lines = lines + ["--Membrana 0: " + str(reglas_aplicadas_paso[regla_aplicada])+ " x " + regla_aplicada[:regla_aplicada.find(")")+1]]
                        diccionario_strings = {}
                        for string in lines:
                            clave, valor = string[:string.find(":")], string[string.find(":")+1:]
                            # Si la clave no está en el diccionario, agregarla con una lista vacía
                            if clave not in diccionario_strings:
                                diccionario_strings[clave] = []
                            
                            # Agregar el valor a la lista correspondiente a la clave
                            diccionario_strings[clave] = diccionario_strings[clave] + [valor]
                
                        
                        for membrana_aplicada in list(diccionario_strings.keys()):
                            texto_unido = (" , ").join(diccionario_strings[membrana_aplicada])
                            self.cuadro_texto_final.insert(tk.END, f"{membrana_aplicada}:{texto_unido} \n")


                        self.cuadro_texto_final.insert(tk.END, "\n Sistema tras la aplicación de las reglas: \n")
                        self.cuadro_texto_final.insert(tk.END, diccionario_a_devolver[paso][1].to_string())
                        if diccionario_a_devolver[paso][1] == diccionario_a_devolver[paso][2]:
                            self.cuadro_texto_final.insert(tk.END, "\n\n No se produce la disolución de ninguna membrana en este paso.\n")
                        else:
                            self.cuadro_texto_final.insert(tk.END, "\n\n Sistema tras aniquilar: \n ")
                            self.cuadro_texto_final.insert(tk.END, diccionario_a_devolver[paso][2].to_string())
                        self.cuadro_texto_final.insert(tk.END, "\n\n")
                    self.cuadro_texto_final.insert(tk.END, mensaje_fin)
                    self.cuadro_texto_final.insert(tk.END, "\n\n MÉTRICAS OBTENIDAS EN LA SIMULACIÓN DEL TORNEO " + str(torneo + 1) + " \n")
                
                    for valquiria in lista_metricas[0].keys():
                        self.cuadro_texto_final.insert(tk.END, "Métricas de la valquiria " + str(valquiria) + "\n")
                        self.cuadro_texto_final.insert(tk.END, "Métrica 1: " + str(lista_metricas[0][valquiria]) + "\n")
                        self.cuadro_texto_final.insert(tk.END, "Métrica 2: " + str(lista_metricas[1][valquiria]) + "\n")
                        self.cuadro_texto_final.insert(tk.END, "Métrica 3: " + str(lista_metricas[2][valquiria]) + "\n")
                        self.cuadro_texto_final.insert(tk.END, "Métrica 4: " + str(lista_metricas[3][valquiria]) + "\n")
                        self.cuadro_texto_final.insert(tk.END, "Métrica 5: " + str(lista_metricas[4][valquiria]) + "\n")
                        self.cuadro_texto_final.insert(tk.END, "Métrica 6: " + str(lista_metricas[5][valquiria]) + "\n\n")


                else:
                    self.cuadro_texto_final.insert(tk.END, "\n\nNO EXISTE NINGUNA REGLA APLICABLE AL SISTEMA, POR LO QUE NO HAY ESTE NO EVOLUCIONA")
                    break

                    
            
            self.cuadro_texto_final.insert(tk.END, "\n\n\-----------------RESULTADO MEDIO DE LOS DIFERENTES TORNEOS----------------- \n")
        
            for valquiria in lista_metricas_agrupados[0][0].keys():
                    self.cuadro_texto_final.insert(tk.END, "Métricas de la valquiria " + str(valquiria) + "\n")
                    self.cuadro_texto_final.insert(tk.END, "Métrica 1: " + str(lista_metricas_media[0][valquiria]) + "\n")
                    self.cuadro_texto_final.insert(tk.END, "Métrica 2: " + str(lista_metricas_media[1][valquiria]) + "\n")
                    self.cuadro_texto_final.insert(tk.END, "Métrica 3: " + str(lista_metricas_media[2][valquiria]) + "\n")
                    self.cuadro_texto_final.insert(tk.END, "Métrica 4: " + str(lista_metricas_media[3][valquiria]) + "\n")
                    self.cuadro_texto_final.insert(tk.END, "Métrica 5: " + str(lista_metricas_media[4][valquiria]) + "\n")
                    self.cuadro_texto_final.insert(tk.END, "Métrica 6: " + str(lista_metricas_media[5][valquiria]) + "\n\n")


            



    
    def ejecutar_opcion(self, opcion):
        if opcion == "Iniciar Nueva Competición":
            self.iniciar_nueva_app()
        elif opcion == "Exportar Resultados":
            self.exportar_texto()
        elif opcion == "Exportar Valquirias":
            self.exportar()
        elif opcion == "Editar Competición":
            self.iniciar_nueva_computacion()

    
    def iniciar_nueva_app(self):

        self.ventana.destroy()  # Cerrar la ventana principal actual
        ventana = tk.Tk()



    # Crear la instancia de la interfaz
        interfaz = Interfaz(ventana)

    # Iniciar el bucle de eventos
        ventana.mainloop()



    def exportar_texto(self):
        try:
            print("EXPORTANDO TEXTO CUADRO FINAL")
            texto = self.cuadro_texto_final.get("1.0", tk.END)  # Obtener todo el texto del cuadro de texto
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                filetypes=[("Text files", ".txt"), ("All files", ".*")])
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(texto)
            messagebox.showinfo("Exportar Texto", "Texto exportado correctamnente")
        except:
            pass

    def iniciar_nueva_computacion(self):
        # Aquí llamarías a tu función existente para simular una nueva computación
        lista_sistemas = self.lista_sistemas
        lista_reglas = self.lista_reglas
        self.ventana.destroy()  # Cerrar la ventana principal actual
        ventana = tk.Tk()



    # Crear la instancia de la interfaz
        interfaz = Interfaz(ventana, lista_sistemas = lista_sistemas, lista_reglas = lista_reglas)

    # Iniciar el bucle de eventos
        ventana.mainloop()

      

    
            
            
        
        
        
    def eliminar(self):
        try:
            numero = int(self.numero_entry.get()) - 1
            del self.lista_sistemas[numero]
            del self.lista_reglas[numero]
            self.actualizar_cuadro_texto()
        except:
            mostrar_pop("Introduce una valquiria válida para eliminar")
            
        
    def generar(self):
        self.entries_generador[1] = self.entry1_generador
        self.entries_generador[2] = self.entry2_generador
        self.entries_generador[3] = self.entry3_generador
        self.entries_generador[4] = self.entry4_generador
        self.entries_generador[5] = self.entry5_generador
        self.entries_generador[6] = self.entry6_generador
        self.entries_generador[7] = self.entry7_generador
        self.entries_generador[8] = self.entry8_generador
        self.entries_generador[9] = self.entry9_generador
        self.entries_generador[10] = self.entry10_generador
        self.entries_generador[11] = self.entry11_generador
        
        
        for entrada in list(self.entries_generador.keys()):
            self.entries_generador[entrada] = self.entries_generador[entrada].get()
        mensaje_pop = ""
        try:
            num_valquirias = int(self.entries_generador[1])
            if num_valquirias < 1:
                mensaje_pop = mensaje_pop + "- El número de valquirias debe ser positivo\n"
        except:
             mensaje_pop = mensaje_pop + "- Número de valquirias erróneo\n"
        try:
            num_elementos = int(self.entries_generador[2])
            if num_elementos < 1:
                mensaje_pop = mensaje_pop + "- El número de membranas debe ser positivo\n"
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de membranas erróneo\n"

        try:
            max_conexiones = int(self.entries_generador[3])
            if max_conexiones < 1:
                mensaje_pop = mensaje_pop + "- El número de membranas hijas debe ser positivo\n"
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de membranas hijas erróneo\n"

        try:
            alfabeto = list(map(str.strip, self.entries_generador[4].split(',')))
            if alfabeto == ['']:
                mensaje_pop = mensaje_pop + "- El alfabeto no puede ser vacío\n"
        except:
            mensaje_pop = mensaje_pop + "- Alfabeto erróneo\n"

        try:
            max_objetos = int(self.entries_generador[5])
            if max_objetos<0:
                mensaje_pop = mensaje_pop + "- Número máximo de objetos por membrana debe ser positivo\n"
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de objetos por membrana erróneo\n"

        try:
            max_num_obj_lhs = int(self.entries_generador[6])
            if max_num_obj_lhs<1:
                mensaje_pop = mensaje_pop + "- Número máximo de objetos LHS debe ser positivo\n"
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de objetos LHS erróneo\n"

        try:
            max_num_obj_rhs = int(self.entries_generador[7])
            if max_num_obj_rhs<1:
                mensaje_pop = mensaje_pop + "- Número máximo de objetos RHS debe ser positivo\n"
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de objetos RHS erróneo\n"
            
        try:
            max_num_obj_padre = int(self.entries_generador[8])
            if max_num_obj_padre<0:
                mensaje_pop = mensaje_pop + "- Número máximo de objetos padre debe ser positivo\n"
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de objetos padre erróneo\n"
            
        try:
            max_num_obj_hijas = int(self.entries_generador[9])
            if max_num_obj_hijas<0:
                mensaje_pop = mensaje_pop + "- Número máximo de objetos hija debe ser positivo\n"
                
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de objetos hija erróneo\n"
            
        try:
            max_reglas= int(self.entries_generador[10])
            if max_reglas < 0:
                mensaje_pop = mensaje_pop + "- Número máximo de reglas debe ser positivo\n"
        except:
            mensaje_pop = mensaje_pop + "- Número máximo de reglas erróneo\n"
            
        try:
            max_timer= int(self.entries_generador[11])
            if max_timer < 0:
                mensaje_pop = mensaje_pop + "-Timer debe ser positivo"
        except:
            mensaje_pop = mensaje_pop + "- Timer máximo erróneo"

        if(mensaje_pop == ""):
            lista_estructuras, lista_objetos, lista_reglas = generador(num_valquirias, num_elementos, max_conexiones, alfabeto, max_objetos , max_num_obj_lhs, max_num_obj_rhs, max_num_obj_padre, max_num_obj_hijas, max_reglas, max_timer)

            sistemas_generados = [SistemaMembrana.SistemaMembrana(lista_estructuras[i], lista_objetos[i]) for i in range(len(lista_estructuras))]
            self.lista_sistemas=self.lista_sistemas + sistemas_generados
            self.lista_reglas = self.lista_reglas + lista_reglas

            self.boton_siguiente.pack(pady=(10, 0))
            self.boton_generar.pack_forget()
            self.actualizar_cuadro_texto()
            #self.cambiar_estructura()
            self.crear_estructura4()
        else:
            mostrar_pop(mensaje_pop)
            
      


            
            

        
        
        
        
        
if __name__ == "__main__":
    # Crear la ventana principal
    ventana_principal = tk.Tk()

    # Crear la instancia de la interfaz
    interfaz = Interfaz(ventana_principal)

    # Iniciar el bucle de eventos
    ventana_principal.mainloop()