import pygame
import sys
import os
from typing import Tuple, Optional
from nivel import Nivel
from jugador import Jugador
from enemigo import GestorEnemigos
from ui_premium import UI_Premium
from utils import crear_imagen_prueba
import math
from powerup import GestorPowerUps

class Juego:
    """Clase principal que maneja el juego."""
    
    def __init__(self):
        """Inicializa el juego y sus componentes."""
        pygame.init()
        
        # Configuración de pantalla
        self.ancho_total = 1000  # Ancho total incluyendo la barra lateral
        self.ancho_juego = 800   # Ancho del área de juego
        self.alto = 600
        self.pantalla = pygame.display.set_mode((self.ancho_total, self.alto))
        pygame.display.set_caption("Gals Panic")
        
        # Reloj para control de FPS
        self.reloj = pygame.time.Clock()
        self.fps = 144  # Aumentado para mayor suavidad
        self.ultimo_tiempo = pygame.time.get_ticks() / 1000.0
        
        # Componentes del juego
        self.nivel = Nivel(self.ancho_juego, self.alto, "imagenes")  # Usar ancho_juego
        self.jugador = Jugador(self.ancho_juego // 2, 10)  # Centrar en área de juego
        self.gestor_enemigos = GestorEnemigos()
        self.ui = UI_Premium(self.ancho_total, self.alto)  # Usar ancho_total
        
        # Establecer la referencia al nivel en el jugador
        self.jugador.nivel = self.nivel
        
        # Gestor de power-ups
        self.gestor_powerups = GestorPowerUps()
        
        # Estado del juego
        self.nivel_actual = 1
        self.puntuacion = 0
        self.jugando = True
        self.pausa = False
        self.mostrando_nivel_completado = False
        
        # Modo debug
        self.modo_debug = False
        
        # Estado del mouse
        self.mouse_presionado = False
        
        # Cargar primer nivel
        self.cargar_nivel(self.nivel_actual)
    
    def cargar_nivel(self, numero_nivel: int) -> None:
        """
        Carga un nivel específico.
        
        Args:
            numero_nivel (int): Número del nivel a cargar
        """
        # Reiniciar componentes
        if self.nivel.cargar_nivel(numero_nivel):
            self.gestor_enemigos = GestorEnemigos()
            self.jugador.x = self.ancho_juego // 2
            self.jugador.y = 10
            
            # Actualizar la referencia al nivel en el jugador
            self.jugador.nivel = self.nivel
            
            # Reiniciar contadores de power-ups
            self.gestor_powerups.reiniciar_contadores()
            
            # Iniciar transición
            self.ui.iniciar_transicion()
            
            print(f"Nivel {numero_nivel} cargado correctamente")
        else:
            print(f"Error al cargar el nivel {numero_nivel}")
    
    def procesar_eventos(self) -> None:
        """Procesa los eventos de entrada."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jugando = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.mostrando_nivel_completado:
                        self.nivel_actual += 1
                        self.cargar_nivel(self.nivel_actual)
                        self.mostrando_nivel_completado = False
                    else:
                        self.pausa = not self.pausa
                elif evento.key == pygame.K_F3:
                    self.modo_debug = not self.modo_debug
                    self.nivel.activar_modo_debug(self.modo_debug)
                    self.jugador.modo_debug = self.modo_debug
                    print(f"Modo debug: {'activado' if self.modo_debug else 'desactivado'}")
                # Teclas para cambiar temas
                elif evento.key == pygame.K_1:
                    self.cambiar_tema("neon_nights")
                elif evento.key == pygame.K_2:
                    self.cambiar_tema("golden_hour")
                elif evento.key == pygame.K_3:
                    self.cambiar_tema("ice_queen")
            
            # Mejorado el manejo del mouse
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if not self.pausa and not self.mostrando_nivel_completado:
                    self.mouse_presionado = True
                    if not self.jugador.invulnerable:  # Solo permitir trazado si no está invulnerable
                        self.jugador.iniciar_trazado()
                        self.nivel.iniciar_trazado(int(self.jugador.x), int(self.jugador.y))
            
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                if not self.pausa and self.mouse_presionado:
                    self.mouse_presionado = False
                    if self.jugador.trazando:
                        puntos = self.jugador.detener_trazado()
                        if puntos and len(puntos) > 2:
                            exito, enemigos_eliminados = self.nivel.procesar_trazado(puntos, self.gestor_enemigos)
                            if exito and enemigos_eliminados > 0:
                                print(f"¡Eliminados {enemigos_eliminados} enemigos!")
                                self.jugador.sonidos.reproducir_sonido('victoria')
    
    def actualizar(self) -> None:
        """Actualiza el estado del juego."""
        if self.pausa or self.mostrando_nivel_completado:
            return
        
        # Obtener tiempo transcurrido
        tiempo_actual = pygame.time.get_ticks() / 1000.0
        delta_tiempo = min(tiempo_actual - self.ultimo_tiempo, 0.05)
        self.ultimo_tiempo = tiempo_actual
        
        # Actualizar UI y jugador
        self.ui.actualizar(delta_tiempo)
        self.jugador.actualizar(delta_tiempo)
        
        # Actualizar nivel y verificar tiempo agotado
        self.nivel.actualizar(delta_tiempo)
        if self.nivel.tiempo_agotado_nivel():
            self._manejar_tiempo_agotado()
            return
        
        # Procesar entrada para movimiento
        teclas = pygame.key.get_pressed()
        dx = dy = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx -= 1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy += 1
            
        # Normalizar el vector de movimiento
        if dx != 0 or dy != 0:
            longitud = math.sqrt(dx * dx + dy * dy)
            dx /= longitud
            dy /= longitud
        
        # Actualizar jugador
        self.jugador.mover(dx, dy, delta_tiempo, self.nivel.area_segura,
                          self.ancho_juego, self.alto)
        
        # Actualizar enemigos con la posición del jugador
        self.gestor_enemigos.actualizar(self.nivel.area_segura, self.ancho_juego, self.alto,
                                      delta_tiempo, self.jugador.x, self.jugador.y)
        
        # Actualizar power-ups
        self.gestor_powerups.actualizar(delta_tiempo, self.ancho_juego, self.alto,
                                      self.jugador, self.gestor_enemigos)
        
        # Procesar colisiones con enemigos si está trazando
        if self.jugador.trazando:
            self._procesar_colisiones_enemigos()
        
        # Verificar colisiones directas con enemigos (solo si no está invulnerable)
        if not self.jugador.invulnerable:
            if self.gestor_enemigos.verificar_colisiones_jugador(
                self.jugador.x, self.jugador.y, self.jugador.radio_colision):
                self._manejar_colision_enemigo()
        
        # Verificar victoria del nivel
        if self.nivel.nivel_completado() and not self.mostrando_nivel_completado:
            self.mostrando_nivel_completado = True
            self.jugador.sonidos.reproducir_sonido('victoria')
        
        # Verificar game over
        if self.jugador.vidas <= 0:
            self.reiniciar_juego()
    
    def dibujar(self) -> None:
        """Dibuja todos los elementos del juego."""
        # Limpiar pantalla principal
        self.pantalla.fill((0, 0, 0))
        
        # Crear superficie para el área de juego
        superficie_juego = pygame.Surface((self.ancho_juego, self.alto))
        
        if self.mostrando_nivel_completado:
            # Mostrar pantalla de nivel completado
            self.ui.mostrar_nivel_completado(self.pantalla, self.nivel.imagen_fondo, self.nivel_actual)
        else:
            # Dibujar elementos del juego en la superficie de juego
            superficie_juego.fill((0, 0, 0))
            
            # Dibujar nivel
            self.nivel.dibujar(superficie_juego)
            
            # Dibujar power-ups
            self.gestor_powerups.dibujar(superficie_juego)
            
            # Dibujar enemigos
            self.gestor_enemigos.dibujar(superficie_juego, self.modo_debug)
            
            # Dibujar jugador
            self.jugador.dibujar(superficie_juego)
            
            # Copiar superficie de juego a la pantalla principal
            self.pantalla.blit(superficie_juego, (0, 0))
            
            # Dibujar UI
            self.ui.dibujar_hud(self.pantalla, self.nivel_actual,
                               self.jugador.vidas,
                               self.nivel.obtener_porcentaje_revelado(),
                               self.nivel.tiempo_restante,
                               self.modo_debug,
                               self.nivel.obtener_porcentaje_meta(),
                               self.nivel.obtener_puntaje_final())
            
            # Dibujar mensaje de pausa
            if self.pausa:
                self.ui.mostrar_mensaje(self.pantalla, "PAUSA")
        
        # Dibujar transición si está activa
        self.ui.dibujar_transicion(self.pantalla)
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def reiniciar_juego(self) -> None:
        """Reinicia el juego al estado inicial."""
        self.nivel_actual = 1
        self.puntuacion = 0
        self.jugador.vidas = 3
        self.mostrando_nivel_completado = False
        self.cargar_nivel(self.nivel_actual)
    
    def ejecutar(self) -> None:
        """Ejecuta el bucle principal del juego."""
        while self.jugando:
            self.reloj.tick(self.fps)
            self.procesar_eventos()
            self.actualizar()
            self.dibujar()
        
        pygame.quit()
        sys.exit()

    def _procesar_colisiones_enemigos(self) -> None:
        """Procesa las colisiones con los enemigos durante el trazado."""
        if not self.jugador.trazando:
            return
        
        # Obtener los puntos del trazado actual
        puntos_trazado = self.jugador.puntos_trazado
        if len(puntos_trazado) < 2:
            return
        
        # Verificar colisión con la línea completa
        if self.gestor_enemigos.verificar_colisiones_linea_completa(puntos_trazado):
            print("¡Araña impactó con la línea trazada!")
            self._manejar_colision_enemigo()
            return
        
        # Verificar colisión con el segmento actual (desde el último punto hasta la posición actual)
        ultimo_punto = puntos_trazado[-1]
        punto_actual = (self.jugador.x, self.jugador.y)
        
        # Solo verificar si el punto actual es diferente al último punto
        if ultimo_punto != punto_actual:
            if self.gestor_enemigos.verificar_colisiones_linea(ultimo_punto, punto_actual):
                print("¡Araña impactó con el segmento actual!")
                self._manejar_colision_enemigo()

    def _manejar_colision_enemigo(self) -> None:
        """Maneja la colisión con un enemigo."""
        # Quitar una vida al jugador
        self.jugador.recibir_daño()
        
        # Reproducir sonido de daño
        self.jugador.sonidos.reproducir_sonido('daño')
        
        # Limpiar el trazado actual
        self.nivel.trazado_actual = []
        self.jugador.cancelar_trazado()
        
        # Hacer al jugador temporalmente invulnerable
        self.jugador.invulnerable = True
        self.jugador.tiempo_invulnerabilidad = 0

    def cambiar_tema(self, nombre_tema: str) -> None:
        """
        Cambia el tema visual del juego.
        
        Args:
            nombre_tema (str): Nombre del tema a activar
        """
        if self.ui.theme_manager.cambiar_tema(nombre_tema):
            # Recrear assets con el nuevo tema
            self.ui._crear_assets()
            print(f"Tema cambiado a: {nombre_tema}")
        else:
            print(f"Tema no encontrado: {nombre_tema}")

    def _manejar_tiempo_agotado(self) -> None:
        """Maneja el evento de tiempo agotado en el nivel."""
        # Quitar una vida al jugador
        self.jugador.recibir_daño()
        
        # Reproducir sonido de daño
        self.jugador.sonidos.reproducir_sonido('daño')
        
        # Reiniciar el nivel actual
        self.cargar_nivel(self.nivel_actual)
        
        # Mostrar mensaje de tiempo agotado
        print("¡Tiempo agotado! Perdiste una vida")

def main():
    """Función principal del juego."""
    # Crear directorio de imágenes si no existe
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")
        print("Directorio de imágenes creado")
    
    # Crear imagen de prueba si no existe
    if not os.path.exists(os.path.join("imagenes", "nivel1.png")):
        print("Creando imagen de prueba...")
        crear_imagen_prueba()
        print("Imagen de prueba creada")
    
    # Iniciar juego
    juego = Juego()
    juego.ejecutar()

if __name__ == "__main__":
    main() 