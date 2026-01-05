import pygame
import os
from typing import List, Tuple, Set, Optional
from utils import cargar_imagenes, rellenar_poligono, es_poligono_valido, ordenar_puntos_horario

class Nivel:
    """Clase que maneja el nivel, imágenes de fondo y áreas reveladas."""
    
    def __init__(self, ancho: int, alto: int, carpeta_imagenes: str):
        """
        Inicializa un nivel.
        
        Args:
            ancho (int): Ancho de la pantalla
            alto (int): Alto de la pantalla
            carpeta_imagenes (str): Ruta a la carpeta con imágenes
        """
        self.ancho = ancho
        self.alto = alto
        self.carpeta_imagenes = carpeta_imagenes
        
        # Cargar todas las imágenes disponibles
        self.imagenes_disponibles = cargar_imagenes(carpeta_imagenes)
        self.total_niveles = len(self.imagenes_disponibles)
        
        # Superficies para el manejo de imágenes
        self.imagen_fondo = None
        self.imagen_revelada = None
        self.mascara_debug = None
        
        # Área segura y trazado
        self.area_segura = set()
        self.vertices_trazado = []
        self.trazado_actual = []
        
        # Contadores y estado
        self.total_pixeles = ancho * alto
        self.pixeles_revelados = 0
        self.porcentaje_victoria = 75.0  # Porcentaje base necesario para ganar
        
        # Tiempo límite
        self.tiempo_limite = 90.0  # 1 minuto y 30 segundos
        self.tiempo_restante = self.tiempo_limite
        self.tiempo_agotado = False
        
        # Sistema de puntaje
        self.puntaje_nivel = 0
        self.puntos_por_pixel = 1
        self.puntos_por_segundo = 10
        self.bonus_porcentaje = 100  # Puntos extra por cada 1% sobre el mínimo
        
        # Modo debug
        self.modo_debug = False
    
    def inicializar_area_segura(self) -> None:
        """Inicializa el área segura como el borde de la pantalla."""
        self.area_segura = set()
        
        # Añadir bordes
        for x in range(self.ancho):
            self.area_segura.add((x, 0))
            self.area_segura.add((x, self.alto - 1))
        for y in range(self.alto):
            self.area_segura.add((0, y))
            self.area_segura.add((self.ancho - 1, y))
    
        self.pixeles_revelados = len(self.area_segura)
    
    def cargar_nivel(self, numero_nivel: int) -> bool:
        """
        Carga un nivel específico.
        
        Args:
            numero_nivel (int): Número del nivel a cargar
            
        Returns:
            bool: True si se cargó correctamente
        """
        if not self.imagenes_disponibles:
            print("No hay imágenes disponibles")
            return False
        
        # Ajustar número de nivel si está fuera de rango
        numero_nivel = ((numero_nivel - 1) % len(self.imagenes_disponibles)) + 1
        
        # Ajustar dificultad según el nivel
        self.porcentaje_victoria = min(75.0 + (numero_nivel - 1) * 2, 95.0)  # Aumenta 2% por nivel, máximo 95%
        self.tiempo_limite = max(90.0 - (numero_nivel - 1) * 5, 60.0)  # Reduce 5 segundos por nivel, mínimo 60
        
        ruta_imagen = self.imagenes_disponibles[numero_nivel - 1]
        
        try:
            # Cargar y redimensionar imagen
            imagen_original = pygame.image.load(ruta_imagen).convert()
            self.imagen_fondo = pygame.transform.scale(imagen_original, (self.ancho, self.alto))
            
            # Crear superficie para la imagen revelada
            self.imagen_revelada = pygame.Surface((self.ancho, self.alto))
            self.imagen_revelada.fill((0, 0, 0))
            
            # Crear máscara para debug
            self.mascara_debug = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            self.mascara_debug.fill((0, 0, 0, 0))
            
            # Reiniciar área segura y contadores
            self.inicializar_area_segura()
            self.vertices_trazado = []
            self.trazado_actual = []
            
            # Reiniciar tiempo y puntaje
            self.tiempo_restante = self.tiempo_limite
            self.tiempo_agotado = False
            self.puntaje_nivel = 0
            
            # Revelar el borde inicial
            for x, y in self.area_segura:
                self.imagen_revelada.set_at((x, y), self.imagen_fondo.get_at((x, y)))
            
            print(f"Nivel {numero_nivel} cargado: {ruta_imagen}")
            print(f"Meta: {self.porcentaje_victoria:.1f}% | Tiempo: {int(self.tiempo_limite)} segundos")
            return True
            
        except pygame.error as e:
            print(f"Error al cargar la imagen: {e}")
            return False
    
    def es_punto_seguro(self, x: int, y: int) -> bool:
        """
        Verifica si un punto está dentro del área segura.
        
        Args:
            x (int): Coordenada X
            y (int): Coordenada Y
            
        Returns:
            bool: True si el punto es seguro
        """
        return (int(x), int(y)) in self.area_segura
    
    def iniciar_trazado(self, x: int, y: int) -> None:
        """
        Inicia un nuevo trazado desde un punto.
        
        Args:
            x (int): Coordenada X inicial
            y (int): Coordenada Y inicial
        """
        self.trazado_actual = [(x, y)]
        if self.modo_debug:
            self.vertices_trazado = [(x, y)]
    
    def agregar_punto_trazado(self, x: int, y: int) -> None:
        """
        Añade un punto al trazado actual.
        
        Args:
            x (int): Coordenada X
            y (int): Coordenada Y
        """
        punto = (int(x), int(y))
        if self.trazado_actual and punto != self.trazado_actual[-1]:
            self.trazado_actual.append(punto)
            if self.modo_debug:
                self.vertices_trazado.append(punto)
    
    def procesar_trazado(self, puntos: List[Tuple[float, float]], gestor_enemigos: Optional['GestorEnemigos'] = None) -> Tuple[bool, int]:
        """
        Procesa el trazado actual para revelar un área y eliminar enemigos.
        
        Args:
            puntos (List[Tuple[float, float]]): Lista de puntos que forman el trazado
            gestor_enemigos (Optional[GestorEnemigos]): Gestor de enemigos para eliminar los que están dentro
            
        Returns:
            Tuple[bool, int]: (Éxito del trazado, Número de enemigos eliminados)
        """
        # Si no hay puntos o el trazado fue cancelado, retornar fallo
        if not puntos or len(puntos) < 3:
            print("Trazado muy corto o cancelado")
            return False, 0
        
        # Convertir puntos a enteros y eliminar duplicados consecutivos
        puntos_enteros = []
        ultimo_punto = None
        for x, y in puntos:
            punto_actual = (int(x), int(y))
            if punto_actual != ultimo_punto:
                puntos_enteros.append(punto_actual)
                ultimo_punto = punto_actual
        
        # Verificar si hay suficientes puntos únicos
        if len(puntos_enteros) < 3:
            print("No hay suficientes puntos únicos")
            return False, 0
        
        # Verificar si el trazado es válido
        if not es_poligono_valido(puntos_enteros):
            print("Polígono no válido")
            return False, 0
        
        # Verificar si hay enemigos en el camino del trazado
        if gestor_enemigos is not None:
            for i in range(len(puntos_enteros) - 1):
                punto1 = puntos_enteros[i]
                punto2 = puntos_enteros[i + 1]
                if gestor_enemigos.verificar_colisiones_linea(punto1, punto2):
                    print("Enemigo detectado en el trazado")
                    return False, 0
        
        # Obtener área
        pixeles_nuevos = rellenar_poligono(puntos_enteros, self.ancho, self.alto)
        
        if not pixeles_nuevos:
            print("No se generaron píxeles nuevos")
            return False, 0
        
        # Eliminar enemigos dentro del área si se proporciona el gestor
        enemigos_eliminados = 0
        if gestor_enemigos is not None:
            enemigos_eliminados = gestor_enemigos.eliminar_enemigos_en_area(puntos_enteros)
        
        # Actualizar área segura y revelar píxeles
        nuevos_pixeles_count = 0
        for x, y in pixeles_nuevos:
            if (x, y) not in self.area_segura:
                nuevos_pixeles_count += 1
                self.area_segura.add((x, y))
                try:
                    color = self.imagen_fondo.get_at((x, y))
                    self.imagen_revelada.set_at((x, y), color)
                except IndexError:
                    continue
        
        # Actualizar puntaje
        self.puntaje_nivel += nuevos_pixeles_count * self.puntos_por_pixel
        
        print(f"Píxeles nuevos revelados: {nuevos_pixeles_count}")
        
        # Actualizar contadores
        self.pixeles_revelados = len(self.area_segura)
        
        # Limpiar trazado
        self.trazado_actual = []
        return True, enemigos_eliminados
    
    def obtener_porcentaje_revelado(self) -> float:
        """
        Calcula el porcentaje del nivel revelado.
        
        Returns:
            float: Porcentaje de área revelada (0-100)
        """
        return (self.pixeles_revelados / self.total_pixeles) * 100
    
    def nivel_completado(self) -> bool:
        """
        Verifica si se ha completado el nivel.
        
        Returns:
            bool: True si se alcanzó el porcentaje necesario
        """
        return self.obtener_porcentaje_revelado() >= self.porcentaje_victoria
    
    def dibujar(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja el nivel en la pantalla.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar fondo negro
        pantalla.fill((0, 0, 0))
        
        # Dibujar imagen de fondo en las áreas reveladas
        if self.imagen_fondo and self.imagen_revelada:
            # Dibujar la imagen revelada
            pantalla.blit(self.imagen_revelada, (0, 0))
            
            # Dibujar el trazado actual si existe
            if len(self.trazado_actual) > 1:
                pygame.draw.lines(pantalla, (0, 255, 255), False, self.trazado_actual, 2)
        
        # Dibujar elementos de debug si está activado
        if self.modo_debug:
            self.dibujar_debug(pantalla)
    
    def dibujar_debug(self, pantalla: pygame.Surface) -> None:
        """
        Dibuja información de debug.
        
        Args:
            pantalla (pygame.Surface): Superficie donde dibujar
        """
        # Dibujar vértices del trazado
        for x, y in self.vertices_trazado:
            pygame.draw.circle(pantalla, (255, 0, 0), (x, y), 3)
            
        # Dibujar borde del área segura
        for x, y in self.area_segura:
            es_borde = False
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in self.area_segura and 0 <= nx < self.ancho and 0 <= ny < self.alto:
                    es_borde = True
                    break
            if es_borde:
                pygame.draw.circle(pantalla, (0, 255, 0), (x, y), 1)
    
    def activar_modo_debug(self, activar: bool) -> None:
        """
        Activa o desactiva el modo debug.
        
        Args:
            activar (bool): True para activar, False para desactivar
        """
        self.modo_debug = activar

    def actualizar(self, delta_tiempo: float) -> None:
        """
        Actualiza el estado del nivel.
        
        Args:
            delta_tiempo (float): Tiempo transcurrido desde el último frame
        """
        if not self.tiempo_agotado:
            self.tiempo_restante -= delta_tiempo
            if self.tiempo_restante <= 0:
                self.tiempo_restante = 0
                self.tiempo_agotado = True

    def tiempo_agotado_nivel(self) -> bool:
        """
        Verifica si se ha agotado el tiempo del nivel.
        
        Returns:
            bool: True si se agotó el tiempo
        """
        return self.tiempo_agotado 

    def obtener_puntaje_final(self) -> int:
        """
        Calcula el puntaje final del nivel incluyendo bonificaciones.
        
        Returns:
            int: Puntaje final del nivel
        """
        # Puntos base acumulados durante el juego
        puntaje_total = self.puntaje_nivel
        
        # Bonus por tiempo restante
        if self.nivel_completado() and not self.tiempo_agotado:
            puntaje_total += int(self.tiempo_restante) * self.puntos_por_segundo
        
        # Bonus por exceder el porcentaje requerido
        porcentaje_actual = self.obtener_porcentaje_revelado()
        if porcentaje_actual > self.porcentaje_victoria:
            porcentaje_extra = porcentaje_actual - self.porcentaje_victoria
            puntaje_total += int(porcentaje_extra * self.bonus_porcentaje)
        
        return puntaje_total

    def obtener_porcentaje_meta(self) -> float:
        """
        Obtiene el porcentaje necesario para completar el nivel.
        
        Returns:
            float: Porcentaje necesario para ganar
        """
        return self.porcentaje_victoria

    def revelar_area_circular(self, centro: Tuple[int, int], radio: int) -> None:
        """
        Revela un área circular alrededor de un punto.
        
        Args:
            centro (Tuple[int, int]): Coordenadas (x, y) del centro
            radio (int): Radio del área a revelar
        """
        centro_x, centro_y = centro
        radio_cuadrado = radio * radio
        
        # Calcular límites del área a revisar
        x_min = max(0, centro_x - radio)
        x_max = min(self.ancho - 1, centro_x + radio)
        y_min = max(0, centro_y - radio)
        y_max = min(self.alto - 1, centro_y + radio)
        
        nuevos_pixeles = 0
        
        # Revelar píxeles dentro del círculo
        for x in range(int(x_min), int(x_max) + 1):
            for y in range(int(y_min), int(y_max) + 1):
                # Calcular distancia al cuadrado
                dx = x - centro_x
                dy = y - centro_y
                distancia_cuadrada = dx * dx + dy * dy
                
                if distancia_cuadrada <= radio_cuadrado:
                    if (x, y) not in self.area_segura:
                        self.area_segura.add((x, y))
                        try:
                            color = self.imagen_fondo.get_at((x, y))
                            self.imagen_revelada.set_at((x, y), color)
                            nuevos_pixeles += 1
                        except IndexError:
                            continue
        
        # Actualizar contadores
        self.pixeles_revelados = len(self.area_segura)
        self.puntaje_nivel += nuevos_pixeles * self.puntos_por_pixel
        
        print(f"Área circular revelada: {nuevos_pixeles} nuevos píxeles")

    def agregar_tiempo(self, tiempo_extra: float) -> None:
        """
        Añade tiempo extra al nivel.
        
        Args:
            tiempo_extra (float): Cantidad de tiempo a añadir en segundos
        """
        self.tiempo_restante += tiempo_extra
        if self.tiempo_agotado and self.tiempo_restante > 0:
            self.tiempo_agotado = False 