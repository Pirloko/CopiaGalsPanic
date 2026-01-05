import json
import os
from typing import Dict, Any, Optional

class ThemeManager:
    """Clase que maneja los temas visuales del juego."""
    
    def __init__(self):
        """Inicializa el gestor de temas."""
        self.temas: Dict[str, Dict[str, Any]] = {}
        self.tema_actual: str = "neon_nights"
        self._cargar_temas()
    
    def _cargar_temas(self) -> None:
        """Carga los temas desde el archivo de configuración."""
        try:
            with open(os.path.join("config", "themes.json"), "r") as f:
                self.temas = json.load(f)
        except FileNotFoundError:
            print("Archivo de temas no encontrado, usando valores por defecto")
            self._crear_temas_por_defecto()
        except json.JSONDecodeError:
            print("Error al leer el archivo de temas, usando valores por defecto")
            self._crear_temas_por_defecto()
    
    def _crear_temas_por_defecto(self) -> None:
        """Crea los temas por defecto si no se puede cargar el archivo."""
        self.temas = {
            "neon_nights": {
                "name": "Neon Nights",
                "colors": {
                    "primary": "#00ffff",
                    "secondary": "#ff1493",
                    "accent": "#7b2ff7",
                    "dark": "#120458",
                    "light": "#edf2f4"
                },
                "effects": {
                    "glow_strength": 5,
                    "particle_count": 100,
                    "transition_speed": 0.3
                }
            }
        }
    
    def cambiar_tema(self, nombre_tema: str) -> bool:
        """
        Cambia al tema especificado.
        
        Args:
            nombre_tema (str): Nombre del tema a activar
            
        Returns:
            bool: True si el cambio fue exitoso
        """
        if nombre_tema in self.temas:
            self.tema_actual = nombre_tema
            return True
        return False
    
    def obtener_tema_actual(self) -> Dict[str, Any]:
        """
        Obtiene la configuración del tema actual.
        
        Returns:
            Dict[str, Any]: Configuración del tema actual
        """
        return self.temas[self.tema_actual]
    
    def obtener_color(self, nombre_color: str) -> tuple:
        """
        Obtiene un color del tema actual.
        
        Args:
            nombre_color (str): Nombre del color a obtener
            
        Returns:
            tuple: Color en formato RGB
        """
        color_hex = self.temas[self.tema_actual]["colors"].get(nombre_color, "#ffffff")
        return self._hex_a_rgb(color_hex)
    
    def obtener_efecto(self, nombre_efecto: str) -> Any:
        """
        Obtiene un valor de efecto del tema actual.
        
        Args:
            nombre_efecto (str): Nombre del efecto a obtener
            
        Returns:
            Any: Valor del efecto
        """
        return self.temas[self.tema_actual]["effects"].get(nombre_efecto, 0)
    
    @staticmethod
    def _hex_a_rgb(hex_color: str) -> tuple:
        """
        Convierte un color hexadecimal a RGB.
        
        Args:
            hex_color (str): Color en formato hexadecimal (#RRGGBB)
            
        Returns:
            tuple: Color en formato RGB (r, g, b)
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def lista_temas(self) -> list:
        """
        Obtiene la lista de temas disponibles.
        
        Returns:
            list: Lista de nombres de temas
        """
        return list(self.temas.keys()) 