import pygame
import random
import math
from typing import Tuple, List, Optional, Set
from utils import detectar_colision_linea_circulo, punto_en_poligono, distancia_punto_a_segmento

class Enemigo:
    """Clase que maneja el comportamiento de los enemigos (arañas)."""
    
    # Definir tipos de arañas con sus características
    TIPOS_ARAÑAS = {
        1: {  # Araña básica (nivel 1) - Movimiento aleatorio
            'color_cuerpo': (20, 20, 20),    # Negro
            'color_patas': (40, 40, 40),     # Gris oscuro
            'color_ojos': (255, 0, 0),       # Rojo
            'velocidad_base': 18.0,
            'escala': 1.0,
            'tipo_ia': 'aleatoria'           # Movimiento aleatorio
        },
        2: {  # Araña de hielo (nivel 2) - Perseguidora lenta
            'color_cuerpo': (0, 150, 255),   # Azul hielo
            'color_patas': (135, 206, 235),  # Azul cielo
            'color_ojos': (200, 255, 255),   # Azul brillante
            'velocidad_base': 22.0,
            'escala': 1.1,
            'tipo_ia': 'perseguidora'        # Persigue al jugador
        },
        3: {  # Araña gigante (nivel 3) - Rebotadora agresiva
            'color_cuerpo': (139, 69, 19),   # Marrón
            'color_patas': (160, 82, 45),    # Siena
            'color_ojos': (255, 215, 0),     # Dorado
            'velocidad_base': 26.0,
            'escala': 1.2,
            'tipo_ia': 'rebotadora'          # Rebota en los bordes
        },
        4: {  # Araña eléctrica (nivel 4) - Perseguidora rápida
            'color_cuerpo': (0, 0, 139),     # Azul oscuro
            'color_patas': (0, 0, 255),      # Azul
            'color_ojos': (255, 255, 0),     # Amarillo
            'velocidad_base': 30.0,
            'escala': 1.15,
            'tipo_ia': 'perseguidora_rapida' # Persigue al jugador rápidamente
        },
        5: {  # Araña de fuego (nivel 5) - Combinación de comportamientos
            'color_cuerpo': (139, 0, 0),     # Rojo oscuro
            'color_patas': (255, 69, 0),     # Rojo-naranja
            'color_ojos': (255, 165, 0),     # Naranja
            'velocidad_base': 35.0,
            'escala': 1.25,
            'tipo_ia': 'inteligente'         # Combina diferentes comportamientos
        }
    }
    
    def __init__(self, x: float, y: float, nivel: int = 1, radio: int = 15):
        """
        Inicializa un enemigo araña.
        
        Args:
            x (float): Posición inicial X
            y (float): Posición inicial Y
            nivel (int): Nivel de la araña que determina su tipo
            radio (int): Radio de colisión
        """
        self.x = x
        self.y = y
        self.nivel = min(max(nivel, 1), len(self.TIPOS_ARAÑAS))
        self.tipo = self.TIPOS_ARAÑAS[self.nivel]
        self.velocidad_base = self.tipo['velocidad_base']
        self.velocidad = self.velocidad_base
        self.radio = radio
        self.escala = self.tipo['escala']
        
        # Animación de patas
        self.angulos_patas = [0] * 8  # Ángulo para cada pata
        self.velocidades_pata = [random.uniform(3, 5) for _ in range(8)]  # Velocidad de animación por pata
        self.fases_pata = [random.uniform(0, 2 * math.pi) for _ in range(8)]  # Fase de animación por pata
        self.amplitud_pata = 15  # Amplitud de movimiento de las patas
        
        # Vector de dirección (normalizado)
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self._normalizar_direccion()
        
        # Ángulo de rotación del cuerpo
        self.angulo = 0
        self.velocidad_rotacion = random.uniform(-2, 2)
        
        # Efectos visuales
        self.escala_actual = self.escala
        self.escala_objetivo = self.escala
        self.velocidad_escala = 5.0
        
        # Trail y efectos
        self.trail_points = []
        self.max_trail_points = 10
        self.trail_alpha = 160
        self.color_trail = (*self.tipo['color_patas'], self.trail_alpha)
        
        # Estado de impacto
        self.esta_impactando = False
        self.tiempo_impacto = 0
        self.duracion_impacto = 0.5
        self.particulas_impacto = []
        
        # Efectos de brillo
        self.brillo = 0
        self.velocidad_brillo = 3.0
        self.direccion_brillo = 1
        
        # Variación de velocidad
        self.tiempo_cambio_velocidad = 0
        self.intervalo_cambio_velocidad = random.uniform(1.0, 2.0)
        self.velocidad_min = self.velocidad_base * 0.8
        self.velocidad_max = self.velocidad_base * 1.5
        
        # Cargar y escalar la imagen de la araña
        try:
            self.imagen_original = pygame.image.load("assets/spider.png").convert_alpha()
            # Escalar la imagen al tamaño deseado (radio * 6 para que sea más visible)
            tamaño = int(radio * 6)  # Aumentado de 4 a 6 para hacer la araña más grande
            self.imagen_original = pygame.transform.scale(self.imagen_original, (tamaño, tamaño))
            self.imagen = self.imagen_original.copy()
        except:
            print("No se pudo cargar la imagen de la araña")
            self.imagen_original = None
            self.imagen = None
        
        # Efectos de movimiento
        self.trail_points = []
        self.max_trail_points = 10
        self.trail_alpha = 160
        
        # Efectos de brillo
        self.brillo = 0
        self.velocidad_brillo = 3.0
        self.direccion_brillo = 1
        
        # Estado
        self.activo = True
        self.tiempo_vida = 0
        
        # Efecto de impacto
        self.esta_impactando = False
        self.tiempo_impacto = 0
        self.duracion_impacto = 0.5
        self.particulas_impacto = []
        
        # Colores
        self.color_impacto = (255, 100, 100)  # Rosa coral
        self.color_trail = (255, 223, 186, 160)  # Dorado con alpha
        
        # Animación de quelíceros
        self.angulo_queliceros = 0
        self.velocidad_queliceros = 8.0
        
        # Pulso del abdomen
        self.escala_abdomen = 1.0
        self.velocidad_pulso_abdomen = 1.5
        self.fase_pulso = random.uniform(0, 2 * math.pi)
        
        # Efectos de partículas
        self.particulas_sombra = []
        self.max_particulas_sombra = 10
        
        # Trail de movimiento
        self.puntos_trail = []
        self.max_puntos_trail = 5
        
        # Efectos de impacto mejorados
        self.color_energia = (0, 255, 255)    # Azul eléctrico
        self.color_destello = (255, 223, 186) # Dorado champagne
        
        # Efecto de pulso
        self.escala_pulso = 1.0
        self.direccion_pulso = 1
        self.velocidad_pulso = 2.0
        
        # Efecto de impacto
        self.particulas_impacto = []
        self.tiempo_impacto = 0
        self.duracion_impacto = 0.5
        self.esta_impactando = False
        
        self.tipo_ia = self.tipo['tipo_ia']
        self.tiempo_cambio_comportamiento = 0
        self.intervalo_cambio_comportamiento = random.uniform(3.0, 5.0)
        self.comportamiento_actual = self.tipo_ia
        self.pos_objetivo = None
        
        # Estado de congelación
        self.congelado = False
        self.tiempo_congelado = 0
        self.duracion_congelacion = 4.0  # 4 segundos
        self.color_congelado = (150, 230, 255)  # Azul claro para efecto de hielo
        self.particulas_hielo = []
        self.max_particulas_hielo = 15
    
    def _normalizar_direccion(self) -> None:
        """Normaliza el vector de dirección."""
        magnitud = math.sqrt(self.dx * self.dx + self.dy * self.dy)
        if magnitud > 0:
            self.dx /= magnitud
            self.dy /= magnitud
    
    def _actualizar_ia(self, jugador_x: float, jugador_y: float, ancho: int, alto: int, delta_tiempo: float) -> None:
        """
        Actualiza el comportamiento de la IA según su tipo.
        
        Args:
            jugador_x (float): Posición X del jugador
            jugador_y (float): Posición Y del jugador
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        if self.tipo_ia == 'inteligente':
            # Cambiar comportamiento periódicamente
            self.tiempo_cambio_comportamiento += delta_tiempo
            if self.tiempo_cambio_comportamiento >= self.intervalo_cambio_comportamiento:
                self.comportamiento_actual = random.choice(['aleatoria', 'perseguidora', 'rebotadora'])
                self.tiempo_cambio_comportamiento = 0
                self.intervalo_cambio_comportamiento = random.uniform(3.0, 5.0)
        else:
            self.comportamiento_actual = self.tipo_ia
        
        # Aplicar comportamiento actual
        if self.comportamiento_actual in ['perseguidora', 'perseguidora_rapida']:
            # Calcular dirección hacia el jugador
            dx = jugador_x - self.x
            dy = jugador_y - self.y
            distancia = math.sqrt(dx * dx + dy * dy)
            if distancia > 0:
                self.dx = dx / distancia
                self.dy = dy / distancia
                
            # Perseguidora rápida tiene aceleración adicional
            if self.comportamiento_actual == 'perseguidora_rapida':
                self.velocidad = min(self.velocidad * 1.05, self.velocidad_base * 1.5)
                
        elif self.comportamiento_actual == 'rebotadora':
            # Mantener la dirección actual hasta chocar con los bordes
            # El rebote se maneja en actualizar()
            # Aumentar velocidad gradualmente
            self.velocidad = min(self.velocidad * 1.02, self.velocidad_base * 1.3)
            
        elif self.comportamiento_actual == 'aleatoria':
            # Cambiar dirección aleatoriamente
            self.tiempo_cambio_velocidad += delta_tiempo
            if self.tiempo_cambio_velocidad >= self.intervalo_cambio_velocidad:
                angulo = random.uniform(-math.pi/3, math.pi/3)
                cos_ang = math.cos(angulo)
                sin_ang = math.sin(angulo)
                nuevo_dx = self.dx * cos_ang - self.dy * sin_ang
                nuevo_dy = self.dx * sin_ang + self.dy * cos_ang
                self.dx = nuevo_dx
                self.dy = nuevo_dy
                self._normalizar_direccion()
                self.tiempo_cambio_velocidad = 0
                self.intervalo_cambio_velocidad = random.uniform(1.0, 2.0)
                self.velocidad = random.uniform(self.velocidad_min, self.velocidad_max)
    
    def _actualizar_particulas_hielo(self, delta_tiempo: float) -> None:
        """Actualiza las partículas de hielo cuando el enemigo está congelado."""
        # Actualizar partículas existentes
        for particula in self.particulas_hielo[:]:
            particula['vida'] -= delta_tiempo
            if particula['vida'] <= 0:
                self.particulas_hielo.remove(particula)
                continue
            
            # Mover partícula
            particula['y'] += particula['velocidad'] * delta_tiempo
            
            # Efecto de oscilación
            particula['x'] = particula['x_base'] + math.sin(particula['tiempo'] * 2) * 2
            particula['tiempo'] += delta_tiempo
        
        # Generar nuevas partículas si es necesario
        if len(self.particulas_hielo) < self.max_particulas_hielo and self.congelado:
            angulo = random.uniform(0, 2 * math.pi)
            distancia = random.uniform(0, self.radio)
            x_base = self.x + math.cos(angulo) * distancia
            y = self.y + math.sin(angulo) * distancia - self.radio
            
            particula = {
                'x_base': x_base,
                'x': x_base,
                'y': y,
                'velocidad': random.uniform(10, 20),
                'vida': random.uniform(0.5, 1.0),
                'tamaño': random.uniform(2, 4),
                'tiempo': random.uniform(0, 2 * math.pi)
            }
            self.particulas_hielo.append(particula)
    
    def actualizar(self, area_segura: List[Tuple[int, int]], ancho: int, alto: int,
                  delta_tiempo: float, jugador_x: float = None, jugador_y: float = None) -> None:
        """
        Actualiza la posición y estado del enemigo.
        
        Args:
            area_segura (List[Tuple[int, int]]): Lista de puntos seguros
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
            delta_tiempo (float): Tiempo transcurrido desde el último frame
            jugador_x (float, optional): Posición X del jugador
            jugador_y (float, optional): Posición Y del jugador
        """
        if not self.activo:
            return
        
        # Actualizar estado de congelación
        if self.congelado:
            self.tiempo_congelado += delta_tiempo
            if self.tiempo_congelado >= self.duracion_congelacion:
                self.congelado = False
                self.tiempo_congelado = 0
                print("¡Araña descongelada!")
            else:
                # Actualizar partículas de hielo
                self._actualizar_particulas_hielo(delta_tiempo)
                return  # No mover si está congelado
        
        # Actualizar IA si tenemos la posición del jugador
        if jugador_x is not None and jugador_y is not None:
            self._actualizar_ia(jugador_x, jugador_y, ancho, alto, delta_tiempo)
        
        # Actualizar tiempo de vida
        self.tiempo_vida += delta_tiempo
        
        # Actualizar animación de patas
        for i in range(8):
            self.fases_pata[i] += self.velocidades_pata[i] * delta_tiempo
            self.angulos_patas[i] = math.sin(self.fases_pata[i]) * self.amplitud_pata
            
            # Ajustar velocidad de patas según la velocidad de movimiento
            factor_velocidad = self.velocidad / self.velocidad_base
            self.velocidades_pata[i] = random.uniform(3, 5) * factor_velocidad
        
        # Actualizar trail
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > self.max_trail_points:
            self.trail_points.pop(0)
        
        # Actualizar efecto de impacto
        if self.esta_impactando:
            self.tiempo_impacto += delta_tiempo
            if self.tiempo_impacto >= self.duracion_impacto:
                self.esta_impactando = False
                self.tiempo_impacto = 0
                self.particulas_impacto.clear()
        
        # Actualizar partículas de impacto
        for particula in self.particulas_impacto[:]:
            particula['vida'] -= delta_tiempo * 2
            if particula['vida'] <= 0:
                self.particulas_impacto.remove(particula)
                continue
            
            # Aplicar física a las partículas
            particula['dy'] += 400 * delta_tiempo  # Gravedad
            particula['dx'] *= 0.95  # Fricción
            particula['dy'] *= 0.95  # Fricción
            
            # Actualizar posición
            particula['x'] += particula['dx'] * delta_tiempo
            particula['y'] += particula['dy'] * delta_tiempo
        
        # Calcular nueva posición
        nueva_x = self.x + self.dx * self.velocidad * delta_tiempo
        nueva_y = self.y + self.dy * self.velocidad * delta_tiempo
        
        # Rebotar en los bordes con efecto más orgánico
        if nueva_x - self.radio < 0 or nueva_x + self.radio >= ancho:
            self.dx *= -1
            nueva_x = max(self.radio, min(ancho - self.radio, nueva_x))
            self.dy += random.uniform(-0.2, 0.2)
            self._normalizar_direccion()
            self.velocidad_rotacion = random.uniform(-2, 2)  # Cambiar rotación al rebotar
        
        if nueva_y - self.radio < 0 or nueva_y + self.radio >= alto:
            self.dy *= -1
            nueva_y = max(self.radio, min(alto - self.radio, nueva_y))
            self.dx += random.uniform(-0.2, 0.2)
            self._normalizar_direccion()
            self.velocidad_rotacion = random.uniform(-2, 2)  # Cambiar rotación al rebotar
        
        # Actualizar posición
        self.x = nueva_x
        self.y = nueva_y
        
        # Cambiar velocidad y dirección periódicamente
        self.tiempo_cambio_velocidad += delta_tiempo
        if self.tiempo_cambio_velocidad >= self.intervalo_cambio_velocidad:
            self.velocidad = random.uniform(self.velocidad_min, self.velocidad_max)
            self.tiempo_cambio_velocidad = 0
            self.intervalo_cambio_velocidad = random.uniform(1.0, 2.0)
            
            # Cambiar dirección de manera más orgánica
            angulo = random.uniform(-math.pi/3, math.pi/3)  # Cambio más suave
            cos_ang = math.cos(angulo)
            sin_ang = math.sin(angulo)
            nuevo_dx = self.dx * cos_ang - self.dy * sin_ang
            nuevo_dy = self.dx * sin_ang + self.dy * cos_ang
            self.dx = nuevo_dx
            self.dy = nuevo_dy
            self._normalizar_direccion()
    
    def dibujar(self, pantalla: pygame.Surface, modo_debug: bool = False) -> None:
        """
        Dibuja el enemigo con efectos visuales mejorados.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
            modo_debug (bool): Si está en modo debug
        """
        if not self.activo:
            return
        
        # Dibujar trail con el color correspondiente al tipo
        if len(self.trail_points) > 1:
            puntos = [(int(x), int(y)) for x, y in self.trail_points]
            if len(puntos) >= 2:
                for i in range(len(puntos) - 1):
                    alpha = int(self.trail_alpha * (i / len(puntos)))
                    color_trail = (*self.tipo['color_patas'], alpha)
                    pygame.draw.line(pantalla, color_trail, puntos[i], puntos[i + 1], 2)
        
        if self.imagen is not None:
            # Rotar la imagen
            self.angulo += self.velocidad_rotacion * (self.velocidad / self.velocidad_base)
            imagen_rotada = pygame.transform.rotate(self.imagen, self.angulo)
            
            # Aplicar escala
            if self.esta_impactando:
                self.escala_objetivo = 1.2
            else:
                self.escala_objetivo = 1.0
            
            self.escala += (self.escala_objetivo - self.escala) * 0.1
            if self.escala != 1.0:
                tamaño = imagen_rotada.get_size()
                nuevo_tamaño = (int(tamaño[0] * self.escala), int(tamaño[1] * self.escala))
                imagen_rotada = pygame.transform.scale(imagen_rotada, nuevo_tamaño)
            
            # Obtener el rectángulo centrado
            rect = imagen_rotada.get_rect()
            rect.center = (int(self.x), int(self.y))
            
            # Aplicar efecto de brillo durante el impacto
            if self.esta_impactando:
                self.brillo += self.velocidad_brillo * self.direccion_brillo
                if self.brillo >= 255:
                    self.brillo = 255
                    self.direccion_brillo = -1
                elif self.brillo <= 0:
                    self.brillo = 0
                    self.direccion_brillo = 1
                
                # Crear una copia de la imagen y aplicar el brillo
                imagen_brillante = imagen_rotada.copy()
                brillo_superficie = pygame.Surface(imagen_rotada.get_size(), pygame.SRCALPHA)
                brillo_superficie.fill((255, 255, 255, int(self.brillo * 0.5)))
                imagen_brillante.blit(brillo_superficie, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
                pantalla.blit(imagen_brillante, rect)
            else:
                pantalla.blit(imagen_rotada, rect)
        
        # Dibujar cuerpo
        pos_cuerpo = (int(self.x), int(self.y))
        radio_actual = int(self.radio * self.escala_actual)
        
        # Dibujar las 8 patas con animación
        for i in range(8):
            angulo_base = (i * 45 + self.angulo) * math.pi / 180
            angulo_animado = angulo_base + self.angulos_patas[i] * math.pi / 180
            
            # Calcular puntos de la pata
            x_inicio = self.x + math.cos(angulo_base) * radio_actual
            y_inicio = self.y + math.sin(angulo_base) * radio_actual
            x_fin = self.x + math.cos(angulo_animado) * radio_actual * 2.5
            y_fin = self.y + math.sin(angulo_animado) * radio_actual * 2.5
            
            # Punto medio para la articulación
            x_medio = (x_inicio + x_fin) / 2
            y_medio = (y_inicio + y_fin) / 2
            
            # Dibujar segmentos de la pata
            pygame.draw.line(pantalla, self.tipo['color_patas'], 
                           (int(x_inicio), int(y_inicio)), 
                           (int(x_medio), int(y_medio)), 3)
            pygame.draw.line(pantalla, self.tipo['color_patas'], 
                           (int(x_medio), int(y_medio)), 
                           (int(x_fin), int(y_fin)), 2)
            
            # Dibujar articulación
            pygame.draw.circle(pantalla, self.tipo['color_patas'], 
                             (int(x_medio), int(y_medio)), 3)
        
        # Dibujar cuerpo con efecto de brillo durante el impacto
        color_cuerpo = self.tipo['color_cuerpo']
        if self.esta_impactando:
            factor_brillo = self.brillo / 255
            color_cuerpo = tuple(min(255, c + int(factor_brillo * 255)) for c in color_cuerpo)
        
        pygame.draw.circle(pantalla, color_cuerpo, pos_cuerpo, radio_actual)
        
        # Dibujar ojos
        radio_ojo = int(radio_actual * 0.2)
        offset_ojo = int(radio_actual * 0.4)
        for offset_x in [-offset_ojo, offset_ojo]:
            # Sombra del ojo
            pygame.draw.circle(pantalla, (0, 0, 0),
                             (pos_cuerpo[0] + offset_x + 1, pos_cuerpo[1] - offset_ojo + 1),
                             radio_ojo + 1)
            # Ojo
            pygame.draw.circle(pantalla, self.tipo['color_ojos'],
                             (pos_cuerpo[0] + offset_x, pos_cuerpo[1] - offset_ojo),
                             radio_ojo)
            # Brillo del ojo
            pygame.draw.circle(pantalla, (255, 255, 255),
                             (pos_cuerpo[0] + offset_x - 1, pos_cuerpo[1] - offset_ojo - 1),
                             radio_ojo // 2)
        
        # Dibujar partículas de impacto
        for particula in self.particulas_impacto[:]:
            alpha = int(255 * particula['vida'])
            color = (*particula['color'][:3], alpha)
            pygame.draw.circle(pantalla, color,
                             (int(particula['x']), int(particula['y'])),
                             int(particula['tamaño'] * (1 + particula['vida'])))
        
        # Dibujar efecto de congelación
        if self.congelado:
            # Dibujar partículas de hielo
            for particula in self.particulas_hielo:
                alpha = int(255 * (particula['vida'] / 1.0))
                color = (*self.color_congelado, alpha)
                pygame.draw.circle(
                    pantalla,
                    color,
                    (int(particula['x']), int(particula['y'])),
                    int(particula['tamaño'])
                )
            
            # Dibujar capa de hielo sobre la araña
            superficie_hielo = pygame.Surface((self.radio * 4, self.radio * 4), pygame.SRCALPHA)
            centro_hielo = (self.radio * 2, self.radio * 2)
            
            # Dibujar cristales de hielo
            for _ in range(6):
                angulo = random.uniform(0, 2 * math.pi)
                x = centro_hielo[0] + math.cos(angulo) * self.radio
                y = centro_hielo[1] + math.sin(angulo) * self.radio
                pygame.draw.circle(superficie_hielo, (*self.color_congelado, 128),
                                 (int(x), int(y)), int(self.radio * 0.3))
            
            # Aplicar superficie de hielo
            rect_hielo = superficie_hielo.get_rect()
            rect_hielo.center = (int(self.x), int(self.y))
            pantalla.blit(superficie_hielo, rect_hielo)
        
        if modo_debug:
            self._dibujar_debug(pantalla)
    
    def _dibujar_debug(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja información de debug.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar vector de dirección
        punto_final = (
            int(self.x + self.dx * self.radio * 2),
            int(self.y + self.dy * self.radio * 2)
        )
        pygame.draw.line(pantalla, (0, 255, 0), (int(self.x), int(self.y)), punto_final, 2)
        
        # Dibujar círculo de colisión
        pygame.draw.circle(pantalla, (255, 255, 0), (int(self.x), int(self.y)),
                         self.radio, 1)
    
    def esta_dentro_area(self, poligono: List[Tuple[int, int]]) -> bool:
        """
        Verifica si el enemigo está completamente dentro de un área.
        
        Args:
            poligono (List[Tuple[int, int]]): Lista de puntos que forman el polígono
            
        Returns:
            bool: True si el enemigo está dentro del área
        """
        # Verificar si el centro está dentro
        if not punto_en_poligono((int(self.x), int(self.y)), poligono):
            return False
        
        # Verificar puntos alrededor del círculo para asegurar que está completamente dentro
        for angulo in range(0, 360, 45):
            rad = math.radians(angulo)
            punto_x = int(self.x + math.cos(rad) * self.radio)
            punto_y = int(self.y + math.sin(rad) * self.radio)
            if not punto_en_poligono((punto_x, punto_y), poligono):
                return False
        
        return True

    def colisiona_con_linea(self, punto1: Tuple[float, float],
                         punto2: Tuple[float, float]) -> bool:
        """
        Verifica si hay colisión con una línea.
        
        Args:
            punto1 (Tuple[float, float]): Primer punto de la línea
            punto2 (Tuple[float, float]): Segundo punto de la línea
            
        Returns:
            bool: True si hay colisión
        """
        # Si la araña no está activa, no hay colisión
        if not self.activo:
            return False
            
        # Usar la función de distancia punto a segmento
        distancia = distancia_punto_a_segmento((self.x, self.y), punto1, punto2)
        
        # Si la distancia es menor o igual al radio, hay colisión
        if distancia <= self.radio:
            self.impactar()  # Activar efectos visuales de impacto
            return True
            
        return False
    
    def colisiona_con_punto(self, x: float, y: float) -> bool:
        """
        Verifica si hay colisión con un punto.
        
        Args:
            x (float): Coordenada X del punto
            y (float): Coordenada Y del punto
            
        Returns:
            bool: True si hay colisión
        """
        dx = x - self.x
        dy = y - self.y
        distancia_cuadrada = dx * dx + dy * dy
        return distancia_cuadrada <= self.radio * self.radio

    def impactar(self) -> None:
        """Activa el efecto de impacto."""
        print("¡Araña impactada! Activando efectos visuales")
        self.esta_impactando = True
        self.tiempo_impacto = 0
        
        # Crear partículas de impacto con más variedad
        num_particulas = 30  # Aumentado para más efecto
        for _ in range(num_particulas):
            angulo = random.uniform(0, 2 * math.pi)
            velocidad = random.uniform(150, 300)  # Velocidad aumentada
            tipo = random.choice(['destello', 'energia', 'fragmento'])
            
            if tipo == 'destello':
                color = (255, 223, 186)  # Dorado
                tamaño = random.uniform(4, 8)
                vida = random.uniform(0.5, 1.0)
            elif tipo == 'energia':
                color = (0, 255, 255)  # Azul eléctrico
                tamaño = random.uniform(2, 4)
                vida = random.uniform(0.3, 0.7)
            else:  # fragmento
                color = self.color_impacto
                tamaño = random.uniform(3, 6)
                vida = random.uniform(0.6, 0.9)
            
            particula = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angulo) * velocidad,
                'dy': math.sin(angulo) * velocidad,
                'vida': vida,
                'vida_inicial': vida,
                'tamaño': tamaño,
                'tipo': tipo,
                'color': color,
                'rotacion': random.uniform(0, 2 * math.pi),
                'velocidad_rotacion': random.uniform(-5, 5)
            }
            self.particulas_impacto.append(particula)
        
        print(f"Creadas {num_particulas} partículas de impacto")

    def colisiona_con_jugador(self, jugador_x: float, jugador_y: float, jugador_radio: float) -> bool:
        """
        Verifica si hay colisión con el jugador.
        
        Args:
            jugador_x (float): Posición X del jugador
            jugador_y (float): Posición Y del jugador
            jugador_radio (float): Radio de colisión del jugador
            
        Returns:
            bool: True si hay colisión
        """
        dx = self.x - jugador_x
        dy = self.y - jugador_y
        distancia_cuadrada = dx * dx + dy * dy
        radio_suma = self.radio + jugador_radio
        return distancia_cuadrada <= radio_suma * radio_suma

class GestorEnemigos:
    """Clase que maneja múltiples enemigos."""
    
    def __init__(self):
        """Inicializa el gestor de enemigos."""
        self.enemigos: List[Enemigo] = []
        self.tiempo_spawn = 0
        self.intervalo_spawn = 1.5
        self.max_enemigos = 5
        
        # Estado de ralentización
        self.ralentizado = False
        self.tiempo_ralentizacion = 0
        self.duracion_ralentizacion = 0
        self.factor_ralentizacion = 0.1  # Reducido a 0.1 (ahora se mueven al 10% de su velocidad)
        
        # Estado de congelación
        self.todos_congelados = False
        self.tiempo_congelacion_global = 0
        self.duracion_congelacion_global = 4.0
    
    def ralentizar(self, duracion: float) -> None:
        """
        Activa el efecto de ralentización.
        
        Args:
            duracion (float): Duración del efecto en segundos
        """
        self.ralentizado = True
        self.tiempo_ralentizacion = 0
        self.duracion_ralentizacion = duracion
        
        # Aplicar ralentización a todos los enemigos
        for enemigo in self.enemigos:
            enemigo.velocidad = enemigo.velocidad_base * self.factor_ralentizacion
            # Efecto visual de ralentización
            enemigo.color_cuerpo = (0, 255, 0)  # Verde para indicar ralentización
    
    def _actualizar_ralentizacion(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado de ralentización.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        if self.ralentizado:
            self.tiempo_ralentizacion += delta_tiempo
            if self.tiempo_ralentizacion >= self.duracion_ralentizacion:
                self.ralentizado = False
                # Restaurar velocidad normal
                for enemigo in self.enemigos:
                    enemigo.velocidad = enemigo.velocidad_base
                    enemigo.color_cuerpo = (20, 20, 20)  # Restaurar color original
    
    def congelar_todos(self, duracion: float = 4.0) -> None:
        """
        Congela a todos los enemigos.
        
        Args:
            duracion (float): Duración del efecto en segundos
        """
        self.todos_congelados = True
        self.tiempo_congelacion_global = 0
        self.duracion_congelacion_global = duracion
        
        for enemigo in self.enemigos:
            enemigo.congelado = True
            enemigo.tiempo_congelado = 0
            enemigo.duracion_congelacion = duracion
        print(f"¡Todos los enemigos congelados por {duracion} segundos!")
    
    def _actualizar_congelacion_global(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado de congelación global.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        if self.todos_congelados:
            self.tiempo_congelacion_global += delta_tiempo
            if self.tiempo_congelacion_global >= self.duracion_congelacion_global:
                self.todos_congelados = False
                self.tiempo_congelacion_global = 0
                print("¡Efecto de congelación global terminado!")
    
    def agregar_enemigo(self, x: float, y: float, nivel: int = 1) -> None:
        """
        Añade un nuevo enemigo.
        
        Args:
            x (float): Posición X inicial
            y (float): Posición Y inicial
            nivel (int): Nivel de la araña que determina su tipo
        """
        if len(self.enemigos) < self.max_enemigos:
            print(f"Creando nueva araña en ({x}, {y})")
            enemigo = Enemigo(x, y, nivel)
            self.enemigos.append(enemigo)
    
    def actualizar(self, area_segura: List[Tuple[int, int]], ancho: int, alto: int,
                  delta_tiempo: float, jugador_x: float = None, jugador_y: float = None) -> None:
        """
        Actualiza todos los enemigos y maneja el spawn de nuevos.
        
        Args:
            area_segura (List[Tuple[int, int]]): Lista de puntos seguros
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
            delta_tiempo (float): Tiempo transcurrido desde el último frame
            jugador_x (float, optional): Posición X del jugador
            jugador_y (float, optional): Posición Y del jugador
        """
        # Actualizar estado de ralentización
        self._actualizar_ralentizacion(delta_tiempo)
        
        # Actualizar estado de congelación global
        self._actualizar_congelacion_global(delta_tiempo)
        
        # Actualizar tiempo de spawn
        self.tiempo_spawn += delta_tiempo
        
        # Generar nuevo enemigo si es necesario
        if self.tiempo_spawn >= self.intervalo_spawn and len(self.enemigos) < self.max_enemigos:
            nivel = random.randint(1, 5)
            radio = 15
            # Posición aleatoria en los bordes
            if random.random() < 0.5:
                x = random.choice([radio, ancho - radio])
                y = random.randint(radio, alto - radio)
            else:
                x = random.randint(radio, ancho - radio)
                y = random.choice([radio, alto - radio])
            
            self.agregar_enemigo(x, y, nivel)
            self.tiempo_spawn = 0
            self.intervalo_spawn = random.uniform(1.0, 2.0)
        
        # Actualizar enemigos existentes
        for enemigo in self.enemigos:
            enemigo.actualizar(area_segura, ancho, alto, delta_tiempo, jugador_x, jugador_y)
    
    def verificar_colisiones_linea(self, punto1: Tuple[float, float],
                                 punto2: Tuple[float, float]) -> bool:
        """
        Verifica colisiones con una línea para todos los enemigos.
        
        Args:
            punto1 (Tuple[float, float]): Primer punto de la línea
            punto2 (Tuple[float, float]): Segundo punto de la línea
            
        Returns:
            bool: True si hay colisión con algún enemigo
        """
        return any(enemigo.colisiona_con_linea(punto1, punto2)
                  for enemigo in self.enemigos if enemigo.activo)
    
    def verificar_colisiones_linea_completa(self, puntos: List[Tuple[float, float]]) -> bool:
        """
        Verifica colisiones con una línea completa (múltiples segmentos).
        
        Args:
            puntos (List[Tuple[float, float]]): Lista de puntos que forman la línea
            
        Returns:
            bool: True si hay colisión con algún segmento
        """
        if len(puntos) < 2:
            return False
        
        # Verificar cada segmento de la línea
        for i in range(len(puntos) - 1):
            if self.verificar_colisiones_linea(puntos[i], puntos[i + 1]):
                return True
            
        return False
    
    def verificar_colisiones_punto(self, x: float, y: float) -> bool:
        """
        Verifica colisiones con un punto para todos los enemigos.
        
        Args:
            x (float): Coordenada X del punto
            y (float): Coordenada Y del punto
            
        Returns:
            bool: True si hay colisión con algún enemigo
        """
        return any(enemigo.colisiona_con_punto(x, y)
                  for enemigo in self.enemigos if enemigo.activo)
    
    def verificar_colisiones_jugador(self, jugador_x: float, jugador_y: float, jugador_radio: float) -> bool:
        """
        Verifica colisiones con el jugador para todos los enemigos.
        
        Args:
            jugador_x (float): Posición X del jugador
            jugador_y (float): Posición Y del jugador
            jugador_radio (float): Radio de colisión del jugador
            
        Returns:
            bool: True si hay colisión con algún enemigo
        """
        return any(enemigo.colisiona_con_jugador(jugador_x, jugador_y, jugador_radio)
                  for enemigo in self.enemigos if enemigo.activo)
    
    def dibujar(self, pantalla: pygame.Surface, modo_debug: bool = False) -> None:
        """
        Dibuja todos los enemigos.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
            modo_debug (bool): Si está activo el modo debug
        """
        if self.enemigos:  # Mensaje de depuración
            print(f"Dibujando {len(self.enemigos)} arañas")
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla, modo_debug)
    
    def eliminar_enemigos_en_area(self, poligono: List[Tuple[int, int]]) -> int:
        """
        Elimina los enemigos que están dentro de un área.
        
        Args:
            poligono (List[Tuple[int, int]]): Lista de puntos que forman el polígono
            
        Returns:
            int: Número de enemigos eliminados
        """
        enemigos_eliminados = 0
        enemigos_activos = []
        
        for enemigo in self.enemigos:
            if enemigo.esta_dentro_area(poligono):
                enemigos_eliminados += 1
                print(f"Araña eliminada en ({enemigo.x}, {enemigo.y})")  # Mensaje de depuración
            else:
                enemigos_activos.append(enemigo)
        
        self.enemigos = enemigos_activos
        return enemigos_eliminados

    def eliminar_enemigos_en_radio(self, centro_x: float, centro_y: float, radio: float) -> int:
        """
        Elimina los enemigos que están dentro de un radio específico.
        
        Args:
            centro_x (float): Coordenada X del centro
            centro_y (float): Coordenada Y del centro
            radio (float): Radio del área de eliminación
            
        Returns:
            int: Número de enemigos eliminados
        """
        enemigos_eliminados = 0
        enemigos_activos = []
        radio_cuadrado = radio * radio
        
        for enemigo in self.enemigos:
            # Calcular distancia al cuadrado (más eficiente que usar raíz cuadrada)
            dx = enemigo.x - centro_x
            dy = enemigo.y - centro_y
            distancia_cuadrada = dx * dx + dy * dy
            
            if distancia_cuadrada <= radio_cuadrado:
                enemigos_eliminados += 1
                print(f"Araña eliminada en ({enemigo.x}, {enemigo.y}) por explosión")
            else:
                enemigos_activos.append(enemigo)
        
        self.enemigos = enemigos_activos
        return enemigos_eliminados