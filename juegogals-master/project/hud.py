import pygame
import os
from typing import Tuple, Optional

class HUD:
    """Clase que maneja el HUD moderno del juego."""
    
    def __init__(self, ancho: int, alto: int):
        """
        Inicializa el HUD.
        
        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
        """
        self.ancho = ancho
        self.alto = alto
        
        # Cargar fuentes
        pygame.font.init()
        try:
            ruta_fuente = os.path.join("project", "assets", "fonts", "Roboto-Bold.ttf")
            self.fuente_grande = pygame.font.Font(ruta_fuente, 48)
            self.fuente_normal = pygame.font.Font(ruta_fuente, 36)
            self.fuente_pequeña = pygame.font.Font(ruta_fuente, 24)
        except:
            # Fallback a fuente por defecto si no se encuentra Roboto
            print("No se pudo cargar la fuente Roboto, usando fuente por defecto")
            self.fuente_grande = pygame.font.Font(None, 48)
            self.fuente_normal = pygame.font.Font(None, 36)
            self.fuente_pequeña = pygame.font.Font(None, 24)
        
        # Colores modernos con esquema neón
        self.color_texto = (220, 220, 220)  # Casi blanco
        self.color_sombra = (20, 20, 20)    # Casi negro
        self.color_acento = (0, 255, 255)   # Cyan neón
        self.color_vida = (255, 50, 50)     # Rojo neón
        self.color_barra_bg = (40, 40, 40)  # Gris oscuro
        self.color_barra_borde = (60, 60, 60)  # Gris más claro
        
        # Dimensiones y posiciones
        self.margen = 20
        self.alto_barra = 30
        self.ancho_barra = 200
        self.espacio_iconos = 5
        self.radio_brillo = 15
        
        # Efectos visuales
        self.brillo_alpha = 0
        self.direccion_brillo = 1
        self.velocidad_brillo = 3
        
        # Cargar íconos
        self.iconos = {
            "vida": self._crear_icono_vida(),
            "nivel": self._crear_icono_nivel(),
            "tiempo": self._crear_icono_tiempo()
        }
        
    def _crear_icono_vida(self) -> pygame.Surface:
        """Crea un icono de corazón."""
        superficie = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Dibujar corazón
        color = self.color_vida
        puntos = [
            (16, 8), (20, 4), (24, 4), (28, 8),
            (28, 12), (16, 28), (4, 12),
            (4, 8), (8, 4), (12, 4), (16, 8)
        ]
        pygame.draw.polygon(superficie, color, puntos)
        
        return superficie
    
    def _crear_icono_nivel(self) -> pygame.Surface:
        """Crea un icono de estrella."""
        superficie = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Dibujar estrella
        color = self.color_acento
        centro = (16, 16)
        puntos = []
        for i in range(5):
            # Punto exterior
            angulo = i * 72 - 90
            rad = pygame.math.Vector2()
            rad.from_polar((14, angulo))
            puntos.append((centro[0] + rad.x, centro[1] + rad.y))
            # Punto interior
            angulo += 36
            rad.from_polar((6, angulo))
            puntos.append((centro[0] + rad.x, centro[1] + rad.y))
        
        pygame.draw.polygon(superficie, color, puntos)
        
        return superficie
    
    def _crear_icono_tiempo(self) -> pygame.Surface:
        """Crea un icono de reloj."""
        superficie = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Dibujar círculo del reloj
        color = self.color_acento
        pygame.draw.circle(superficie, color, (16, 16), 14, 2)
        
        # Dibujar manecillas
        pygame.draw.line(superficie, color, (16, 16), (16, 8), 2)
        pygame.draw.line(superficie, color, (16, 16), (22, 16), 2)
        
        return superficie
    
    def _dibujar_texto_con_efecto(self, superficie: pygame.Surface, texto: str,
                                 x: int, y: int, fuente: pygame.font.Font,
                                 color: Tuple[int, int, int]) -> None:
        """
        Dibuja texto con efecto de sombra y brillo.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
            texto (str): Texto a mostrar
            x (int): Posición X
            y (int): Posición Y
            fuente (pygame.font.Font): Fuente a usar
            color (Tuple[int, int, int]): Color del texto
        """
        # Sombra
        sombra = fuente.render(texto, True, self.color_sombra)
        superficie.blit(sombra, (x + 2, y + 2))
        
        # Texto principal
        texto_surface = fuente.render(texto, True, color)
        superficie.blit(texto_surface, (x, y))
        
        # Efecto de brillo
        if self.brillo_alpha > 0:
            brillo = fuente.render(texto, True, self.color_acento)
            brillo.set_alpha(self.brillo_alpha)
            superficie.blit(brillo, (x, y))
    
    def _dibujar_barra_progreso(self, superficie: pygame.Surface, x: int, y: int,
                               valor: float, max_valor: float) -> None:
        """
        Dibuja una barra de progreso moderna con efectos.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
            x (int): Posición X
            y (int): Posición Y
            valor (float): Valor actual
            max_valor (float): Valor máximo
        """
        # Fondo de la barra
        pygame.draw.rect(superficie, self.color_barra_bg,
                        (x, y, self.ancho_barra, self.alto_barra))
        pygame.draw.rect(superficie, self.color_barra_borde,
                        (x, y, self.ancho_barra, self.alto_barra), 1)
        
        # Calcular progreso
        progreso = min(1.0, valor / max_valor)
        ancho_progreso = int(self.ancho_barra * progreso)
        
        if ancho_progreso > 0:
            # Barra de progreso con gradiente
            for i in range(ancho_progreso):
                factor = i / self.ancho_barra
                color = (
                    int(self.color_acento[0] * (0.7 + 0.3 * factor)),
                    int(self.color_acento[1] * (0.7 + 0.3 * factor)),
                    int(self.color_acento[2] * (0.7 + 0.3 * factor))
                )
                pygame.draw.line(superficie, color,
                               (x + i, y + 2),
                               (x + i, y + self.alto_barra - 2))
            
            # Brillo en el borde del progreso
            brillo = pygame.Surface((4, self.alto_barra), pygame.SRCALPHA)
            for i in range(4):
                alpha = int(150 * (1 - i/4))
                pygame.draw.line(brillo, (*self.color_acento, alpha),
                               (i, 0), (i, self.alto_barra))
            superficie.blit(brillo, (x + ancho_progreso - 2, y))
    
    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza los efectos visuales del HUD.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        # Actualizar efecto de brillo
        self.brillo_alpha += self.direccion_brillo * self.velocidad_brillo
        if self.brillo_alpha >= 100:
            self.brillo_alpha = 100
            self.direccion_brillo = -1
        elif self.brillo_alpha <= 0:
            self.brillo_alpha = 0
            self.direccion_brillo = 1
    
    def dibujar(self, superficie: pygame.Surface, nivel: int, vidas: int,
                porcentaje: float, tiempo: float) -> None:
        """
        Dibuja el HUD completo.
        
        Args:
            superficie (pygame.Surface): Superficie donde dibujar
            nivel (int): Número de nivel actual
            vidas (int): Número de vidas restantes
            porcentaje (float): Porcentaje completado
            tiempo (float): Tiempo restante en segundos
        """
        # Nivel (esquina superior izquierda)
        superficie.blit(self.iconos["nivel"],
                       (self.margen, self.margen))
        self._dibujar_texto_con_efecto(
            superficie,
            f"Nivel {nivel}",
            self.margen + 40, self.margen + 4,
            self.fuente_normal,
            self.color_texto
        )
        
        # Vidas (debajo del nivel)
        y_vidas = self.margen + 50
        for i in range(vidas):
            superficie.blit(self.iconos["vida"],
                          (self.margen + i * (32 + self.espacio_iconos), y_vidas))
        
        # Barra de progreso (esquina superior derecha)
        x_barra = self.ancho - self.margen - self.ancho_barra
        self._dibujar_barra_progreso(superficie, x_barra, self.margen,
                                   porcentaje, 100)
        
        # Porcentaje sobre la barra
        texto_porcentaje = f"{porcentaje:.1f}%"
        self._dibujar_texto_con_efecto(
            superficie,
            texto_porcentaje,
            x_barra + self.ancho_barra - 70,
            self.margen + self.alto_barra + 5,
            self.fuente_pequeña,
            self.color_acento
        )
        
        # Tiempo restante (centro superior)
        minutos = int(tiempo / 60)
        segundos = int(tiempo % 60)
        texto_tiempo = f"{minutos:02d}:{segundos:02d}"
        
        # Color del tiempo basado en el tiempo restante
        color_tiempo = self.color_texto
        if tiempo <= 30:  # Últimos 30 segundos
            if tiempo <= 10:  # Últimos 10 segundos
                color_tiempo = (255, 0, 0)  # Rojo
            else:
                color_tiempo = (255, 165, 0)  # Naranja
        
        # Dibujar tiempo en el centro superior
        x_tiempo = self.ancho // 2 - 50
        y_tiempo = self.margen
        
        # Icono de reloj
        superficie.blit(self.iconos["tiempo"],
                       (x_tiempo - 40, y_tiempo))
        
        # Texto del tiempo con efecto parpadeante en los últimos 10 segundos
        if tiempo <= 10 and int(tiempo * 2) % 2 == 0:
            color_tiempo = (255, 255, 255)  # Parpadeo a blanco
        
        self._dibujar_texto_con_efecto(
            superficie,
            texto_tiempo,
            x_tiempo,
            y_tiempo,
            self.fuente_grande,  # Usar fuente más grande para el tiempo
            color_tiempo
        ) 