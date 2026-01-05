# 🎮 Instrucciones para Ejecutar el Juego Gals Panic

## Requisitos Previos

- Python 3.6 o superior
- pip (gestor de paquetes de Python)

## Instalación de Dependencias

### Opción 1: Instalación Global
```bash
pip3 install pygame==2.5.2
```

### Opción 2: Instalación para Usuario (Recomendado)
```bash
pip3 install --user pygame==2.5.2
```

### Opción 3: Usando Entorno Virtual (Más Seguro)
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
# venv\Scripts\activate

# Instalar pygame
pip install pygame==2.5.2
```

## Ejecución del Juego

### Método 1: Usando el Script Automático
```bash
cd /Users/pirloko/Desktop/PROYECTOS/juegogals-master/project
bash ejecutar.sh
```

### Método 2: Ejecución Directa
```bash
cd /Users/pirloko/Desktop/PROYECTOS/juegogals-master/project
python3 main.py
```

## Verificación de Instalación

Para verificar que pygame está instalado correctamente:
```bash
python3 -c "import pygame; print('Pygame version:', pygame.__version__)"
```

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'pygame'"
- Asegúrate de haber instalado pygame con uno de los métodos anteriores
- Verifica que estés usando la misma versión de Python para instalar y ejecutar

### Error: "Permission denied" al instalar
- Usa `pip3 install --user pygame==2.5.2` para instalar solo para tu usuario
- O usa un entorno virtual (Opción 3)

### Error: "SSL Certificate Error"
- Esto puede ocurrir en algunos sistemas. Intenta:
  ```bash
  pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org pygame==2.5.2
  ```

## Controles del Juego

- **Movimiento**: WASD o Flechas del teclado
- **Trazar líneas**: Click y arrastrar con el mouse
- **Pausa**: ESC
- **Modo Debug**: F3
- **Cambiar Tema**: Teclas 1, 2, 3
- **Continuar nivel**: ESC (en pantalla de completado)

## Estructura de Carpetas Necesaria

El juego necesita:
- `imagenes/` - Carpeta con imágenes de niveles (nivel1.png a nivel10.png)
- `assets/spider.png` - Imagen de la araña
- `config/themes.json` - Configuración de temas
- `sonidos/` - Carpeta con efectos de sonido (opcional)

Si no existen las imágenes, el juego creará una imagen de prueba automáticamente.

## Notas

- El juego se ejecuta en una ventana de 1000x600 píxeles
- Requiere una pantalla con al menos esa resolución
- Los sonidos son opcionales, el juego funcionará sin ellos

