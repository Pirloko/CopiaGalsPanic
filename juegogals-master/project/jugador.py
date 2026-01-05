import pygame
import math
from typing import Tuple, List, Optional
import random
from sonidos import GestorSonidos

class Jugador:
    """Clase que maneja el comportamiento del jugador."""
    
    def __init__(self, x: float, y: float, velocidad: float = 35.0):
        """
        Inicializa el jugador.
        
        Args:
            x (float): Posición inicial X
            y (float): Posición inicial Y
            velocidad (float): Velocidad de movimiento
        """
        self.x = x
        self.y = y
        self.velocidad = velocidad
        
        # Dimensiones y colisión
        self.radio = 8
        self.radio_colision = 6
        
        # Estado de movimiento
        self.dx = 0
        self.dy = 0
        self.aceleracion = 60.0  # Aumentada de 20.0 a 60.0 (x3)
        self.desaceleracion = 13.5  # Aumentada de 4.5 a 13.5 (x3)
        self.velocidad_maxima = velocidad * 5.0  # Ya multiplicada por la velocidad base aumentada
        
        # Factores de easing para movimiento suave
        self.easing_factor = 0.25  # Aumentado para respuesta más inmediata
        self.velocidad_actual = 0.0
        self.angulo_movimiento = 0.0
        
        # Estado del trazado
        self.trazando = False
        self.puntos_trazado: List[Tuple[float, float]] = []
        self.ultimo_punto_valido: Optional[Tuple[float, float]] = None
        self.distancia_min_puntos = 2.0
        self.punto_prediccion: Optional[Tuple[float, float]] = None
        self.distancia_prediccion = 60.0
        self.min_distancia_puntos = 10  # Distancia mínima entre puntos del trazado
        
        # Efectos visuales mejorados
        self.color_base = (0, 255, 255)  # Cyan
        self.color_trazado = (0, 200, 255)  # Cyan más claro
        self.color_prediccion = (0, 255, 0)  # Verde
        self.color_estela = (0, 150, 255, 128)  # Cyan semi-transparente
        
        # Sistema de partículas para la estela
        self.particulas: List[dict] = []
        self.max_particulas = 60  # Aumentado para estela más larga
        self.tiempo_spawn_particula = 0
        self.intervalo_spawn_particula = 0.008  # Reducido para más partículas
        
        # Efectos de brillo
        self.brillo_alpha = 0
        self.direccion_brillo = 1
        self.velocidad_brillo = 4
        
        # Estado del jugador
        self.vidas = 3
        self.invulnerable = False
        self.tiempo_invulnerabilidad = 0
        self.duracion_invulnerabilidad = 3.0  # Aumentado de 2.0 a 3.0 segundos
        self.frecuencia_parpadeo = 8.0  # Frecuencia de parpadeo durante invulnerabilidad
        
        # Modo debug
        self.modo_debug = False
        
        # Gestor de sonidos
        self.sonidos = GestorSonidos()
        
        # Estado del escudo
        self.tiene_escudo = False
        self.tiempo_escudo = 0
        self.duracion_escudo = 0
        self.color_escudo = (0, 191, 255)  # Azul cielo
        self.alpha_escudo = 128
        self.radio_escudo = self.radio * 1.5
        
        # Referencia al nivel actual
        self.nivel = None
    
    def _aplicar_easing(self, actual: float, objetivo: float, factor: float) -> float:
        """
        Aplica una función de easing para suavizar el movimiento.
        
        Args:
            actual (float): Valor actual
            objetivo (float): Valor objetivo
            factor (float): Factor de suavizado (0-1)
            
        Returns:
            float: Valor suavizado
        """
        return actual + (objetivo - actual) * factor
    
    def mover(self, dx: float, dy: float, delta_tiempo: float,
              area_segura: List[Tuple[int, int]], ancho: int, alto: int) -> None:
        """
        Mueve al jugador según la entrada.
        
        Args:
            dx (float): Dirección X (-1 a 1)
            dy (float): Dirección Y (-1 a 1)
            delta_tiempo (float): Tiempo transcurrido desde el último frame
            area_segura (List[Tuple[int, int]]): Lista de puntos seguros
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        # Calcular dirección de movimiento
        if dx != 0 or dy != 0:
            # Calcular ángulo de movimiento
            self.angulo_movimiento = math.atan2(dy, dx)
            
            # Aplicar aceleración con easing
            velocidad_objetivo = self.velocidad_maxima
            self.velocidad_actual = self._aplicar_easing(
                self.velocidad_actual,
                velocidad_objetivo,
                self.easing_factor
            )
        else:
            # Aplicar desaceleración con easing
            self.velocidad_actual = self._aplicar_easing(
                self.velocidad_actual,
                0,
                self.easing_factor * 2
            )
        
        # Calcular componentes de velocidad
        if self.velocidad_actual > 0.1:  # Umbral mínimo de movimiento
            self.dx = math.cos(self.angulo_movimiento) * self.velocidad_actual
            self.dy = math.sin(self.angulo_movimiento) * self.velocidad_actual
        else:
            self.dx = self.dy = 0
        
        # Calcular nueva posición
        nueva_x = self.x + self.dx * delta_tiempo
        nueva_y = self.y + self.dy * delta_tiempo
        
        # Mantener dentro de los límites
        nueva_x = max(self.radio + 1, min(ancho - self.radio - 1, nueva_x))
        nueva_y = max(self.radio + 1, min(alto - self.radio - 1, nueva_y))
        
        # Actualizar posición
        self.x = nueva_x
        self.y = nueva_y
        
        # Actualizar sistema de partículas
        self._actualizar_particulas(delta_tiempo)
        
        # Actualizar trazado si está activo
        if self.trazando:
            self._actualizar_trazado()
    
    def _actualizar_particulas(self, delta_tiempo: float) -> None:
        """
        Actualiza el sistema de partículas de la estela.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        # Generar nuevas partículas si hay movimiento
        self.tiempo_spawn_particula += delta_tiempo
        if self.velocidad_actual > 1.0 and self.tiempo_spawn_particula >= self.intervalo_spawn_particula:
            self.tiempo_spawn_particula = 0
            if len(self.particulas) < self.max_particulas:
                # Crear nueva partícula
                particula = {
                    'x': self.x,
                    'y': self.y,
                    'vida': 1.0,
                    'velocidad': random.uniform(0.3, 0.7),
                    'angulo': self.angulo_movimiento + random.uniform(-0.5, 0.5),
                    'tamaño': random.uniform(2, 4)
                }
                self.particulas.append(particula)
        
        # Actualizar partículas existentes
        for particula in self.particulas[:]:
            particula['vida'] -= delta_tiempo * 2
            if particula['vida'] <= 0:
                self.particulas.remove(particula)
                continue
            
            # Mover partícula
            particula['x'] -= math.cos(particula['angulo']) * particula['velocidad']
            particula['y'] -= math.sin(particula['angulo']) * particula['velocidad']
    
    def _dibujar_particulas(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja las partículas de la estela.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        """
        for particula in self.particulas:
            alpha = int(255 * particula['vida'])
            color = (*self.color_estela[:3], alpha)
            pygame.draw.circle(
                pantalla,
                color,
                (int(particula['x']), int(particula['y'])),
                int(particula['tamaño'] * particula['vida'])
            )
    
    def _actualizar_trazado(self) -> None:
        """Actualiza los puntos del trazado actual."""
        punto_actual = (self.x, self.y)
        if self.ultimo_punto_valido is None:
            self.ultimo_punto_valido = punto_actual
            return
        
        # Calcular distancia al último punto
        dx = punto_actual[0] - self.ultimo_punto_valido[0]
        dy = punto_actual[1] - self.ultimo_punto_valido[1]
        distancia = math.sqrt(dx * dx + dy * dy)
        
        # Añadir punto solo si está lo suficientemente lejos
        if distancia >= self.distancia_min_puntos:
            self.puntos_trazado.append(punto_actual)
            self.ultimo_punto_valido = punto_actual
            
        # Actualizar punto de predicción
        self.punto_prediccion = self._encontrar_punto_cercano()
    
    def _encontrar_punto_cercano(self) -> Optional[Tuple[float, float]]:
        """
        Encuentra el punto más cercano del trazado dentro de un radio.
        
        Returns:
            Optional[Tuple[float, float]]: Punto más cercano o None si no hay ninguno
        """
        if len(self.puntos_trazado) < 3:
            return None
            
        # Ignorar los últimos puntos para evitar conexiones no deseadas
        puntos_a_verificar = self.puntos_trazado[:-2]
        pos_actual = (self.x, self.y)
        
        punto_mas_cercano = None
        distancia_minima = self.distancia_prediccion
        
        for punto in puntos_a_verificar:
            dx = punto[0] - pos_actual[0]
            dy = punto[1] - pos_actual[1]
            distancia = math.sqrt(dx * dx + dy * dy)
            
            if distancia < distancia_minima:
                distancia_minima = distancia
                punto_mas_cercano = punto
        
        return punto_mas_cercano
    
    def detener_trazado(self) -> List[Tuple[float, float]]:
        """
        Detiene el trazado actual normalmente.
        
        Returns:
            List[Tuple[float, float]]: Lista de puntos del trazado
        """
        if not self.trazando:
            return []
            
        self.trazando = False
        
        # Si hay un punto de predicción, usarlo como punto final
        if self.punto_prediccion is not None:
            self.puntos_trazado.append(self.punto_prediccion)
        else:
            # Añadir el último punto si es diferente
            if self.ultimo_punto_valido != (self.x, self.y):
                self.puntos_trazado.append((self.x, self.y))
            
        puntos = self.puntos_trazado.copy()  # Hacer una copia para retornar
        self.limpiar_trazado()
        return puntos

    def cancelar_trazado(self) -> None:
        """Cancela el trazado actual sin retornar puntos."""
        self.trazando = False
        self.limpiar_trazado()

    def limpiar_trazado(self) -> None:
        """Limpia todas las variables relacionadas con el trazado."""
        self.puntos_trazado = []
        self.ultimo_punto_valido = None
        self.punto_prediccion = None

    def activar_escudo(self, duracion: float) -> None:
        """
        Activa el escudo protector.
        
        Args:
            duracion (float): Duración del escudo en segundos
        """
        self.tiene_escudo = True
        self.tiempo_escudo = 0
        self.duracion_escudo = duracion
        print("¡Escudo activado!")

    def _actualizar_escudo(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado del escudo.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        if self.tiene_escudo:
            self.tiempo_escudo += delta_tiempo
            if self.tiempo_escudo >= self.duracion_escudo:
                self.tiene_escudo = False
                print("Escudo desactivado")

    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado del jugador.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        # Actualizar invulnerabilidad
        if self.invulnerable:
            self.tiempo_invulnerabilidad += delta_tiempo
            if self.tiempo_invulnerabilidad >= self.duracion_invulnerabilidad:
                self.invulnerable = False
                self.tiempo_invulnerabilidad = 0
        
        # Actualizar escudo
        self._actualizar_escudo(delta_tiempo)
    
    def recibir_daño(self) -> None:
        """Procesa el daño recibido por el jugador."""
        if self.tiene_escudo:
            # El escudo absorbe el daño
            self.tiene_escudo = False
            self.sonidos.reproducir_sonido('escudo')
            print("¡El escudo ha absorbido el daño!")
            return
        
        if not self.invulnerable:
            self.vidas -= 1
            self.invulnerable = True
            self.tiempo_invulnerabilidad = 0
            # Cancelar cualquier trazado en progreso
            self.cancelar_trazado()
    
    def dibujar(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja el jugador y sus efectos visuales.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar sistema de partículas
        self._dibujar_particulas(pantalla)
        
        # Verificar si debemos dibujar el jugador (efecto de parpadeo durante invulnerabilidad)
        if not self.invulnerable or (self.tiempo_invulnerabilidad * self.frecuencia_parpadeo) % 2 < 1:
            # Dibujar escudo si está activo
            if self.tiene_escudo:
                # Efecto de pulso para el escudo
                factor_pulso = 1.0 + 0.2 * math.sin(self.tiempo_escudo * 5.0)
                radio_escudo = int(self.radio_escudo * factor_pulso)
                
                # Crear superficie para el escudo con transparencia
                superficie_escudo = pygame.Surface((radio_escudo * 2, radio_escudo * 2), pygame.SRCALPHA)
                color_escudo = (*self.color_escudo, self.alpha_escudo)
                pygame.draw.circle(superficie_escudo, color_escudo,
                                 (radio_escudo, radio_escudo), radio_escudo)
                
                # Dibujar líneas de energía
                num_lineas = 8
                for i in range(num_lineas):
                    angulo = self.tiempo_escudo * 2 + (i * 2 * math.pi / num_lineas)
                    x1 = radio_escudo + math.cos(angulo) * (radio_escudo * 0.7)
                    y1 = radio_escudo + math.sin(angulo) * (radio_escudo * 0.7)
                    x2 = radio_escudo + math.cos(angulo) * radio_escudo
                    y2 = radio_escudo + math.sin(angulo) * radio_escudo
                    pygame.draw.line(superficie_escudo, (*self.color_escudo, 200),
                                   (int(x1), int(y1)), (int(x2), int(y2)), 2)
                
                # Dibujar escudo
                pantalla.blit(superficie_escudo,
                             (int(self.x - radio_escudo), int(self.y - radio_escudo)))
            
            # Dibujar jugador
            pygame.draw.circle(pantalla, self.color_base,
                             (int(self.x), int(self.y)), self.radio)
            
            # Dibujar brillo interior
            pygame.draw.circle(pantalla, (255, 255, 255),
                             (int(self.x), int(self.y)), self.radio - 3)
        
        # Dibujar trazado actual
        if self.trazando and len(self.puntos_trazado) > 1:
            pygame.draw.lines(pantalla, self.color_trazado, False,
                            [(int(x), int(y)) for x, y in self.puntos_trazado], 2)
            
            # Dibujar punto de predicción si existe
            if self.punto_prediccion is not None:
                pygame.draw.line(pantalla, self.color_prediccion,
                               (int(self.x), int(self.y)),
                               (int(self.punto_prediccion[0]),
                                int(self.punto_prediccion[1])), 2)
                pygame.draw.circle(pantalla, self.color_prediccion,
                                 (int(self.punto_prediccion[0]),
                                  int(self.punto_prediccion[1])), 5)
        
        # Dibujar elementos de debug
        if self.modo_debug:
            # Dibujar círculo de colisión
            pygame.draw.circle(pantalla, (255, 255, 0),
                             (int(self.x), int(self.y)), self.radio_colision, 1)
            
            # Dibujar estado de invulnerabilidad
            if self.invulnerable:
                pygame.draw.circle(pantalla, (255, 0, 0),
                                 (int(self.x), int(self.y)), self.radio + 5, 1)
    
    def iniciar_trazado(self) -> None:
        """Inicia un nuevo trazado."""
        if self.invulnerable:  # No permitir trazado mientras está invulnerable
            return
        self.trazando = True
        self.puntos_trazado = [(self.x, self.y)]
        self.ultimo_punto_valido = (self.x, self.y)