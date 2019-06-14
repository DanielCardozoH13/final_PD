#!/usr/bin/env python3
import socket, threading, argparse, mysql.connector

class Player:
    def __init__(self, id, name, conn, address, puntos=0):
        self.id = id
        self.name = name
        self.conn = conn
        self.address = address
        self.choice = "" #eleccion (piedra, papel, tijera)
        self.puntos = puntos

class Juego():
    def __init__(self, puert, direccionIp):
        try:
            self.socket_jugadores = socket.socket()  # socket para jugadores
            self.socket_jugadores.bind((direccionIp, puert))
            self.socket_jugadores.listen(10)

            puert_adm = puert + 1
            self.socket_admin = socket.socket()
            self.socket_admin.bind((direccionIp, puert_adm))
            self.socket_admin.listen(10)

            hilo_jugadores = threading.Thread(target=self.hilos_para_jugadores)
            hilo_jugadores.start()

            hilo_admins = threading.Thread(target=self.hilo_admin)
            hilo_admins.start()
        except Exception as e:
            print(e)
            return

    def hilo_admin(self):
        try:
            conn_adm, address_adm = self.socket_admin.accept()
            print("se ha conectado un Administrador %s" % str(address_adm))
            while True:
                try:
                    mensaje_admin = str(conn_adm.recv(1024).decode())
                    self.dar_respuesta(mensaje_admin, conn_adm, Player)
                except Exception as e:
                    print(e)
                    break
        except Exception as e:
            print(e)
            return

    def hilos_para_jugadores(self):
        print("Esperando Conexiones")
        next_id = 1
        while True:
            try:
                try:
                    conn, address = self.socket_jugadores.accept()
                    player1 = Player(next_id, "Player 1", conn, address)
                    print("Se conecto el jugador 1: " + str(address))
                    mensaje1 = str(player1.conn.recv(1024).decode("utf-8"))
                    self.dar_respuesta(mensaje1, conn, player1)
                    next_id = next_id + 1

                except Exception as e:
                    print(e)
                    break
                try:

                    conn, address = self.socket_jugadores.accept()
                    player2 = Player(next_id, "Player 2", conn, address)
                    print("Se conecto el jugador 2: " + str(address))
                    mensaje2 = str(player2.conn.recv(1024).decode())
                    self.dar_respuesta(mensaje2, conn, player2)
                    next_id = next_id + 1
                except Exception as e:
                    print(e)
                    try:
                        print("el jugador 2 salio")
                        break
                    except:
                        break
                gt = GameThread(player1, player2)
                gt.start()
            except Exception as e:
                print(e)
                pass


    def conexion_bd(self):
        conexion = mysql.connector.connect(user="root", password="", host="localhost",
                                                database="juego_piedra_papel_tijera")
        cursor = conexion.cursor()

        return (conexion,cursor)

    def cambiar_estado(self, jugador):
        try:
            conexion, cursor = self.conexion_bd()
            sql = "UPDATE jugadores SET Estado='inactivo' WHERE Usuario = '%s'" % (str(jugador))
            cursor.execute(sql)
            conexion.commit()
        except Exception as e:
            print(e)
            return

    def dar_respuesta(self, mensaje, direccion_ip, player):
        try:
            if len(mensaje)>0:
                mensaje = mensaje.split("/")
                conexion, cursor = self.conexion_bd()
                respuesta = ""
                print(mensaje)
                if mensaje[0] == "registro":
                    try:
                        sql = "INSERT INTO jugadores (Nombre, Usuario, Contrasena,Rol, Estado) VALUES ('%s','%s','%s','player','activo')" % (
                        mensaje[1], mensaje[2], mensaje[3])
                        cursor.execute(sql)
                        conexion.commit()
                        respuesta = "agregado"
                        player.name = mensaje[2]
                        player.puntos = 0
                    except:
                        respuesta = "no agregado"
                elif mensaje[0] == "ingreso":
                    try:
                        sql = "SELECT * FROM jugadores WHERE Usuario = '" + mensaje[2] + "' AND Contrasena = '" + mensaje[
                            3] + "' AND Rol = '%s' " % mensaje[1]
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if len(result) > 0:
                            for datos in result:
                                datosl = datos
                            if datosl[6] == "inactivo":
                                sql = "UPDATE jugadores SET Estado='activo' WHERE Usuario = '%s'" % str(mensaje[2])
                                cursor.execute(sql)
                                conexion.commit()
                                if datosl[5] == "player":
                                    respuesta = "ingresado/player/%i" % int(datosl[4])
                                    player.name = datosl[2]
                                    player.puntos = datos[4]
                                else:
                                    respuesta = "ingresado/admin"
                            else:
                                respuesta = "activo"
                        else:
                            respuesta="no ingreso"

                    except:
                        respuesta = "no ingresado"

                elif mensaje[0] == "registros_bd":
                    try:
                        if mensaje[1] == "juegos":
                            sql = "SELECT Codigo, Jugador1, Jugador2, Resultado FROM %s" % mensaje[1]
                        elif mensaje[1] == "jugadores":
                            sql = "SELECT Codigo, Nombre, Usuario, Puntos, Rol FROM %s" % mensaje[1]
                        else:
                            sql = "SELECT Nombre, Usuario, Puntos FROM jugadores ORDER BY Puntos DESC LIMIT 3"
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        respuesta=str(result)
                    except:
                        respuesta = "no registros"
                elif mensaje[0] == "saliendo":
                    self.cambiar_estado(mensaje[1])
                direccion_ip.send(respuesta.encode("utf-8"))
        except Exception as e:
            print(e)



class GameThread (threading.Thread):
    def __init__(self, player1, player2):
        threading.Thread.__init__(self)

        self.player1 = player1
        self.player2 = player2

    def run(self):
        while True:
            try:
                respuesta1 = str(self.player1.conn.recv(1024).decode())
                respuesta2 = str(self.player2.conn.recv(1024).decode())
                respuesta1 = respuesta1.split("/")
                respuesta2 = respuesta2.split("/")
                print(respuesta1)
                print(respuesta2)
                if respuesta1[0] == "esperando" and respuesta2[0] == "esperando":
                    mensaje1 = "run_juego/%s" % str(self.player2.name)  # se envia mensaje para iniciar el juego
                    mensaje2 = "run_juego/%s" % str(self.player1.name)  # se envia mensaje para iniciar el juego
                    self.player1.conn.send(mensaje1.encode("utf-8"))
                    self.player2.conn.send(mensaje2.encode("utf-8"))
                    pass
                elif respuesta1[0] == "eleccion" and respuesta2[0] == "eleccion":
                    self.player1.choice = respuesta1[1]
                    self.player2.choice = respuesta2[1]
                    ganador = int(self.obtener_ganador(str(self.player1.choice), str(self.player2.choice)))
                    #self.dar_puntuacion(ganador)
                    self.guardar_juego([self.player1,self.player2],int(ganador))
                    mensaje = "fin_juego/%i/%s/%s/1" % (ganador,str(self.player1.choice),str(self.player2.choice))
                    self.player1.conn.send(mensaje.encode("utf-8"))
                    mensaje = "fin_juego/%i/%s/%s/2" % (ganador,str(self.player2.choice),str(self.player1.choice))
                    self.player2.conn.send(mensaje.encode("utf-8"))
            except:
                self.actualizar_estado(self.player1.name)
                self.actualizar_estado(self.player2.name)
                try:
                    try:
                        mensaje = "error/%s" % (str(self.player2.name))
                        self.player1.conn.send(mensaje.encode("utf-8"))
                        print("El jugador 2 salio: (%s)" % (str(self.player2.conn)))
                        self.actualizar_estado(self.player2.name)
                        break
                    except:
                        try:
                            mensaje = "error/%s" % (str(self.player1.name))
                            self.player2.conn.send(mensaje.encode("utf-8"))
                            print("El jugador 1 salio: (%s)" % (str(self.player1.conn)))
                            self.actualizar_estado(self.player1.name)
                        except:
                            break
                    break
                except:
                    try:
                        self.player1.conn.close()
                        self.player2.conn.close()
                    finally:
                        break
    def obtener_ganador(self, player1_choice, player2_choice):
        victoria = 10
        empate = 5
        derrota = 0
        # jugadores empate
        if player1_choice == player2_choice:
            return 0
        #T=tijera ,Pa=papel,Pi=piedra
        if player1_choice == "Pi":
            if player2_choice == "T":
                return 1
            if player2_choice == "Pa":
                return 2

        if player1_choice == "Pa":
            if player2_choice == "Pi":
                return 1
            if player2_choice == "T":
                return 2

        if player1_choice == "T":
            if player2_choice == "Pa":
                return 1
            if player2_choice == "Pi":
                return 2

        # operaticion invalida
        return 3
    def dar_puntuacion(self, resultado_juego):
        victoria = 10
        empate = 5
        derrota = 0
        if resultado_juego == 0:
            self.player1.puntos = self.player1.puntos + empate
            self.player2.puntos = self.player2.puntos + empate
        elif resultado_juego == 1:
            self.player1.puntos = self.player1.puntos + victoria
            self.player2.puntos = self.player2.puntos + derrota
        else:
            self.player1.puntos = self.player1.puntos + derrota
            self.player2.puntos = self.player2.puntos + victoria
    def conexionbd(self):
        conexion = mysql.connector.connect(user="root", password="", host="localhost",
                                           database="juego_piedra_papel_tijera")
        cursor = conexion.cursor()
        return conexion, cursor

    def guardar_juego(self, players, ganador):
        self.dar_puntuacion(int(ganador))
        try:
            conexion, cursor = self.conexionbd()
            for player in players:
                sql = "UPDATE jugadores SET Puntos='%i' WHERE Usuario = '%s'" % (player.puntos, str(player.name))
                cursor.execute(sql)
                #self.conn.commit()
            sql2 = "INSERT INTO juegos (Jugador1, Jugador2, Resultado) VALUES ('%s','%s',%i)" % (
                players[0].name, players[1].name, ganador)
            cursor.execute(sql2)
            conexion.commit()
        except Exception as e:
            print(e)
            return

    def actualizar_estado(self, jugador):
        try:
            conexion, cursor = self.conexionbd()
            sql = "UPDATE jugadores SET Estado='inactivo' WHERE Usuario = '%s'" % (str(jugador))
            cursor.execute(sql)
            conexion.commit()
        except Exception as e:
            print(e)
            return




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="server IP address", default="localhost")
    parser.add_argument("-p", type=int, help="server port", default=10000)
    args = parser.parse_args()

    PiedraPapleTijeras = Juego(args.p, args.a)

if __name__ == '__main__':
    main()
