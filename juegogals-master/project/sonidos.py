import pygame
from typing import Dict, Optional

class GestorSonidos:
    """Clase que maneja los efectos de sonido del juego."""
    
    def __init__(self):
        """Inicializa el gestor de sonidos."""
        self.sonidos: Dict[str, Optional[pygame.mixer.Sound]] = {}
        self.volumen = 0.5
        
        # Intentar cargar los sonidos
        try:
            self.sonidos['impacto'] = pygame.mixer.Sound('sonidos/impacto.wav')
            self.sonidos['victoria'] = pygame.mixer.Sound('sonidos/victoria.wav')
            self.sonidos['daño'] = pygame.mixer.Sound('sonidos/daño.wav')
            self.sonidos['powerup'] = pygame.mixer.Sound('sonidos/powerup.wav')
            self.sonidos['explosion'] = pygame.mixer.Sound('sonidos/explosion.wav')
        except:
            print("No se pudieron cargar algunos sonidos")
            # Si no se pueden cargar, usar None
            for nombre in ['impacto', 'victoria', 'daño', 'powerup', 'explosion']:
                if nombre not in self.sonidos:
                    self.sonidos[nombre] = None
        
        # Establecer volumen
        for sonido in self.sonidos.values():
            if sonido:
                sonido.set_volume(self.volumen)
    
    def reproducir_sonido(self, nombre: str) -> None:
        """
        Reproduce un sonido por su nombre.
        
        Args:
            nombre (str): Nombre del sonido a reproducir
        """
        if nombre in self.sonidos and self.sonidos[nombre]:
            self.sonidos[nombre].play()
    
    def actualizar(self) -> None:
        """Actualiza el estado de los sonidos."""
        pass  # Por ahora no necesitamos actualización
    
    def establecer_volumen(self, volumen: float) -> None:
        """
        Establece el volumen de todos los sonidos.
        
        Args:
            volumen (float): Volumen entre 0.0 y 1.0
        """
        self.volumen = max(0.0, min(1.0, volumen))
        for sonido in self.sonidos.values():
            if sonido:
                sonido.set_volume(self.volumen) 