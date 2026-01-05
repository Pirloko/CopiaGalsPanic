# 🎮 Gals Panic - Phaser 3 Clone

Un clon completo del clásico juego arcade "Gals Panic" implementado con **Phaser 3**, **TypeScript** y **Vite**.

## 📋 Descripción

Juego 2D arcade donde debes:
- Moverte por el área de juego con las **flechas del teclado**
- **Dibujar polígonos** arrastrando el mouse para revelar áreas
- **Atrapar enemigos** dentro de los polígonos cerrados
- Completar niveles alcanzando el porcentaje requerido
- Usar **power-ups** para ayudarte en tu misión

## 🚀 Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Compilar para producción
npm run build
```

## 🎯 Características

### Mecánicas del Juego
- ✅ Sistema completo de dibujo de polígonos con mouse/touch
- ✅ Algoritmo scanline optimizado para rellenado de áreas
- ✅ 5 tipos de enemigos con IA distintiva
- ✅ Sistema de power-ups (5 tipos: Escudo, Ralentización, Congelación, Vida Extra, Bomba)
- ✅ 10 niveles con dificultad progresiva
- ✅ Sistema de puntaje y bonificaciones
- ✅ Gestión de vidas y tiempo

### Sistemas Implementados
- ✅ **Player**: Movimiento suave con aceleración/desaceleración
- ✅ **LineDrawer**: Sistema de dibujo en tiempo real
- ✅ **PolygonFiller**: Rellenado optimizado de polígonos
- ✅ **EnemyManager**: Gestión completa de enemigos y colisiones
- ✅ **PowerUpManager**: Spawn y gestión de power-ups
- ✅ **HUD**: Interfaz completa con tiempo, nivel, puntaje, vidas
- ✅ **AudioManager**: Sistema de audio preparado (estructura completa)

### Scenes
- ✅ **MenuScene**: Menú principal
- ✅ **GameScene**: Escena principal de juego
- ✅ **LevelCompleteScene**: Transición entre niveles
- ✅ **GameOverScene**: Pantalla de fin de juego

## 🎮 Controles

- **Flechas**: Mover el jugador
- **Mouse/Touch**: Click y arrastrar para dibujar polígonos
- **ESPACIO**: Continuar en pantallas de transición
- **R**: Reiniciar (en Game Over)
- **M**: Volver al menú (en Game Over)

## 📁 Estructura del Proyecto

```
src/
├── config/          # Configuración global
│   ├── gameConfig.ts
│   └── events.ts
├── entities/        # Entidades del juego
│   ├── Player.ts
│   ├── Enemy.ts
│   └── PowerUp.ts
├── scenes/          # Scenes de Phaser
│   ├── MenuScene.ts
│   ├── GameScene.ts
│   ├── LevelCompleteScene.ts
│   └── GameOverScene.ts
├── systems/         # Sistemas complejos
│   ├── LineDrawer.ts
│   ├── PolygonFiller.ts
│   ├── EnemyManager.ts
│   ├── PowerUpManager.ts
│   ├── LevelManager.ts
│   ├── TimeManager.ts
│   ├── ScoreManager.ts
│   ├── LivesManager.ts
│   └── AudioManager.ts
├── ui/              # Interfaz de usuario
│   └── HUD.ts
├── utils/           # Utilidades
│   └── geometry.ts
└── main.ts          # Punto de entrada
```

## 🛠️ Stack Tecnológico

- **Phaser 3**: Motor de juegos 2D
- **TypeScript**: Tipado estático
- **Vite**: Build tool y dev server
- **Arcade Physics**: Sistema de física de Phaser

## 📊 Estado del Proyecto

**Estado**: ✅ **COMPLETADO**

El juego está funcionalmente completo con todas las características implementadas:
- ✅ 9 fases de desarrollo completadas
- ✅ Todos los sistemas funcionando
- ✅ Código documentado y optimizado
- ✅ Sin bugs críticos conocidos

## 🎨 Mejoras Futuras (Opcionales)

- Sistema de temas visuales múltiples
- Archivos de audio (el sistema ya está preparado)
- Efectos visuales avanzados (partículas, trails)
- Sistema de pausa
- Ranking/leaderboard
- Más niveles
- Múltiples dificultades

## 📝 Desarrollo

Este proyecto fue desarrollado en **9 fases incrementales**:

1. **FASE 1**: Fundación y estructura base
2. **FASE 2**: Utilidades geométricas y dibujo de líneas
3. **FASE 3**: Sistema de polígonos y rellenado
4. **FASE 4**: HUD y sistemas de juego base
5. **FASE 5**: Enemigos básicos
6. **FASE 6**: Enemigos avanzados y colisiones
7. **FASE 7**: Power-ups
8. **FASE 8**: Sistema completo (menús, transiciones, audio)
9. **FASE 9**: Pulido final y optimización

Ver `PLAN_DE_FASES.md` para más detalles.

## 📄 Licencia

Este proyecto es un clon educativo/divertido del juego original "Gals Panic".

---

**¡Disfruta jugando! 🎮**