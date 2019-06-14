from tkinter import *
from tkinter import ttk
from hashlib import sha1
from tkinter import messagebox
import tkinter.font as tkFont
import argparse, socket, threading

class Table(Frame):
    def __init__(self, parent=None, title="", headers=[], height=13, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self._title = Label(self, text=title, background="white", font=("Helvetica", 16))
        self._headers = headers
        self._tree = ttk.Treeview(self,
                                  height=height,
                                  columns=self._headers,
                                  show="headings")
        self._title.pack(side=TOP, fill="x")

        # Agregamos dos scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self._tree.xview)
        hsb.pack(side='bottom', fill='x')

        self._tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        self._tree.pack(side="top", expand=True, fill=BOTH)

        for header in self._headers:
            self._tree.heading(header, text=header.title())
            self._tree.column(header, stretch=True,
                              width=tkFont.Font().measure(header.title()))

    def add_row(self, row):
        self._tree.insert('', 'end', values=row)
        for i, item in enumerate(row):
            col_width = tkFont.Font().measure(item)
            if self._tree.column(self._headers[i], width=None) < col_width:
                    self._tree.column(self._headers[i], width=col_width)

class interfaz_grafica():
    def __init__(self,ip, puert_player, puert_admin):
        self.principal = Tk()
        self.principal.title("JaJanKen")
        self.principal.geometry("650x470")
        self.principal.resizable(False, False)
        self.principal.protocol("WM_DELETE_WINDOW", self.cerrando)
        # Coleres para la interfaz.
        self.color_btn_salir = "#FA5858"
        self.color_btn_ingresar = "#30a862"
        self.color_btn_registrar = "#58ACFA"
        self.color_btn_admin = "#F2F5A9"
        self.color_btn_tablas = "#ff9e40"
        self.color_btn_piedra = "#857460"
        self.color_btn_papel = "#ffffbf"
        self.color_btn_tijera = "#d5303e"
        self.color_label_elecci = "#f5f2f2"
        self.fondo = "#E0F2F7"

        self.principal.config(bg=self.fondo)
        self.ip = ip
        self.puert_player = puert_player
        self.puert_admin = puert_admin
        self.label_playe2 = StringVar()

        self.v_entrada()

        self.principal.mainloop()

    def cerrando(self, event=None):
        print("saliendo")
        try:
            mensaje = "saliendo/%s" % str(self.player_nombre)
            self.sock_players.send(mensaje.encode())
            self.sock_players.close()
        except:
            try:
                mensaje = "saliendo/%s" % str(self.admin_name)
                self.sock_admin.send(mensaje.encode())
                self.sock_admin.close()
            except:
                pass
        finally:
            self.principal.quit()
            #self.principal.destroy()

    def cambio_v(self, ventana=""):
        self.frame_principal.destroy()
        return eval(ventana)

    def v_entrada(self):
        self.frame_principal = Frame(self.principal, bg=self.fondo)
        self.frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=60)

        frame_bton_admin = Frame(self.frame_principal, padx=40, bg=self.fondo)
        frame_bton_admin.pack(fill=X, expand=True)
        bton_ingrso_admin = Button(frame_bton_admin,bg=self.color_btn_admin, text="Admin",command=lambda:self.cambio_v('self.v_ingreso("admin")') ,font=("Cooper Black", 12), relief=RAISED, bd=5, width=8, height=2)
        bton_ingrso_admin.pack(side=RIGHT)

        frame_fila1 = Frame(self.frame_principal, padx=60, pady=70, bg=self.fondo)
        frame_fila1.pack(fill=X, expand=True)

        btn_admin = Button(frame_fila1, text="Registro",bg=self.color_btn_registrar, font=("Cooper Black", 18), relief=RAISED, bd=5, width=10, height=2,
                           padx=30, command=lambda: self.cambio_v("self.v_registro()"))
        btn_admin.pack(side=LEFT)
        btn_ingreso = Button(frame_fila1, text="Ingreso", font=("Cooper Black", 18), relief=RAISED, bd=5, width=10,
                             height=2, padx=30,bg=self.color_btn_ingresar, command=lambda:self.cambio_v("self.v_ingreso()"))
        btn_ingreso.pack(side=RIGHT)

    def ingresar_app_admin(self):
        usuario = self.entry_usuario.get()
        contrasena = sha1(self.entry_contrasena.get().encode('utf-8')).hexdigest() ### ==== encriptación de contraseña
        if len(usuario)>0 and len(contrasena)>0:
            self.sock_admin = socket.socket()
            self.sock_admin.connect((self.ip, self.puert_admin))
            mensaje = "ingreso/admin/%s/%s" %(str(usuario.strip("")),str(contrasena.strip("")))
            print(mensaje)
            self.sock_admin.send(mensaje.encode("utf-8"))
            respuesta = str(self.sock_admin.recv(1024).decode("utf-8"))
            print(respuesta)
            respuesta = respuesta.split("/")
            if respuesta[0] == "ingresado":
                self.admin_name = respuesta[1]
                self.frame_principal.destroy()
                self.v_admin()
            elif respuesta[0] == "activo":
                messagebox.showerror("Error", "Hay un sesión activa")
                self.frame_principal.destroy()
                self.v_ingreso("admin")
            else:
                messagebox.showerror("Error", "Hubo un error, verifique:\n\n-Los datos esten correctos\n-Que seas un Administrador")
                self.frame_principal.destroy()
                self.v_ingreso("admin")

        else:
            messagebox.showwarning("Problema", "Complete todos los campos")
            self.frame_principal.destroy()
            self.v_ingreso("admin")

    def ingresar_app(self, event=None):
        usuario = self.entry_usuario.get()
        contrasena = sha1(self.entry_contrasena.get().encode('utf-8')).hexdigest() ### ==== encriptación de contraseña
        if len(usuario)>0 and len(contrasena)>0:
            self.sock_players = socket.socket()
            self.sock_players.connect((self.ip, self.puert_player))
            mensaje = "ingreso/player/%s/%s" %(str(usuario.strip("")),str(contrasena.strip("")))
            self.sock_players.send(mensaje.encode("utf-8"))
            respuesta = str(self.sock_players.recv(1024).decode("utf-8"))
            respuesta = respuesta.split("/")
            print(respuesta)
            if respuesta[0] == "ingresado":
                if respuesta[1] == "player":
                    self.player_nombre = usuario
                    self.player_puntos = respuesta[2]
                    self.frame_principal.destroy()
                    self.v_juego()
                    hilo_jugando = threading.Thread(target=self.jugando)
                    hilo_jugando.start()
                else:
                    self.player_nombre = usuario
                    self.frame_principal.destroy()
                    self.v_admin()
            elif respuesta[0] == "activo":
                messagebox.showerror("Error", "Hay un sesión activa")
                self.cambio_v("self.v_ingreso()")
            else:
                messagebox.showerror("Error", "Usuario No Registrado")
                self.cambio_v("self.v_registro()")
        else:
            messagebox.showwarning("Problema", "Complete todos los campos")
            self.cambio_v("self.v_ingreso()")

    def v_ingreso(self, tipo_user="player"):
        self.frame_principal = Frame(self.principal, bg=self.fondo)
        self.frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=160)

        frame_fila1 = Frame(self.frame_principal, padx=80, bg=self.fondo)
        frame_fila1.pack(fill=X, expand=True)
        label_usuario = Label(frame_fila1,bg=self.fondo, text="Usuario:", anchor="e", font=("Cooper Black", 12,"italic"), width=10).pack(side=LEFT)
        self.entry_usuario = Entry(frame_fila1, width=35, font=("Comic Sans MS", 12,"bold"), justify=CENTER)
        self.entry_usuario.pack(side=RIGHT)

        frame_fila2 = Frame(self.frame_principal, padx=80, bg=self.fondo)
        frame_fila2.pack(fill=X, expand=True)
        label_contrasena = Label(frame_fila2,bg=self.fondo, text="Contraseña:", anchor="e", font=("Cooper Black", 12, "italic"), width=10).pack(
            side=LEFT)
        self.entry_contrasena = Entry(frame_fila2, width=35, font=("Comic Sans MS", 12, "bold"),justify=CENTER, show="*")
        self.entry_contrasena.pack(side=RIGHT)

        frame_fila3 = Frame(self.frame_principal, padx=130, bg=self.fondo)
        frame_fila3.pack(fill=X, expand=True)
        btn_salir = Button(frame_fila3, width=12, height=2, text="SALIR",bg=self.color_btn_salir, font=("Cooper Black", 12, "italic"), command=lambda: self.cerrando()).pack(side=LEFT)
        if tipo_user == "player":
            btn_ingreso_juego = Button(frame_fila3,bg=self.color_btn_ingresar, width=12, height=2, text="INGRESAR", font=("Cooper Black", 12, "italic"), command= lambda: self.ingresar_app()).pack(side=RIGHT)
        else:
            btn_ingreso_juego = Button(frame_fila3,bg=self.color_btn_ingresar, width=12, height=2, text="INGRESAR", font=("Cooper Black", 12, "italic"), command= lambda: self.ingresar_app_admin()).pack(side=RIGHT)

    def v_registro(self):
        self.frame_principal = Frame(self.principal, bg=self.fondo)
        self.frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=130)

        frame_fila1 = Frame(self.frame_principal,  padx=80, bg=self.fondo)
        frame_fila1.pack(fill=X, expand=True)
        label_nombre = Label(frame_fila1, text="Nombre:",bg=self.fondo, anchor="e", font=("Cooper Black", 12, "italic"), width=10).pack(
            side=LEFT)
        self.entry_nombre = Entry(frame_fila1, width=35, font=("Comic Sans MS", 12, "bold"), justify=CENTER)
        self.entry_nombre.pack(side=RIGHT)

        frame_fila2 = Frame(self.frame_principal,  padx=80, bg=self.fondo)
        frame_fila2.pack(fill=X, expand=True)
        label_usuario = Label(frame_fila2, text="Usuario:",bg=self.fondo, anchor="e", font=("Cooper Black", 12, "italic"), width=10).pack(
            side=LEFT)
        self.entry_usuario = Entry(frame_fila2, width=35, font=("Comic Sans MS", 12, "bold"), justify=CENTER)
        self.entry_usuario.pack(side=RIGHT)

        frame_fila3 = Frame(self.frame_principal, padx=80, bg=self.fondo)
        frame_fila3.pack(fill=X, expand=True)
        label_contrasena = Label(frame_fila3,bg=self.fondo, text="Contraseña:", anchor="e", font=("Cooper Black", 12, "italic"),
                                 width=10).pack(
            side=LEFT)
        self.entry_contrasena = Entry(frame_fila3, width=35, font=("Comic Sans MS", 12, "bold"), justify=CENTER, show="*")
        self.entry_contrasena.pack(side=RIGHT)

        frame_fila4 = Frame(self.frame_principal,  padx=130, bg=self.fondo)
        frame_fila4.pack(fill=X, expand=True)
        btn_salir = Button(frame_fila4, width=12, height=2, text="SALIR",bg=self.color_btn_salir, font=("Cooper Black", 12, "italic"), command=lambda: self.cerrando()).pack(side=LEFT)
        btn_ingreso_juego = Button(frame_fila4,bg=self.color_btn_registrar, width=12, height=2, text="REGISTRAR",
                                   font=("Cooper Black", 12, "italic"), command=lambda: self.registrar_app()).pack(side=RIGHT)

    def registrar_app(self):
        self.sock_players = socket.socket()
        self.sock_players.connect((self.ip, self.puert_player))
        nombre = str(self.entry_nombre.get()).strip()
        usuario = str(self.entry_usuario.get()).strip()
        contrasena = str(sha1(self.entry_contrasena.get().encode('utf-8')).hexdigest()).strip() ### ==== encriptación de contraseña
        if len(nombre)>0 and len(usuario)>0 and len(contrasena)>0:
            mensaje = "registro/%s/%s/%s" %(str(nombre.strip("")),str(usuario.strip("")),str(contrasena.strip("")))
            self.sock_players.send(mensaje.encode("utf-8"))
            print(mensaje)
            respuesta = self.sock_players.recv(1024).decode("utf-8")
            print(respuesta)
            if respuesta == "agregado":
                messagebox.showinfo("Info", "Usuario Creado")
                self.player_nombre = usuario
                self.player_puntos = 0
                self.frame_principal.destroy()
                self.v_juego()
                hilo_jugando = threading.Thread(target=self.jugando)
                hilo_jugando.start()
            else:
                messagebox.showerror("Error", "Usuario No Creado")
                self.cambio_v("self.v_entrada()")
        else:
            messagebox.showwarning("Problema", "Complete todos los campos")
            self.cambio_v("self.v_registro()")

    def jugando(self):
        self.sock_players.send("esperando/".encode())
        try:
            while True:
                mensaje = str(self.sock_players.recv(1024).decode("utf-8"))
                mensaje = mensaje.split("/")
                print(mensaje)
                if mensaje[0]=="run_juego": #mensaje[0]->run juego, mensaje[1]->oponente
                    self.label_player2 = (mensaje[1])
                    self.cambio_v('self.v_juego("self.fram_jugando()",self.label_player2)')
                if mensaje[0]=="fin_juego":  #mensaje[0]->fin_juego, mensaje[1]->resultado, mensaje[2]->eleccion j1, mensaje[3]->eleccion j2, mensaje[4]-> jugador 1 o 2
                    self.fram_ganador(self.texto_resultado(int(mensaje[1]),int(mensaje[4])), self.obtener_figura(mensaje[2]), self.obtener_figura(mensaje[3]))
                if mensaje[0]=="error":
                    self.frame_puntos.destroy()
                    texto_resultado = "%s se ha retirado" % mensaje[1]
                    self.frame_fila2.destroy()
                    self.fram_ganador(texto_resultado,"","",False)
                    self.sock_players.close()
                    break
        except Exception:
            return

    def v_juego(self, funcion="self.fram_esperando()", player2=""):
        self.frame_principal = Frame(self.principal, bg=self.fondo)
        self.frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=30)

        self.frame_fila1 = Frame(self.frame_principal, padx=50, bg=self.fondo)
        self.frame_fila1.pack(fill=X, side=TOP)
        label_player1 = Label(self.frame_fila1,bg=self.fondo, text=self.player_nombre, anchor="e", font=("Cooper Black", 20), width=10).pack(side=LEFT)
        label_vs = Label(self.frame_fila1,bg=self.fondo, text="vs", font=("Cooper Black", 20, "italic"), width=10).pack(side=LEFT)
        label_player2 = Label(self.frame_fila1,bg=self.fondo, text=player2, anchor="w", font=("Cooper Black", 20), width=10).pack(side=LEFT)

        eval(funcion)

    def fram_esperando(self):
        self.frame_fila2 = Frame(self.frame_principal, padx=30, bg=self.fondo)
        self.frame_fila2.pack(fill=X, expand=True, side=TOP)
        label_esperando = Label(self.frame_fila2,bg=self.fondo, text="Esperando Oponente...", font=("Comic Sans MS", 25, "italic")).pack(
            side=LEFT)


        self.frame_puntos = Frame(self.frame_principal, padx=20, bg=self.fondo)
        self.frame_puntos.pack(fill=X, side=TOP)
        puntaje = "Tienes: (%s puntos)" % str(self.player_puntos)
        self.label_puntos = Label(self.frame_puntos,bg=self.fondo, text=puntaje, font=("Cooper Black", 12, "italic")).pack(side=LEFT)

    def act_btn_eleccion(self, eleccion):
        self.frame_fila2.destroy()
        self.frame_puntos.destroy()
        mensaje = "eleccion/%s" % str(eleccion)
        self.sock_players.send(mensaje.encode())

    def fram_jugando(self):
        self.frame_fila2 = Frame(self.frame_principal, padx=60, bg=self.fondo)
        self.frame_fila2.pack(fill=X, expand=True)
        btn_piedra = Button(self.frame_fila2, text="PIEDRA",bg=self.color_btn_piedra, command=lambda:self.act_btn_eleccion("Pi"), font=("Comic Sans MS", 25, "italic"), width=8, heigh=2).pack(
            side=LEFT)
        label_en_blanco = Label(self.frame_fila2,bg=self.fondo, text=" ").pack(side=LEFT, fill=Y)
        btn_papel = Button(self.frame_fila2, text="PAPEL",bg=self.color_btn_papel, command=lambda:self.act_btn_eleccion("Pa"), font=("Comic Sans MS", 25, "italic"),width=8,heigh=2).pack(
            side=LEFT)
        label_en_blanco = Label(self.frame_fila2,bg=self.fondo, text=" ").pack(side=LEFT, fill=Y)
        btn_tijera = Button(self.frame_fila2, text="TIJERA",bg=self.color_btn_tijera, command=lambda:self.act_btn_eleccion("T"), font=("Comic Sans MS", 25, "italic"),width=8,heigh=2).pack(
            side=LEFT)

        self.frame_puntos = Frame(self.frame_principal, padx=20, bg=self.fondo)
        self.frame_puntos.pack(fill=X, side=TOP)
        puntaje = "Tienes: (%s puntos)" % str(self.player_puntos)
        self.label_puntos = Label(self.frame_puntos,bg=self.fondo, text=puntaje, font=("Cooper Black", 12, "italic")).pack(side=LEFT)

    def obtener_figura(self, texto):
        if texto == "Pa":
            figura = "✋"
        elif texto == "Pi":
            figura = "✊"
        else:
            figura = "✌"
        return figura


    def fram_ganador(self, txt_ganador="", eleccion_player1="",  eleccion_player2="", noError = True):
        frame_fila2 = Frame(self.frame_principal, padx=120, bg=self.fondo)
        frame_fila2.pack(fill=X, expand=True)
        if noError:
            label_eleccion_player1 = Label(frame_fila2,bg=self.color_label_elecci, text=eleccion_player1, font=("Arial", 93), width=2, heigh=1).pack(
                side=LEFT)
            label_vs = Label(frame_fila2, text="vs",bg = self.color_label_elecci, font=("Comic Sans MS", 25, "italic"), width=5, heigh=3).pack(
                side=LEFT)
            label_eleccion_player2 = Label(frame_fila2,bg=self.color_label_elecci, text=eleccion_player2, font=("Arial", 93), width=2, heigh=1).pack(
                side=LEFT)

        frame_fila3 = Frame(self.frame_principal, padx=100, bg=self.fondo)
        frame_fila3.pack(fill=X, expand=True)
        label_ganador = Label(frame_fila3,bg=self.fondo, text=txt_ganador, font=("Comic Sans MS", 20, "italic"),
                              width=40).pack(
            side=LEFT)

        self.frame_puntos = Frame(self.frame_principal, padx=20, bg=self.fondo)
        self.frame_puntos.pack(fill=X, side=TOP)
        puntaje = "Tienes: (%s puntos)" % str(self.player_puntos)
        self.label_puntos = Label(self.frame_puntos,bg=self.fondo, text=puntaje, font=("Cooper Black", 12, "italic")).pack(side=LEFT)

        self.frame_fila4 = Frame(self.frame_principal, padx=140, bg=self.fondo)
        self.frame_fila4.pack(fill=X, expand=False, side=BOTTOM)


        if noError:
            btn_jugar=Button(self.frame_fila4, text="VOLVER A JUGAR",bg=self.color_btn_ingresar, command=lambda: self.cambio_v("self.v_juego('self.fram_jugando()', self.label_player2)"), width=16, heigh=1, font=("Cooper Black", 16)).pack(side=LEFT)
            btn_atras=Button(self.frame_fila4, text="SALIR", width=7, heigh=1,bg=self.color_btn_salir, font=("Cooper Black", 16), command=lambda: self.cerrando()).pack(side=RIGHT)
        else:
            btn_atras=Button(self.frame_fila4, text="SALIR", width=7, heigh=1,bg=self.color_btn_salir, font=("Cooper Black", 16), command=lambda: self.cerrando()).pack(side=RIGHT)


    def texto_resultado(self, resultado, jugador):
        texto = ""
        if resultado == 0:
            texto="¡Empate! (+ 5 puntos)"
            self.player_puntos = int(self.player_puntos) + 5
        elif resultado == jugador:
            texto="¡Eres el Ganador! (+ 10 puntos)"
            self.player_puntos = int(self.player_puntos) + 10
        elif resultado != jugador:
            texto="¡Eres el Perdedor! (+ 0 puntos)"
        return texto

    def v_admin(self):
        self.frame_principal = Frame(self.principal, bg=self.fondo)
        self.frame_principal.pack(fill=BOTH, expand=True, padx=5, pady=90)

        frame_fila1 = Frame(self.frame_principal, padx=15, bg=self.fondo)
        frame_fila1.pack(fill=X, side=TOP)
        label_administracion = Label(frame_fila1,bg=self.fondo, text="Estadísticas", anchor="w", font=("Cooper Black", 15)).pack(side=LEFT)

        frame_fila2 = Frame(self.frame_principal, padx=15, pady=30, bg=self.fondo)
        frame_fila2.pack(fill=X, expand=True)

        btn_jugadores = Button(frame_fila2,bg=self.color_btn_tablas, text="Jugadores", font=("Cooper Black", 17), relief=RAISED, bd=5, width=7, height=2,
                           padx=30, command=lambda: self.toplevel("jugadores"))
        btn_jugadores.grid(row=0, column=0, )
        btn_mejor_jugador = Button(frame_fila2,bg=self.color_btn_tablas, text="Mejores jugadores", font=("Cooper Black", 17), relief=RAISED, bd=5, width=11,
                             height=2, padx=30, command=lambda: self.toplevel("mejor_jugador"))
        btn_mejor_jugador.grid(row=0, column=1)
        btn_juego = Button(frame_fila2,bg=self.color_btn_tablas, text="Juegos", font=("Cooper Black", 17), relief=RAISED, bd=5, width=7,
                             height=2, padx=30, command=lambda: self.toplevel("juegos"))
        btn_juego.grid(row=0, column=2)

        frame_fila3 = Frame(self.frame_principal, padx=140, pady=30, bg=self.fondo)
        frame_fila3.pack(fill=X, expand=False, side=BOTTOM)
        btn_atras = Button(frame_fila3, text="SALIR",bg=self.color_btn_salir, width=7, heigh=1,relief=RAISED, bd=5, font=("Cooper Black", 14),
                           command=lambda: self.cerrando()).pack(side=RIGHT)

    def toplevel(self, tabla):
        toplevel = Toplevel()
        toplevel.focus_set()
        toplevel.grab_set()
        toplevel.title("Estadisticas")
        root_width = self.principal.winfo_width()
        root_pos_x = self.principal.winfo_x()
        root_pos_y = self.principal.winfo_y()
        position = '650x470' + '+' + str(root_pos_x + int(root_width* 0.8)) + '+' + str(root_pos_y)
        toplevel.geometry(position)
        toplevel.resizable(False,False)
        if tabla == "jugadores":
            self.tabla_jugadores(toplevel)
        elif tabla == "juegos":
            self.tabla_juegos(toplevel)
        else:
            self.tabla_mejor_jugador(toplevel)

    def tabla_mejor_jugador(self, toplevel):
        encabezados = ["Nombre", "Usuario", "Puntos"]
        jugadores_table = Table(toplevel, title="TOP 3 JUGADORES", headers=encabezados)
        jugadores_table.pack(fill=BOTH, expand=True)

        registros = self.obtener_registros("mejor_jugador")
        print(registros)
        for row in registros:
            jugadores_table.add_row(row)

    def tabla_jugadores(self, toplevel):
        encabezados = ("Id", "Nombre", "Usuario", "Puntos", "Rol")
        jugadores_table = Table(toplevel, title="JUGADORES", headers=encabezados)
        jugadores_table.pack(fill=BOTH, expand=True)

        registros = self.obtener_registros("jugadores")
        for row in registros:
            jugadores_table.add_row(row)

    def tabla_juegos(self, toplevel):
        encabezados = ("Id", "Jugador 1", "Juagador 2", "Resultado")
        jugadores_table = Table(toplevel, title="JUEGOS", headers=encabezados)
        jugadores_table.pack(fill=BOTH, expand=True)

        registros = self.obtener_registros("juegos")
        for row in registros:
            jugadores_table.add_row(row)

    def obtener_registros(self, tabla):
        mensaje = "registros_bd/%s" % str(tabla)
        self.sock_admin.send(mensaje.encode("utf-8"))
        respuesta = str(self.sock_admin.recv(1024).decode("utf-8"))
        registros = eval(respuesta)
        return registros

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="Dirección Ip del servidor", default="localhost")
    parser.add_argument("-p", type=int, help="Puerto del Servidor", default=10000)
    args = parser.parse_args()

    try:
        puerto_jugador = args.p
        puerto_admin = puerto_jugador + 1
        direccion_ip = args.a
        nuevo_juego = interfaz_grafica(direccion_ip, puerto_jugador, puerto_admin)

    except Exception:
        return

if __name__ == '__main__':
    main()