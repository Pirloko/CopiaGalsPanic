import pygame
import os
import math
import random
from typing import List, Tuple, Set

def cargar_imagenes(carpeta: str) -> List[str]:
    """
    Carga todas las imágenes de una carpeta.
    
    Args:
        carpeta (str): Ruta a la carpeta con imágenes
        
    Returns:
        List[str]: Lista de rutas a las imágenes encontradas
    """
    imagenes = []
    extensiones = {'.png', '.jpg', '.jpeg', '.bmp'}
    
    if os.path.exists(carpeta):
        for archivo in os.listdir(carpeta):
            ext = os.path.splitext(archivo)[1].lower()
            if ext in extensiones:
                ruta_completa = os.path.join(carpeta, archivo)
                imagenes.append(ruta_completa)
    
    return sorted(imagenes)  # Ordenar para consistencia

def es_poligono_valido(puntos: List[Tuple[float, float]]) -> bool:
    """
    Verifica si un polígono es válido.
    
    Args:
        puntos (List[Tuple[float, float]]): Lista de puntos que forman el polígono
        
    Returns:
        bool: True si el polígono es válido
    """
    if len(puntos) < 3:
        return False
    
    # Verificar que no haya puntos repetidos consecutivos
    for i in range(len(puntos)):
        if puntos[i] == puntos[(i + 1) % len(puntos)]:
            return False
    
    return True

def ordenar_puntos_horario(puntos: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Ordena los puntos en sentido horario alrededor de su centroide.
    
    Args:
        puntos (List[Tuple[float, float]]): Lista de puntos a ordenar
        
    Returns:
        List[Tuple[float, float]]: Lista de puntos ordenados
    """
    # Calcular el centroide
    cx = sum(x for x, _ in puntos) / len(puntos)
    cy = sum(y for _, y in puntos) / len(puntos)
    
    # Ordenar puntos según su ángulo respecto al centroide
    return sorted(puntos, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

def rellenar_poligono(puntos: List[Tuple[int, int]], ancho: int, alto: int) -> Set[Tuple[int, int]]:
    """
    Rellena un polígono usando el algoritmo de scanline.
    
    Args:
        puntos (List[Tuple[int, int]]): Lista de puntos que forman el polígono
        ancho (int): Ancho máximo permitido
        alto (int): Alto máximo permitido
        
    Returns:
        Set[Tuple[int, int]]: Conjunto de puntos dentro del polígono
    """
    pixeles_dentro = set()
    
    # Encontrar límites verticales
    y_min = max(0, min(y for _, y in puntos))
    y_max = min(alto - 1, max(y for _, y in puntos))
    
    # Para cada línea horizontal
    for y in range(y_min, y_max + 1):
        intersecciones = []
        
        # Encontrar intersecciones con cada segmento del polígono
        for i in range(len(puntos)):
            x1, y1 = puntos[i]
            x2, y2 = puntos[(i + 1) % len(puntos)]
            
            if y1 > y2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            
            if y1 <= y < y2:
                if y2 - y1 != 0:  # Evitar división por cero
                    x = int(x1 + (x2 - x1) * (y - y1) / (y2 - y1))
                    if 0 <= x < ancho:
                        intersecciones.append(x)
        
        # Ordenar las intersecciones
        intersecciones.sort()
        
        # Rellenar entre pares de intersecciones
        for i in range(0, len(intersecciones) - 1, 2):
            if i + 1 < len(intersecciones):
                for x in range(intersecciones[i], intersecciones[i + 1] + 1):
                    if 0 <= x < ancho:
                        pixeles_dentro.add((x, y))
    
    # Asegurar que los puntos del borde estén incluidos
    for x, y in puntos:
        if 0 <= x < ancho and 0 <= y < alto:
            pixeles_dentro.add((x, y))
            # Añadir píxeles adyacentes para asegurar un borde continuo
            for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < ancho and 0 <= ny < alto:
                    pixeles_dentro.add((nx, ny))
    
    return pixeles_dentro

def dibujar_texto_con_borde(superficie: pygame.Surface, texto: str, fuente: pygame.font.Font,
                           color_texto: Tuple[int, int, int], color_borde: Tuple[int, int, int],
                           pos: Tuple[int, int], grosor_borde: int = 2) -> None:
    """
    Dibuja texto con borde para mejor visibilidad.
    
    Args:
        superficie (pygame.Surface): Superficie donde dibujar
        texto (str): Texto a dibujar
        fuente (pygame.font.Font): Fuente a usar
        color_texto (Tuple[int, int, int]): Color RGB del texto
        color_borde (Tuple[int, int, int]): Color RGB del borde
        pos (Tuple[int, int]): Posición (x, y) donde dibujar
        grosor_borde (int): Grosor del borde en píxeles
    """
    # Renderizar el borde
    for dx in range(-grosor_borde, grosor_borde + 1):
        for dy in range(-grosor_borde, grosor_borde + 1):
            if dx*dx + dy*dy <= grosor_borde*grosor_borde:
                texto_surface = fuente.render(texto, True, color_borde)
                superficie.blit(texto_surface, (pos[0] + dx, pos[1] + dy))
    
    # Renderizar el texto principal
    texto_surface = fuente.render(texto, True, color_texto)
    superficie.blit(texto_surface, pos)

def crear_barra_progreso(valor: float, max_valor: float, ancho: int, alto: int,
                        color_barra: Tuple[int, int, int],
                        color_fondo: Tuple[int, int, int] = (50, 50, 50)) -> pygame.Surface:
    """
    Crea una barra de progreso moderna.
    
    Args:
        valor (float): Valor actual
        max_valor (float): Valor máximo
        ancho (int): Ancho de la barra
        alto (int): Alto de la barra
        color_barra (Tuple[int, int, int]): Color RGB de la barra
        color_fondo (Tuple[int, int, int]): Color RGB del fondo
        
    Returns:
        pygame.Surface: Superficie con la barra de progreso
    """
    superficie = pygame.Surface((ancho, alto))
    
    # Dibujar fondo
    pygame.draw.rect(superficie, color_fondo, (0, 0, ancho, alto))
    
    # Calcular ancho de la barra de progreso
    progreso = min(1.0, valor / max_valor)
    ancho_barra = int(ancho * progreso)
    
    # Dibujar barra de progreso
    if ancho_barra > 0:
        pygame.draw.rect(superficie, color_barra, (0, 0, ancho_barra, alto))
    
    return superficie

def detectar_colision_linea_circulo(punto1: Tuple[float, float], punto2: Tuple[float, float],
                                   centro_circulo: Tuple[float, float], radio: float) -> bool:
    """
    Detecta colisión entre una línea y un círculo.
    
    Args:
        punto1 (Tuple[float, float]): Primer punto de la línea
        punto2 (Tuple[float, float]): Segundo punto de la línea
        centro_circulo (Tuple[float, float]): Centro del círculo
        radio (float): Radio del círculo
        
    Returns:
        bool: True si hay colisión
    """
    x1, y1 = punto1
    x2, y2 = punto2
    cx, cy = centro_circulo
    
    # Vector de la línea
    dx = x2 - x1
    dy = y2 - y1
    
    # Longitud de la línea al cuadrado
    len_sq = dx * dx + dy * dy
    
    if len_sq == 0:
        # Los puntos son iguales, verificar distancia al punto
        return math.sqrt((x1 - cx)**2 + (y1 - cy)**2) <= radio
    
    # Proyección del centro del círculo en la línea
    t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / len_sq))
    
    # Punto más cercano en la línea al centro del círculo
    px = x1 + t * dx
    py = y1 + t * dy
    
    # Verificar si la distancia al punto más cercano es menor que el radio
    return math.sqrt((px - cx)**2 + (py - cy)**2) <= radio

def flood_fill(superficie, x, y, color_nuevo, color_objetivo=None):
    """
    Implementa el algoritmo de flood fill (relleno por inundación).
    
    Args:
        superficie (pygame.Surface): Superficie donde aplicar el algoritmo
        x (int): Coordenada X del punto de inicio
        y (int): Coordenada Y del punto de inicio
        color_nuevo (tuple): Color RGB(A) para rellenar
        color_objetivo (tuple, optional): Color a reemplazar. Si es None, 
                                         se usa el color del punto inicial.
    
    Returns:
        set: Conjunto de puntos (x, y) que fueron rellenados
    """
    # Obtener dimensiones de la superficie
    ancho, alto = superficie.get_size()
    
    # Si no se especifica un color objetivo, usar el del punto inicial
    if color_objetivo is None:
        try:
            color_objetivo = superficie.get_at((x, y))
        except IndexError:
            return set()  # Punto fuera de la superficie
    
    # Si el color objetivo es igual al nuevo, no hay nada que hacer
    if color_objetivo == color_nuevo:
        return set()
    
    # Conjunto para almacenar los puntos modificados
    puntos_modificados = set()
    
    # Pila para el algoritmo (evita recursión excesiva)
    pila = [(x, y)]
    
    while pila:
        x, y = pila.pop()
        
        # Verificar si el punto está dentro de los límites
        if x < 0 or x >= ancho or y < 0 or y >= alto:
            continue
        
        # Verificar si el color coincide con el objetivo
        try:
            if superficie.get_at((x, y)) != color_objetivo:
                continue
        except IndexError:
            continue
        
        # Cambiar el color y añadir a los puntos modificados
        superficie.set_at((x, y), color_nuevo)
        puntos_modificados.add((x, y))
        
        # Añadir vecinos a la pila
        pila.append((x + 1, y))
        pila.append((x - 1, y))
        pila.append((x, y + 1))
        pila.append((x, y - 1))
    
    return puntos_modificados

def crear_imagen_prueba(ancho: int = 800, alto: int = 600) -> None:
    """
    Crea una imagen de prueba para el juego.
    
    Args:
        ancho (int): Ancho de la imagen
        alto (int): Alto de la imagen
    """
    # Crear superficie
    superficie = pygame.Surface((ancho, alto))
    
    # Rellenar con un color de fondo
    superficie.fill((50, 50, 50))
    
    # Dibujar algunos elementos aleatorios
    for _ in range(50):
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        x = random.randint(0, ancho)
        y = random.randint(0, alto)
        radio = random.randint(10, 50)
        pygame.draw.circle(superficie, color, (x, y), radio)
    
    # Guardar la imagen
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")
    pygame.image.save(superficie, os.path.join("imagenes", "nivel1.png"))

def punto_en_poligono(punto: Tuple[int, int], poligono: List[Tuple[int, int]]) -> bool:
    """
    Determina si un punto está dentro de un polígono usando el algoritmo de ray casting.
    
    Args:
        punto (Tuple[int, int]): Punto a verificar
        poligono (List[Tuple[int, int]]): Lista de puntos que forman el polígono
        
    Returns:
        bool: True si el punto está dentro del polígono
    """
    x, y = punto
    dentro = False
    
    j = len(poligono) - 1
    for i in range(len(poligono)):
        if ((poligono[i][1] > y) != (poligono[j][1] > y) and
            x < (poligono[j][0] - poligono[i][0]) * (y - poligono[i][1]) /
                (poligono[j][1] - poligono[i][1]) + poligono[i][0]):
            dentro = not dentro
        j = i
    
    return dentro

def distancia_punto_a_segmento(p: Tuple[float, float],
                           a: Tuple[float, float],
                           b: Tuple[float, float]) -> float:
    """
    Calcula la distancia mínima de un punto a un segmento de línea.
    
    Args:
        p (Tuple[float, float]): Punto a verificar (x, y)
        a (Tuple[float, float]): Primer punto del segmento (x1, y1)
        b (Tuple[float, float]): Segundo punto del segmento (x2, y2)
        
    Returns:
        float: Distancia mínima del punto al segmento
    """
    # Vector del segmento
    vx = b[0] - a[0]
    vy = b[1] - a[1]
    
    # Vector del punto al inicio del segmento
    px = p[0] - a[0]
    py = p[1] - a[1]
    
    # Longitud del segmento al cuadrado
    len_sq = vx * vx + vy * vy
    
    if len_sq == 0:
        # Los puntos a y b son el mismo punto
        return math.sqrt(px * px + py * py)
    
    # Proyección del punto sobre la línea (valor entre 0 y 1)
    t = max(0, min(1, (px * vx + py * vy) / len_sq))
    
    # Punto más cercano en la línea
    nx = a[0] + t * vx
    ny = a[1] + t * vy
    
    # Distancia al punto más cercano
    dx = p[0] - nx
    dy = p[1] - ny
    return math.sqrt(dx * dx + dy * dy) 