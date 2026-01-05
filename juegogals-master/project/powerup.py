import pygame
import random
import math
from typing import Tuple, Optional
from abc import ABC, abstractmethod

class PowerUp(ABC):
    """Clase base abstracta para los power-ups."""
    
    def __init__(self, x: float, y: float, duracion: float = 5.0):
        """
        Inicializa el power-up.
        
        Args:
            x (float): Posición X inicial
            y (float): Posición Y inicial
            duracion (float): Duración del efecto en segundos
        """
        self.x = x
        self.y = y
        self.activo = True
        self.radio = 15
        self.duracion = duracion
        self.tiempo_activo = 0
        
        # Efectos visuales
        self.angulo = 0
        self.escala = 1.0
        self.velocidad_rotacion = 2.0
        self.velocidad_pulso = 3.0
        
        # Partículas
        self.particulas = []
        self.max_particulas = 20
        
    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado del power-up.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        # Actualizar efectos visuales
        self.angulo += self.velocidad_rotacion * delta_tiempo
        self.escala = 1.0 + 0.2 * math.sin(self.tiempo_activo * self.velocidad_pulso)
        
        # Actualizar partículas
        self._actualizar_particulas(delta_tiempo)
        
        # Generar nuevas partículas
        if random.random() < 0.1:
            self._generar_particula()
    
    def _actualizar_particulas(self, delta_tiempo: float) -> None:
        """Actualiza las partículas del power-up."""
        for particula in self.particulas[:]:
            particula['vida'] -= delta_tiempo
            if particula['vida'] <= 0:
                self.particulas.remove(particula)
                continue
            
            # Mover partícula
            particula['x'] += particula['dx'] * delta_tiempo
            particula['y'] += particula['dy'] * delta_tiempo
            
            # Actualizar alpha basado en vida restante
            particula['alpha'] = int(255 * (particula['vida'] / particula['vida_inicial']))
    
    def _generar_particula(self) -> None:
        """Genera una nueva partícula decorativa."""
        if len(self.particulas) >= self.max_particulas:
            return
            
        angulo = random.uniform(0, 2 * math.pi)
        velocidad = random.uniform(20, 40)
        vida = random.uniform(0.5, 1.0)
        
        particula = {
            'x': self.x,
            'y': self.y,
            'dx': math.cos(angulo) * velocidad,
            'dy': math.sin(angulo) * velocidad,
            'vida': vida,
            'vida_inicial': vida,
            'alpha': 255,
            'color': self.get_color()
        }
        self.particulas.append(particula)
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el power-up y sus efectos visuales.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
        """
        if not self.activo:
            return
            
        # Dibujar partículas
        for particula in self.particulas:
            color = (*particula['color'][:3], particula['alpha'])
            pygame.draw.circle(superficie, color,
                             (int(particula['x']), int(particula['y'])), 2)
        
        # Dibujar brillo exterior
        radio_brillo = int(self.radio * 1.5 * self.escala)
        superficie_brillo = pygame.Surface((radio_brillo * 2, radio_brillo * 2), pygame.SRCALPHA)
        color_brillo = (*self.get_color()[:3], 128)
        pygame.draw.circle(superficie_brillo, color_brillo,
                         (radio_brillo, radio_brillo), radio_brillo)
        superficie.blit(superficie_brillo,
                       (int(self.x - radio_brillo), int(self.y - radio_brillo)))
        
        # Dibujar círculo principal
        radio_actual = int(self.radio * self.escala)
        pygame.draw.circle(superficie, self.get_color(),
                         (int(self.x), int(self.y)), radio_actual)
        
        # Dibujar símbolo
        self.dibujar_simbolo(superficie, radio_actual)
    
    def colisiona_con_punto(self, x: float, y: float) -> bool:
        """
        Verifica si hay colisión con un punto.
        
        Args:
            x (float): Coordenada X del punto
            y (float): Coordenada Y del punto
            
        Returns:
            bool: True si hay colisión
        """
        if not self.activo:
            return False
            
        dx = x - self.x
        dy = y - self.y
        return (dx * dx + dy * dy) <= (self.radio * self.radio)
    
    @abstractmethod
    def aplicar_efecto(self, jugador: 'Jugador', gestor_enemigos: 'GestorEnemigos') -> None:
        """
        Aplica el efecto del power-up.
        
        Args:
            jugador (Jugador): Jugador al que aplicar el efecto
            gestor_enemigos (GestorEnemigos): Gestor de enemigos para efectos que los afecten
        """
        pass
    
    @abstractmethod
    def get_color(self) -> Tuple[int, int, int, int]:
        """
        Obtiene el color del power-up.
        
        Returns:
            Tuple[int, int, int, int]: Color RGBA
        """
        pass
    
    @abstractmethod
    def dibujar_simbolo(self, superficie: pygame.Surface, radio: int) -> None:
        """
        Dibuja el símbolo característico del power-up.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
            radio (int): Radio actual del power-up
        """
        pass

class PowerUpEscudo(PowerUp):
    """Power-up que otorga un escudo protector."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, duracion=10.0)  # El escudo dura 10 segundos
    
    def get_color(self) -> Tuple[int, int, int, int]:
        return (0, 191, 255, 255)  # Azul cielo
    
    def dibujar_simbolo(self, superficie: pygame.Surface, radio: int) -> None:
        # Dibujar símbolo de escudo
        puntos = []
        num_puntos = 6
        for i in range(num_puntos):
            angulo = self.angulo + (i * 2 * math.pi / num_puntos)
            x = self.x + math.cos(angulo) * (radio * 0.7)
            y = self.y + math.sin(angulo) * (radio * 0.7)
            puntos.append((int(x), int(y)))
        
        if len(puntos) >= 3:
            pygame.draw.polygon(superficie, (255, 255, 255), puntos, 2)
    
    def aplicar_efecto(self, jugador: 'Jugador', gestor_enemigos: 'GestorEnemigos') -> None:
        jugador.activar_escudo(self.duracion)
        jugador.sonidos.reproducir_sonido('powerup')

class PowerUpRalentizador(PowerUp):
    """Power-up que ralentiza a los enemigos."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, duracion=5.0)  # Ajustado a 5.0 segundos exactos
    
    def get_color(self) -> Tuple[int, int, int, int]:
        return (50, 205, 50, 255)  # Verde lima
    
    def dibujar_simbolo(self, superficie: pygame.Surface, radio: int) -> None:
        # Dibujar símbolo de reloj
        centro = (int(self.x), int(self.y))
        radio_reloj = int(radio * 0.7)
        pygame.draw.circle(superficie, (255, 255, 255), centro, radio_reloj, 2)
        
        # Manecillas del reloj
        angulo_hora = self.angulo
        angulo_minuto = self.angulo * 2
        
        # Manecilla hora
        x_hora = self.x + math.cos(angulo_hora) * (radio_reloj * 0.5)
        y_hora = self.y + math.sin(angulo_hora) * (radio_reloj * 0.5)
        pygame.draw.line(superficie, (255, 255, 255), centro, (int(x_hora), int(y_hora)), 2)
        
        # Manecilla minuto
        x_min = self.x + math.cos(angulo_minuto) * (radio_reloj * 0.7)
        y_min = self.y + math.sin(angulo_minuto) * (radio_reloj * 0.7)
        pygame.draw.line(superficie, (255, 255, 255), centro, (int(x_min), int(y_min)), 2)
    
    def aplicar_efecto(self, jugador: 'Jugador', gestor_enemigos: 'GestorEnemigos') -> None:
        gestor_enemigos.ralentizar(self.duracion)
        jugador.sonidos.reproducir_sonido('powerup')

class PowerUpCongelacion(PowerUp):
    """Power-up que congela a todos los enemigos."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y, duracion=4.0)  # Congelación dura 4 segundos
    
    def get_color(self) -> Tuple[int, int, int, int]:
        return (150, 230, 255, 255)  # Azul hielo
    
    def dibujar_simbolo(self, superficie: pygame.Surface, radio: int) -> None:
        # Dibujar copo de nieve
        centro = (int(self.x), int(self.y))
        color = (255, 255, 255)  # Blanco
        
        # Dibujar las 6 puntas del copo de nieve
        for i in range(6):
            angulo = self.angulo + (i * math.pi / 3)
            # Línea principal
            x_fin = self.x + math.cos(angulo) * (radio * 0.7)
            y_fin = self.y + math.sin(angulo) * (radio * 0.7)
            pygame.draw.line(superficie, color, centro, (int(x_fin), int(y_fin)), 2)
            
            # Ramificaciones
            tercio = radio * 0.3
            medio = (self.x + math.cos(angulo) * (radio * 0.4),
                    self.y + math.sin(angulo) * (radio * 0.4))
            
            # Ramificación izquierda
            angulo_rama = angulo - math.pi / 4
            x_rama = medio[0] + math.cos(angulo_rama) * tercio
            y_rama = medio[1] + math.sin(angulo_rama) * tercio
            pygame.draw.line(superficie, color, medio, (int(x_rama), int(y_rama)), 2)
            
            # Ramificación derecha
            angulo_rama = angulo + math.pi / 4
            x_rama = medio[0] + math.cos(angulo_rama) * tercio
            y_rama = medio[1] + math.sin(angulo_rama) * tercio
            pygame.draw.line(superficie, color, medio, (int(x_rama), int(y_rama)), 2)
    
    def aplicar_efecto(self, jugador: 'Jugador', gestor_enemigos: 'GestorEnemigos') -> None:
        gestor_enemigos.congelar_todos(self.duracion)
        jugador.sonidos.reproducir_sonido('powerup')

class PowerUpVida(PowerUp):
    """Power-up que otorga una vida extra al jugador."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y)  # No necesita duración
        self.latido = 0  # Para animación de latido
        self.velocidad_latido = 5.0
    
    def get_color(self) -> Tuple[int, int, int, int]:
        return (255, 50, 50, 255)  # Rojo brillante
    
    def actualizar(self, delta_tiempo: float) -> None:
        super().actualizar(delta_tiempo)
        self.latido += self.velocidad_latido * delta_tiempo
        self.escala = 1.0 + 0.2 * abs(math.sin(self.latido))  # Efecto de latido
    
    def dibujar_simbolo(self, superficie: pygame.Surface, radio: int) -> None:
        # Dibujar corazón
        centro_x = int(self.x)
        centro_y = int(self.y)
        tamaño = radio * 0.8  # Tamaño relativo al radio
        
        # Puntos para formar el corazón
        puntos = []
        for t in range(0, 360, 5):
            rad = math.radians(t)
            # Ecuación paramétrica de corazón
            x = 16 * math.sin(rad) ** 3
            y = 13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad)
            # Escalar y posicionar
            px = centro_x + int(x * tamaño / 16)
            py = centro_y - int(y * tamaño / 16)  # Restamos porque y crece hacia abajo en pygame
            puntos.append((px, py))
        
        # Dibujar el contorno y relleno
        if len(puntos) > 2:
            pygame.draw.polygon(superficie, (255, 255, 255), puntos)  # Borde blanco
            pygame.draw.polygon(superficie, self.get_color(), puntos, 2)  # Relleno rojo
    
    def aplicar_efecto(self, jugador: 'Jugador', gestor_enemigos: 'GestorEnemigos') -> None:
        if jugador.vidas < 3:  # Solo si no ha alcanzado el máximo
            jugador.vidas += 1
            jugador.sonidos.reproducir_sonido('powerup')
            print(f"¡Vida extra! Vidas actuales: {jugador.vidas}")

class PowerUpBomba(PowerUp):
    """Power-up que revela una zona y elimina enemigos en ella."""
    
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self.radio_explosion = 150  # Radio de la explosión en píxeles
        self.particulas_explosion = []
        self.duracion_explosion = 0.5
        self.tiempo_explosion = 0
        self.explotando = False
    
    def get_color(self) -> Tuple[int, int, int, int]:
        return (255, 165, 0, 255)  # Naranja explosivo
    
    def dibujar_simbolo(self, superficie: pygame.Surface, radio: int) -> None:
        # Dibujar bomba en pixel art
        centro_x = int(self.x)
        centro_y = int(self.y)
        
        # Cuerpo de la bomba (círculo negro)
        pygame.draw.circle(superficie, (30, 30, 30), (centro_x, centro_y), int(radio * 0.7))
        
        # Mecha (rectángulo marrón)
        mecha_x = centro_x - int(radio * 0.1)
        mecha_y = centro_y - int(radio * 0.8)
        pygame.draw.rect(superficie, (139, 69, 19), 
                        (mecha_x, mecha_y, int(radio * 0.2), int(radio * 0.3)))
        
        # Brillo (pequeño círculo blanco)
        brillo_x = centro_x + int(radio * 0.3)
        brillo_y = centro_y - int(radio * 0.3)
        pygame.draw.circle(superficie, (255, 255, 255), 
                         (brillo_x, brillo_y), int(radio * 0.15))
        
        # Si está explotando, dibujar la explosión
        if self.explotando:
            self._dibujar_explosion(superficie)
    
    def _dibujar_explosion(self, superficie: pygame.Surface) -> None:
        """Dibuja el efecto de explosión."""
        # Dibujar partículas de explosión
        for particula in self.particulas_explosion:
            alpha = int(255 * (particula['vida'] / particula['vida_inicial']))
            color = (*particula['color'][:3], alpha)
            radio = int(particula['tamaño'] * (1 + particula['vida']))
            pygame.draw.circle(superficie, color,
                             (int(particula['x']), int(particula['y'])), radio)
    
    def _crear_explosion(self) -> None:
        """Crea las partículas de la explosión."""
        colores_explosion = [
            (255, 165, 0),  # Naranja
            (255, 69, 0),   # Rojo-naranja
            (255, 215, 0),  # Amarillo
            (255, 255, 255) # Blanco
        ]
        
        num_particulas = 30
        for _ in range(num_particulas):
            angulo = random.uniform(0, 2 * math.pi)
            velocidad = random.uniform(100, 300)
            distancia = random.uniform(0, self.radio_explosion)
            vida = random.uniform(0.3, 0.8)
            
            particula = {
                'x': self.x + math.cos(angulo) * distancia,
                'y': self.y + math.sin(angulo) * distancia,
                'dx': math.cos(angulo) * velocidad,
                'dy': math.sin(angulo) * velocidad,
                'vida': vida,
                'vida_inicial': vida,
                'tamaño': random.uniform(5, 15),
                'color': random.choice(colores_explosion)
            }
            self.particulas_explosion.append(particula)
    
    def aplicar_efecto(self, jugador: 'Jugador', gestor_enemigos: 'GestorEnemigos') -> None:
        """
        Aplica el efecto de la bomba: revela área y elimina enemigos.
        
        Args:
            jugador (Jugador): Jugador que recogió el power-up
            gestor_enemigos (GestorEnemigos): Gestor de enemigos para eliminarlos
        """
        # Crear explosión
        self.explotando = True
        self._crear_explosion()
        
        # Verificar que el jugador tenga referencia al nivel
        if jugador.nivel is not None:
            # Calcular área a revelar (20% alrededor de la bomba)
            centro = (int(self.x), int(self.y))
            jugador.nivel.revelar_area_circular(centro, self.radio_explosion)
            
            # Eliminar enemigos en el área
            enemigos_eliminados = gestor_enemigos.eliminar_enemigos_en_radio(
                self.x, self.y, self.radio_explosion)
            
            print(f"¡Bomba detonada! Área revelada y {enemigos_eliminados} enemigos eliminados")
            
            # Reproducir sonido de explosión
            jugador.sonidos.reproducir_sonido('explosion')
        else:
            print("Error: El jugador no tiene referencia al nivel actual")

class GestorPowerUps:
    """Clase que gestiona la generación y actualización de power-ups."""
    
    def __init__(self):
        """Inicializa el gestor de power-ups."""
        self.power_ups = []
        self.tiempo_spawn = 0
        self.intervalo_spawn = 8.0
        self.intervalo_spawn_vida_baja = 4.0
        self.tipos_power_up = [
            PowerUpEscudo,
            PowerUpRalentizador,
            PowerUpCongelacion,
            PowerUpVida,
            PowerUpBomba
        ]
        
        # Control de cantidad por tipo
        self.contadores_powerup = {
            PowerUpEscudo: 0,
            PowerUpRalentizador: 0,
            PowerUpCongelacion: 0,
            PowerUpVida: 0,
            PowerUpBomba: 0
        }
        self.max_por_tipo = 3
        
        # Control de spawn de vida
        self.tiempo_spawn_vida = 0
        self.spawn_vida_prioritario = False
    
    def reiniciar_contadores(self) -> None:
        """Reinicia los contadores de power-ups para un nuevo nivel."""
        self.contadores_powerup = {tipo: 0 for tipo in self.tipos_power_up}
        self.tiempo_spawn = 0
        self.tiempo_spawn_vida = 0
    
    def actualizar(self, delta_tiempo: float, ancho: int, alto: int,
                  jugador: 'Jugador', gestor_enemigos: 'GestorEnemigos') -> None:
        """
        Actualiza todos los power-ups y genera nuevos.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
            ancho (int): Ancho del área de juego
            alto (int): Alto del área de juego
            jugador (Jugador): Referencia al jugador
            gestor_enemigos (GestorEnemigos): Referencia al gestor de enemigos
        """
        # Actualizar estado de spawn prioritario de vida
        self.spawn_vida_prioritario = jugador.vidas == 1
        
        # Actualizar tiempo para generar nuevos power-ups
        self.tiempo_spawn += delta_tiempo
        if self.spawn_vida_prioritario:
            self.tiempo_spawn_vida += delta_tiempo
        
        # Generar power-up de vida con mayor frecuencia si es necesario
        if self.spawn_vida_prioritario and self.tiempo_spawn_vida >= self.intervalo_spawn_vida_baja:
            self.tiempo_spawn_vida = 0
            if self.contadores_powerup[PowerUpVida] < self.max_por_tipo:
                self._generar_power_up_especifico(PowerUpVida, ancho, alto)
        
        # Generar power-ups normales
        if self.tiempo_spawn >= self.intervalo_spawn:
            self.tiempo_spawn = 0
            self._generar_power_up(ancho, alto)
        
        # Actualizar power-ups existentes
        for power_up in self.power_ups[:]:
            if not power_up.activo:
                self.power_ups.remove(power_up)
                continue
            
            power_up.actualizar(delta_tiempo)
            
            # Verificar colisión con el jugador
            if power_up.colisiona_con_punto(jugador.x, jugador.y):
                power_up.aplicar_efecto(jugador, gestor_enemigos)
                power_up.activo = False
    
    def _generar_power_up_especifico(self, tipo: type, ancho: int, alto: int) -> None:
        """Genera un power-up de un tipo específico."""
        if self.contadores_powerup[tipo] >= self.max_por_tipo:
            return
            
        margen = 50
        x = random.randint(margen, ancho - margen)
        y = random.randint(margen, alto - margen)
        
        power_up = tipo(x, y)
        self.power_ups.append(power_up)
        self.contadores_powerup[tipo] += 1
        print(f"Nuevo power-up de vida generado en ({x}, {y})")
    
    def _generar_power_up(self, ancho: int, alto: int) -> None:
        """
        Genera un nuevo power-up en una posición aleatoria.
        
        Args:
            ancho (int): Ancho del área de juego
            alto (int): Alto del área de juego
        """
        # Filtrar tipos disponibles (que no hayan alcanzado el máximo)
        tipos_disponibles = [tipo for tipo in self.tipos_power_up 
                           if self.contadores_powerup[tipo] < self.max_por_tipo]
        
        if not tipos_disponibles:
            print("No hay más power-ups disponibles en este nivel")
            return
        
        # Elegir tipo aleatorio entre los disponibles
        tipo_power_up = random.choice(tipos_disponibles)
        
        # Generar posición aleatoria (con margen para evitar bordes)
        margen = 50
        x = random.randint(margen, ancho - margen)
        y = random.randint(margen, alto - margen)
        
        # Crear y añadir el power-up
        power_up = tipo_power_up(x, y)
        self.power_ups.append(power_up)
        self.contadores_powerup[tipo_power_up] += 1
        
        # Mensaje informativo
        print(f"Nuevo power-up generado: {tipo_power_up.__name__} en ({x}, {y})")
        print(f"Contadores actuales: Escudo({self.contadores_powerup[PowerUpEscudo]}), " +
              f"Ralentizador({self.contadores_powerup[PowerUpRalentizador]}), " +
              f"Congelación({self.contadores_powerup[PowerUpCongelacion]}), " +
              f"Vida({self.contadores_powerup[PowerUpVida]}), Bomba({self.contadores_powerup[PowerUpBomba]})")
    
    def dibujar(self, superficie: pygame.Surface) -> None:
        """
        Dibuja todos los power-ups activos.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
        """
        for power_up in self.power_ups:
            power_up.dibujar(superficie) 