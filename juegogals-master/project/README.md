# Gals Panic Clone

Este proyecto es un clon básico del juego Gals Panic implementado en Python usando la biblioteca Pygame.

## Características

- Trazado de líneas para revelar partes de imágenes de fondo
- Sistema de niveles con diferentes imágenes
- Enemigos que se mueven por la pantalla
- Sistema de vidas y condición de victoria basada en porcentaje revelado
- Soporte para imágenes personalizadas

## Requisitos

- Python 3.x
- Pygame (instalable con `pip install pygame`)

## Cómo jugar

1. Ejecuta `main.py` para iniciar el juego
2. Usa las teclas de flecha para mover al jugador
3. Traza líneas para revelar partes de la imagen saliendo del área segura y volviendo a ella
4. Evita a los enemigos mientras trazas líneas
5. Revela el 80% de la imagen para pasar al siguiente nivel

## Carpeta de imágenes

El juego buscará imágenes en una carpeta llamada `imagenes` en el directorio del juego. Puedes añadir tus propias imágenes en formato PNG, JPG o BMP.

## Controles

- Flechas: Mover al jugador
- R: Reiniciar el juego después de perder
- Espacio: Avanzar al siguiente nivel después de ganar

## Estructura del código

- `main.py`: Punto de entrada del juego y bucle principal
- `jugador.py`: Clase para manejar al jugador y trazado de líneas
- `enemigo.py`: Clase para los enemigos y su comportamiento
- `nivel.py`: Manejo de niveles, imágenes de fondo y áreas reveladas
- `ui.py`: Interfaz de usuario y elementos visuales
- `utils.py`: Funciones de utilidad como relleno de polígonos

## Personalización

Puedes personalizar aspectos del juego modificando las constantes al inicio de cada archivo, como:
- Velocidad del jugador y enemigos
- Porcentaje necesario para ganar
- Número de vidas
- Colores y aspecto visual