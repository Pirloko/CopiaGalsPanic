#!/bin/bash

# Script para ejecutar el juego Gals Panic

echo "🎮 Iniciando Gals Panic..."

# Cambiar al directorio del proyecto
cd "$(dirname "$0")"

# Verificar si pygame está instalado
python3 -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Pygame no está instalado. Instalando..."
    pip3 install --user pygame==2.5.2
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar pygame. Intenta ejecutar manualmente:"
        echo "   pip3 install pygame==2.5.2"
        exit 1
    fi
fi

# Verificar que las imágenes existan
if [ ! -d "imagenes" ] || [ -z "$(ls -A imagenes/*.png 2>/dev/null)" ]; then
    echo "⚠️  No se encontraron imágenes. El juego creará una imagen de prueba."
fi

# Ejecutar el juego
echo "🚀 Ejecutando el juego..."
python3 main.py

