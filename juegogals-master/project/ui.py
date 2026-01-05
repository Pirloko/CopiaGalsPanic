import pygame
from typing import Tuple, Optional
from utils import dibujar_texto_con_borde, crear_barra_progreso
from hud import HUD

class UI:
    """Clase que maneja la interfaz de usuario del juego."""
    
    def __init__(self, ancho: int, alto: int):
        """
        Inicializa la interfaz de usuario.
        
        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        
        # Crear HUD moderno
        self.hud = HUD(ancho, alto)
        
        # Estado de transición
        self.en_transicion = False
        self.tiempo_transicion = 0
        self.duracion_transicion = 1.0  # segundos
        
        # Estado de nivel completado
        self.nivel_completado = False
        self.boton_siguiente = pygame.Rect(self.ancho // 2 - 100, self.alto - 100, 200, 50)
        self.mouse_sobre_boton = False
        
        # Superficie para transición
        self.superficie_transicion = pygame.Surface((ancho, alto))
        self.superficie_transicion.fill((0, 0, 0))
        
        # Estado de debug
        self.modo_debug = False
        
        # Tiempo de juego
        self.tiempo_juego = 0
    
    def dibujar_hud(self, pantalla: pygame.Surface, nivel: int, vidas: int,
                   porcentaje: float, modo_debug: bool = False) -> None:
        """
        Dibuja el HUD del juego.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
            nivel (int): Número de nivel actual
            vidas (int): Número de vidas restantes
            porcentaje (float): Porcentaje completado del nivel
            modo_debug (bool): Si está activo el modo debug
        """
        self.hud.dibujar(pantalla, nivel, vidas, porcentaje, self.tiempo_juego)
        
        # Información de debug
        if modo_debug:
            self.dibujar_info_debug(pantalla)
    
    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado de la UI.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        # Actualizar tiempo de juego
        self.tiempo_juego += delta_tiempo
        
        # Actualizar HUD
        self.hud.actualizar(delta_tiempo)
        
        # Actualizar transición
        if self.en_transicion:
            self.tiempo_transicion += delta_tiempo
            if self.tiempo_transicion >= self.duracion_transicion:
                self.en_transicion = False
                self.tiempo_transicion = 0
    
    def dibujar_info_debug(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja información de debug en pantalla.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        """
        texto_debug = "DEBUG MODE"
        self.hud._dibujar_texto_con_efecto(
            pantalla,
            texto_debug,
            self.ancho - 100,
            10,
            self.hud.fuente_pequeña,
            self.hud.color_acento
        )
    
    def iniciar_transicion(self) -> None:
        """Inicia una transición entre niveles."""
        self.en_transicion = True
        self.tiempo_transicion = 0
    
    def dibujar_transicion(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja la transición.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        """
        if not self.en_transicion:
            return
        
        # Calcular opacidad
        alpha = int(255 * (1.0 - self.tiempo_transicion / self.duracion_transicion))
        
        # Crear superficie para el fade
        fade = pygame.Surface((self.ancho, self.alto))
        fade.fill((0, 0, 0))
        fade.set_alpha(alpha)
        
        pantalla.blit(fade, (0, 0))
    
    def mostrar_nivel_completado(self, pantalla: pygame.Surface,
                               imagen_completa: pygame.Surface) -> bool:
        """
        Muestra la imagen completa y el botón de siguiente nivel.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
            imagen_completa (pygame.Surface): Imagen completa del nivel
            
        Returns:
            bool: True si se debe pasar al siguiente nivel
        """
        # Mostrar imagen completa
        pantalla.blit(imagen_completa, (0, 0))
        
        # Mostrar mensaje de nivel completado
        self.hud._dibujar_texto_con_efecto(
            pantalla,
            "¡Nivel Completado!",
            self.ancho // 2 - 150,
            50,
            self.hud.fuente_grande,
            self.hud.color_acento
        )
        
        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_sobre_boton = self.boton_siguiente.collidepoint(mouse_pos)
        
        # Dibujar botón con efecto neón
        color_boton = self.hud.color_acento if self.mouse_sobre_boton else (40, 40, 40)
        pygame.draw.rect(pantalla, color_boton, self.boton_siguiente)
        pygame.draw.rect(pantalla, self.hud.color_acento, self.boton_siguiente, 2)
        
        # Texto del botón
        self.hud._dibujar_texto_con_efecto(
            pantalla,
            "Siguiente Nivel",
            self.boton_siguiente.centerx - 80,
            self.boton_siguiente.centery - 15,
            self.hud.fuente_normal,
            self.hud.color_texto
        )
        
        # Verificar clic en el botón
        return self.mouse_sobre_boton and pygame.mouse.get_pressed()[0]
    
    def mostrar_mensaje(self, pantalla: pygame.Surface, mensaje: str,
                       pos: Optional[Tuple[int, int]] = None) -> None:
        """
        Muestra un mensaje en pantalla.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
            mensaje (str): Mensaje a mostrar
            pos (Optional[Tuple[int, int]]): Posición donde mostrar el mensaje
        """
        if pos is None:
            pos = (self.ancho // 2 - 100, self.alto // 2)
        
        self.hud._dibujar_texto_con_efecto(
            pantalla,
            mensaje,
            pos[0],
            pos[1],
            self.hud.fuente_grande,
            self.hud.color_texto
        )