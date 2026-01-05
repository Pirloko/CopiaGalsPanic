import pygame
import os
import math

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (20, 20, 20)
GRIS_OSCURO = (40, 40, 40)
GRIS_CLARO = (60, 60, 60)
ROJO = (255, 0, 0)
ROJO_OSCURO = (180, 0, 0)
MORADO = (128, 0, 128)

# Crear una superficie para la araña (transparente)
tamaño = 128  # Aumentado para más detalle
superficie = pygame.Surface((tamaño, tamaño), pygame.SRCALPHA)

# Función para crear un degradado circular
def dibujar_circulo_degradado(superficie, color_centro, color_borde, pos, radio):
    for r in range(radio, 0, -1):
        factor = r / radio
        color = (
            int(color_centro[0] * factor + color_borde[0] * (1 - factor)),
            int(color_centro[1] * factor + color_borde[1] * (1 - factor)),
            int(color_centro[2] * factor + color_borde[2] * (1 - factor))
        )
        pygame.draw.circle(superficie, color, pos, r)

# Dibujar el cuerpo de la araña (más detallado)
radio_cuerpo = tamaño // 4
radio_abdomen = int(radio_cuerpo * 1.5)

# Dibujar abdomen con degradado y patrón
centro_abdomen = (tamaño//2 + radio_cuerpo//2, tamaño//2)
dibujar_circulo_degradado(superficie, MORADO, NEGRO, centro_abdomen, radio_abdomen)

# Añadir patrón al abdomen
for i in range(4):
    angulo = i * (math.pi / 2)
    x = centro_abdomen[0] + int(math.cos(angulo) * radio_abdomen * 0.7)
    y = centro_abdomen[1] + int(math.sin(angulo) * radio_abdomen * 0.7)
    pygame.draw.circle(superficie, GRIS_CLARO, (x, y), radio_abdomen // 6)

# Dibujar cefalotórax con degradado
centro_cefalotorax = (tamaño//2 - radio_cuerpo//2, tamaño//2)
dibujar_circulo_degradado(superficie, GRIS_OSCURO, NEGRO, centro_cefalotorax, radio_cuerpo)

# Dibujar las patas con más detalle y curvas
puntos_pata = [
    # Patas lado izquierdo
    [(tamaño//2 - radio_cuerpo//2, tamaño//2 - radio_cuerpo//4), (tamaño//4, tamaño//4)],
    [(tamaño//2 - radio_cuerpo//2, tamaño//2), (tamaño//4, tamaño//2)],
    [(tamaño//2 - radio_cuerpo//2, tamaño//2 + radio_cuerpo//4), (tamaño//4, 3*tamaño//4)],
    [(tamaño//2 - radio_cuerpo//2, tamaño//2 + radio_cuerpo//2), (tamaño//3, 7*tamaño//8)],
    # Patas lado derecho
    [(tamaño//2 - radio_cuerpo//2, tamaño//2 - radio_cuerpo//4), (3*tamaño//4, tamaño//4)],
    [(tamaño//2 - radio_cuerpo//2, tamaño//2), (3*tamaño//4, tamaño//2)],
    [(tamaño//2 - radio_cuerpo//2, tamaño//2 + radio_cuerpo//4), (3*tamaño//4, 3*tamaño//4)],
    [(tamaño//2 - radio_cuerpo//2, tamaño//2 + radio_cuerpo//2), (2*tamaño//3, 7*tamaño//8)],
]

# Dibujar cada pata con segmentos y articulaciones más detalladas
for inicio, fin in puntos_pata:
    # Puntos de control para la curva
    control1 = (
        inicio[0] + (fin[0] - inicio[0]) // 3,
        inicio[1] + (fin[1] - inicio[1]) // 3 - 10
    )
    control2 = (
        inicio[0] + 2 * (fin[0] - inicio[0]) // 3,
        inicio[1] + 2 * (fin[1] - inicio[1]) // 3 + 10
    )
    
    # Dibujar segmentos de la pata con grosor variable
    puntos = []
    for t in range(0, 101, 5):
        t = t / 100
        # Fórmula de curva de Bézier cúbica
        x = (1-t)**3 * inicio[0] + 3*(1-t)**2*t * control1[0] + 3*(1-t)*t**2 * control2[0] + t**3 * fin[0]
        y = (1-t)**3 * inicio[1] + 3*(1-t)**2*t * control1[1] + 3*(1-t)*t**2 * control2[1] + t**3 * fin[1]
        puntos.append((int(x), int(y)))
    
    # Dibujar la pata con grosor variable
    for i in range(len(puntos)-1):
        grosor = int(4 * (1 - i/len(puntos)))  # Grosor disminuye hacia el final
        pygame.draw.line(superficie, NEGRO, puntos[i], puntos[i+1], grosor)
    
    # Dibujar articulaciones
    for punto in [puntos[len(puntos)//3], puntos[2*len(puntos)//3]]:
        pygame.draw.circle(superficie, NEGRO, punto, 4)
        pygame.draw.circle(superficie, GRIS_OSCURO, punto, 2)

# Dibujar los ojos con efectos más elaborados
def dibujar_ojo(pos, radio):
    # Sombra del ojo
    pygame.draw.circle(superficie, NEGRO, (pos[0]+1, pos[1]+1), radio+2)
    # Base del ojo
    pygame.draw.circle(superficie, ROJO_OSCURO, pos, radio+1)
    # Ojo principal
    pygame.draw.circle(superficie, ROJO, pos, radio)
    # Brillo principal
    pygame.draw.circle(superficie, (255, 255, 255), (pos[0]-1, pos[1]-1), radio//2)
    # Brillo secundario
    pygame.draw.circle(superficie, (255, 255, 255), (pos[0]+1, pos[1]-2), radio//4)

# Posición de los ojos
radio_ojo = 6
offset_ojo_x = 8
offset_ojo_y = 6
for x in [-offset_ojo_x, offset_ojo_x]:
    dibujar_ojo((centro_cefalotorax[0] + x, centro_cefalotorax[1] - offset_ojo_y), radio_ojo)

# Asegurarse de que existe el directorio assets
if not os.path.exists('assets'):
    os.makedirs('assets')

# Guardar la imagen
pygame.image.save(superficie, "assets/spider.png")
print("Imagen de araña mejorada creada exitosamente en assets/spider.png") 