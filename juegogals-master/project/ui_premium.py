import pygame
import math
import random
from typing import List, Tuple, Optional
from theme_manager import ThemeManager

class UI_Premium:
    """Clase que maneja la interfaz de usuario premium con efectos visuales avanzados."""
    
    def __init__(self, ancho: int, alto: int):
        """
        Inicializa la interfaz premium.
        
        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        
        # Gestor de temas
        self.theme_manager = ThemeManager()
        
        # Cargar fuentes
        pygame.font.init()
        try:
            self.fuente_principal = pygame.font.Font("fonts/Orbitron-Bold.ttf", 24)
            self.fuente_numeros = pygame.font.Font("fonts/DS-DIGI.ttf", 32)
        except:
            print("Fuentes personalizadas no encontradas, usando fallback...")
            self.fuente_principal = pygame.font.SysFont("arial", 24)
            self.fuente_numeros = pygame.font.SysFont("arial", 32)
        
        # Sistema de partículas
        self.particulas = []
        self.max_particulas = self.theme_manager.obtener_efecto("particle_count")
        
        # Estado de transición
        self.en_transicion = False
        self.alpha_transicion = 0
        self.direccion_transicion = 1
        
        # Efectos visuales
        self.tiempo_acumulado = 0
        self.angulo_glow = 0
        
        # Crear superficies pre-renderizadas
        self._crear_assets()
    
    def _crear_assets(self) -> None:
        """Crea y pre-renderiza elementos visuales comunes."""
        # Crear corazón base
        self.corazon_base = self._crear_corazon()
        
        # Crear efectos de glow
        self.glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self._actualizar_glow()
    
    def _crear_corazon(self) -> pygame.Surface:
        """
        Crea una superficie con un corazón estilizado.
        
        Returns:
            pygame.Surface: Superficie con el corazón renderizado
        """
        superficie = pygame.Surface((40, 40), pygame.SRCALPHA)
        
        # Crear forma de corazón con gradiente
        puntos = [
            (20, 10), (10, 5), (5, 10), (5, 15),
            (20, 35), (35, 15), (35, 10), (30, 5)
        ]
        
        # Dibujar con gradiente
        for y in range(40):
            color = self._interpolar_color(
                self.theme_manager.obtener_color("secondary"),
                self.theme_manager.obtener_color("accent"),
                y / 40
            )
            pygame.draw.line(superficie, color, (0, y), (40, y))
        
        # Aplicar máscara de corazón
        mascara = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(mascara, (255, 255, 255), puntos)
        superficie.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        return superficie
    
    def _interpolar_color(self, color1: Tuple[int, int, int],
                         color2: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """
        Interpola entre dos colores.
        
        Args:
            color1 (Tuple[int, int, int]): Color inicial
            color2 (Tuple[int, int, int]): Color final
            factor (float): Factor de interpolación (0-1)
            
        Returns:
            Tuple[int, int, int]: Color interpolado
        """
        return tuple(int(c1 + (c2 - c1) * factor) for c1, c2 in zip(color1, color2))
    
    def _actualizar_glow(self) -> None:
        """Actualiza el efecto de resplandor."""
        self.glow_surface.fill((0, 0, 0, 0))
        centro = (50, 50)
        
        glow_strength = self.theme_manager.obtener_efecto("glow_strength")
        color_primary = self.theme_manager.obtener_color("primary")
        
        for radio in range(50, 0, -5):
            alpha = int(255 * (radio / 50) * (glow_strength / 5))
            color = (*color_primary, alpha)
            pygame.draw.circle(self.glow_surface, color, centro, radio)
    
    def _dibujar_barra_progreso(self, superficie: pygame.Surface,
                               x: int, y: int, ancho: int, alto: int,
                               porcentaje: float) -> None:
        """
        Dibuja una barra de progreso estilizada.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
            x (int): Posición X
            y (int): Posición Y
            ancho (int): Ancho de la barra
            alto (int): Alto de la barra
            porcentaje (float): Valor de progreso (0-100)
        """
        # Asegurar que el porcentaje esté entre 0 y 100
        porcentaje = max(0, min(100, porcentaje))
        
        # Fondo de la barra con borde
        pygame.draw.rect(superficie, self.theme_manager.obtener_color("primary"),
                        (x - 2, y - 2, ancho + 4, alto + 4), border_radius=5)
        
        # Fondo interno de la barra
        pygame.draw.rect(superficie, self.theme_manager.obtener_color("dark"),
                        (x, y, ancho, alto), border_radius=5)
        
        # Progreso
        if porcentaje > 0:
            ancho_progreso = int((ancho * porcentaje) / 100)
            if ancho_progreso > 0:
                rect_progreso = pygame.Rect(x, y, ancho_progreso, alto)
                color_progreso = self.theme_manager.obtener_color("accent")
                pygame.draw.rect(superficie, color_progreso,
                               rect_progreso, border_radius=5)
                
                # Efecto de brillo en la barra
                brillo_alpha = int(128 + 64 * math.sin(self.tiempo_acumulado * 2))
                brillo_superficie = pygame.Surface((ancho_progreso, alto // 2), pygame.SRCALPHA)
                pygame.draw.rect(brillo_superficie, (*color_progreso, brillo_alpha),
                               (0, 0, ancho_progreso, alto // 2), border_radius=3)
                superficie.blit(brillo_superficie, (x, y))
    
    def _crear_particula(self, x: float, y: float) -> None:
        """
        Crea una nueva partícula en la posición especificada.
        
        Args:
            x (float): Posición X
            y (float): Posición Y
        """
        if len(self.particulas) < self.max_particulas:
            particula = {
                'x': x,
                'y': y,
                'dx': random.uniform(-2, 2),
                'dy': random.uniform(-4, -2),
                'vida': 1.0,
                'color': self.theme_manager.obtener_color("primary"),
                'tamaño': random.uniform(2, 4)
            }
            self.particulas.append(particula)
    
    def _actualizar_particulas(self, delta_tiempo: float) -> None:
        """
        Actualiza el sistema de partículas.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        for particula in self.particulas[:]:
            particula['vida'] -= delta_tiempo * 2
            if particula['vida'] <= 0:
                self.particulas.remove(particula)
                continue
            
            particula['x'] += particula['dx']
            particula['y'] += particula['dy']
            particula['dy'] += 0.1  # Gravedad
    
    def _dibujar_particulas(self, superficie: pygame.Surface) -> None:
        """
        Dibuja todas las partículas activas.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
        """
        for particula in self.particulas:
            alpha = int(255 * particula['vida'])
            color = (*particula['color'], alpha)
            pos = (int(particula['x']), int(particula['y']))
            pygame.draw.circle(superficie, color, pos,
                             int(particula['tamaño'] * particula['vida']))
    
    def dibujar_hud(self, superficie: pygame.Surface, nivel: int, vidas: int,
                    porcentaje: float, tiempo_restante: float, modo_debug: bool = False,
                    porcentaje_meta: float = 75.0, puntaje: int = 0) -> None:
        """
        Dibuja el HUD premium con todos los efectos visuales.
        """
        # Dimensiones y posición de la barra lateral
        ancho_barra = 200
        x_barra = self.ancho - ancho_barra
        margen_lateral = 20
        
        # Contenedor principal (barra lateral)
        pygame.draw.rect(superficie, (*self.theme_manager.obtener_color("dark"), 230),
                        (x_barra, 0, ancho_barra, self.alto))
        
        # Separador decorativo
        pygame.draw.line(superficie, self.theme_manager.obtener_color("primary"),
                        (x_barra, 0), (x_barra, self.alto), 2)
        
        # Nivel
        y_actual = 30
        texto_nivel = self.fuente_principal.render(
            f"NIVEL {nivel}",
            True,
            self.theme_manager.obtener_color("primary")
        )
        x_texto = x_barra + (ancho_barra - texto_nivel.get_width()) // 2
        superficie.blit(texto_nivel, (x_texto, y_actual))
        
        # Tiempo restante
        y_actual += 50
        texto_tiempo = self.fuente_principal.render(
            "TIEMPO",
            True,
            self.theme_manager.obtener_color("primary")
        )
        x_texto = x_barra + (ancho_barra - texto_tiempo.get_width()) // 2
        superficie.blit(texto_tiempo, (x_texto, y_actual))
        
        # Mostrar tiempo en formato MM:SS
        y_actual += 30
        minutos = int(tiempo_restante / 60)
        segundos = int(tiempo_restante % 60)
        texto_tiempo = self.fuente_numeros.render(
            f"{minutos:02d}:{segundos:02d}",
            True,
            self.theme_manager.obtener_color("accent")
        )
        x_texto = x_barra + (ancho_barra - texto_tiempo.get_width()) // 2
        superficie.blit(texto_tiempo, (x_texto, y_actual))
        
        # Progreso
        y_actual += 50
        texto_progreso = self.fuente_principal.render(
            "PROGRESO",
            True,
            self.theme_manager.obtener_color("primary")
        )
        x_texto = x_barra + (ancho_barra - texto_progreso.get_width()) // 2
        superficie.blit(texto_progreso, (x_texto, y_actual))
        
        # Barra de progreso
        y_actual += 30
        ancho_barra_progreso = ancho_barra - (margen_lateral * 2)
        self._dibujar_barra_progreso(
            superficie,
            x_barra + margen_lateral,
            y_actual,
            ancho_barra_progreso,
            20,  # Alto de la barra
            porcentaje
        )
        
        # Porcentaje actual/meta
        y_actual += 30
        texto_porcentaje = self.fuente_numeros.render(
            f"{porcentaje:.1f}% / {porcentaje_meta:.1f}%",
            True,
            self.theme_manager.obtener_color("accent")
        )
        x_texto = x_barra + (ancho_barra - texto_porcentaje.get_width()) // 2
        superficie.blit(texto_porcentaje, (x_texto, y_actual))
        
        # Puntaje
        y_actual += 60
        texto_puntaje = self.fuente_principal.render(
            "PUNTAJE",
            True,
            self.theme_manager.obtener_color("primary")
        )
        x_texto = x_barra + (ancho_barra - texto_puntaje.get_width()) // 2
        superficie.blit(texto_puntaje, (x_texto, y_actual))
        
        y_actual += 30
        texto_puntaje = self.fuente_numeros.render(
            f"{puntaje:,}",
            True,
            self.theme_manager.obtener_color("accent")
        )
        x_texto = x_barra + (ancho_barra - texto_puntaje.get_width()) // 2
        superficie.blit(texto_puntaje, (x_texto, y_actual))
        
        # Vidas
        y_actual += 60
        texto_vidas = self.fuente_principal.render(
            "VIDAS",
            True,
            self.theme_manager.obtener_color("primary")
        )
        x_texto = x_barra + (ancho_barra - texto_vidas.get_width()) // 2
        superficie.blit(texto_vidas, (x_texto, y_actual))
        
        # Dibujar corazones
        y_actual += 30
        x_corazon = x_barra + margen_lateral
        for i in range(vidas):
            superficie.blit(self.corazon_base, (x_corazon, y_actual))
            x_corazon += 50
        
        # Partículas
        self._actualizar_particulas(1/60)
        self._dibujar_particulas(superficie)
        
        # Información de debug
        if modo_debug:
            y_actual = self.alto - 30
            texto_debug = self.fuente_principal.render(
                "DEBUG",
                True,
                self.theme_manager.obtener_color("accent")
            )
            x_texto = x_barra + (ancho_barra - texto_debug.get_width()) // 2
            superficie.blit(texto_debug, (x_texto, y_actual))
    
    def iniciar_transicion(self) -> None:
        """Inicia una transición de pantalla."""
        self.en_transicion = True
        self.alpha_transicion = 0
        self.direccion_transicion = 1
    
    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza los elementos animados de la UI.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        if self.en_transicion:
            velocidad = self.theme_manager.obtener_efecto("transition_speed")
            self.alpha_transicion += self.direccion_transicion * delta_tiempo * 255 * velocidad
            if self.alpha_transicion >= 255:
                self.alpha_transicion = 255
                self.direccion_transicion = -1
            elif self.alpha_transicion <= 0:
                self.alpha_transicion = 0
                self.en_transicion = False
    
    def dibujar_transicion(self, superficie: pygame.Surface) -> None:
        """
        Dibuja el efecto de transición.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
        """
        if self.en_transicion:
            transicion = pygame.Surface((self.ancho, self.alto))
            transicion.fill(self.theme_manager.obtener_color("dark"))
            transicion.set_alpha(int(self.alpha_transicion))
            superficie.blit(transicion, (0, 0))
    
    def mostrar_mensaje(self, superficie: pygame.Surface, mensaje: str) -> None:
        """
        Muestra un mensaje estilizado en pantalla.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
            mensaje (str): Mensaje a mostrar
        """
        texto = self.fuente_principal.render(
            mensaje,
            True,
            self.theme_manager.obtener_color("primary")
        )
        sombra = self.fuente_principal.render(
            mensaje,
            True,
            self.theme_manager.obtener_color("dark")
        )
        
        pos_x = (self.ancho - texto.get_width()) // 2
        pos_y = (self.alto - texto.get_height()) // 2
        
        # Dibujar sombra con desplazamiento
        superficie.blit(sombra, (pos_x + 2, pos_y + 2))
        superficie.blit(texto, (pos_x, pos_y))
    
    def renderizar_texto_neon(self, texto: str, color: Tuple[int, int, int], tamaño_fuente: int) -> Tuple[pygame.Surface, pygame.Surface]:
        """
        Renderiza texto con efecto neón.
        
        Args:
            texto (str): Texto a renderizar
            color (Tuple[int, int, int]): Color del texto
            tamaño_fuente (int): Tamaño de la fuente
            
        Returns:
            Tuple[pygame.Surface, pygame.Surface]: Superficies con el efecto glow y el texto
        """
        # Usar una fuente del sistema
        fuente = pygame.font.SysFont("arial", tamaño_fuente, bold=True)
        
        # Renderizar el texto normal
        texto_surface = fuente.render(texto, True, color)
        
        # Crear superficie para el glow
        glow = pygame.Surface((texto_surface.get_width() + 10, texto_surface.get_height() + 10), pygame.SRCALPHA)
        
        # Renderizar múltiples copias del texto con diferentes tamaños para crear el efecto glow
        for offset in range(5, 0, -1):
            glow_color = (*color, 50 - offset * 10)  # Reducir el alpha gradualmente
            glow_surface = fuente.render(texto, True, glow_color)
            glow.blit(glow_surface, (offset, offset))
            glow.blit(glow_surface, (offset + 1, offset))
            glow.blit(glow_surface, (offset, offset + 1))
            glow.blit(glow_surface, (offset + 1, offset + 1))
        
        return glow, texto_surface

    def mostrar_nivel_completado(self, superficie: pygame.Surface,
                               imagen_fondo: Optional[pygame.Surface] = None,
                               nivel_actual: int = 1) -> bool:
        """
        Muestra la pantalla de nivel completado con efectos visuales mejorados.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
            imagen_fondo (Optional[pygame.Surface]): Imagen de fondo del nivel
            nivel_actual (int): Número del nivel actual
            
        Returns:
            bool: True si se hizo clic en continuar
        """
        if imagen_fondo:
            imagen_completa = imagen_fondo.copy()
            superficie.blit(imagen_completa, (0, 0))
        
        # Panel lateral derecho más ancho
        panel_width = 400
        panel = pygame.Surface((panel_width, superficie.get_height()), pygame.SRCALPHA)
        for y in range(panel.get_height()):
            alpha = max(180 - y // 4, 0)  # Panel más opaco
            pygame.draw.line(panel, (20, 20, 50, alpha), (0, y), (panel_width, y))
        superficie.blit(panel, (superficie.get_width() - panel_width, 0))
        
        tiempo = pygame.time.get_ticks() / 1000
        x_base = superficie.get_width() - panel_width + 20
        
        # Fuentes más pequeñas para mejor ajuste
        fuente_grande = pygame.font.SysFont("arial", 42, bold=True)
        fuente_mediana = pygame.font.SysFont("arial", 32, bold=True)
        fuente_pequeña = pygame.font.SysFont("arial", 24, bold=True)
        
        # Mensaje 1: ¡Felicidades!
        y_pos = 80  # Empezar un poco más arriba
        escala = 1.0 + math.sin(tiempo * 2) * 0.1  # Efecto de escala pulsante
        
        texto1 = "¡FELICIDADES!"
        texto2 = f"NIVEL {nivel_actual}"
        texto3 = "COMPLETADO"
        
        # Colores brillantes
        color_titulo = (255, 215, 0)  # Dorado
        color_nivel = (255, 100, 100)  # Rojo claro
        color_completado = (100, 255, 100)  # Verde claro
        
        # Renderizar mensajes con sombra
        def renderizar_con_sombra(fuente, texto, color, y_pos, escala=1.0):
            # Sombra
            texto_surface = fuente.render(texto, True, (0, 0, 0))
            rect = texto_surface.get_rect(centerx=x_base + panel_width//2 + 2, centery=y_pos + 2)
            if escala != 1.0:
                nuevo_ancho = int(rect.width * escala)
                nuevo_alto = int(rect.height * escala)
                texto_surface = pygame.transform.scale(texto_surface, (nuevo_ancho, nuevo_alto))
                rect = texto_surface.get_rect(centerx=x_base + panel_width//2 + 2, centery=y_pos + 2)
            superficie.blit(texto_surface, rect)
            
            # Texto principal
            texto_surface = fuente.render(texto, True, color)
            rect = texto_surface.get_rect(centerx=x_base + panel_width//2, centery=y_pos)
            if escala != 1.0:
                nuevo_ancho = int(rect.width * escala)
                nuevo_alto = int(rect.height * escala)
                texto_surface = pygame.transform.scale(texto_surface, (nuevo_ancho, nuevo_alto))
                rect = texto_surface.get_rect(centerx=x_base + panel_width//2, centery=y_pos)
            superficie.blit(texto_surface, rect)
            return rect.bottom + 15  # Reducir el espacio entre líneas
        
        # Renderizar los tres mensajes principales
        y_pos = renderizar_con_sombra(fuente_grande, texto1, color_titulo, y_pos, escala)
        y_pos = renderizar_con_sombra(fuente_grande, texto2, color_nivel, y_pos)
        y_pos = renderizar_con_sombra(fuente_grande, texto3, color_completado, y_pos)
        
        # Mensaje 2: ¿Quieres ver más?
        # y_pos += 30
        # alpha = int(abs(math.sin(tiempo * 3)) * 255)  # Efecto de parpadeo suave
        # color_mensaje2 = (100, 200, 255, alpha)  # Azul claro
        
        # texto4 = "¿QUIERES VER MÁS?"
        # texto5 = "¡BÚSCANOS EN GOOGLE!"
        
        # y_pos = renderizar_con_sombra(fuente_mediana, texto4, color_mensaje2, y_pos)
        # y_pos = renderizar_con_sombra(fuente_mediana, texto5, color_mensaje2, y_pos)
        
        # Mensaje 3: Presiona ESC
        y_pos += 30
        if int(tiempo * 2) % 2 == 0:  # Efecto de parpadeo
            texto6 = "PRESIONA ESC"
            texto7 = "PARA EL SIGUIENTE NIVEL"
            
            y_pos = renderizar_con_sombra(fuente_pequeña, texto6, (255, 255, 255), y_pos)
            renderizar_con_sombra(fuente_pequeña, texto7, (255, 255, 255), y_pos)
        
        return False