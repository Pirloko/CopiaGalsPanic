# Prompt para crear Gals Panic Clone con Phaser 3

## Descripción del Proyecto

Necesito crear un clon completo del juego Gals Panic usando **Phaser 3** (JavaScript/TypeScript). El juego debe ser una recreación fiel del original con todas sus mecánicas, efectos visuales y sistemas.

## Tecnologías y Requisitos

- **Framework**: Phaser 3 (última versión estable)
- **Lenguaje**: TypeScript (preferido) o JavaScript
- **Build Tool**: Vite o Webpack
- **Estilo**: CSS moderno o integrado en Phaser
- **Resolución**: 1000x600 (800x600 área de juego + 200px barra lateral)

## Mecánicas Principales del Juego

### 1. Sistema de Trazado y Revelado
- El jugador debe poder trazar líneas con el mouse/touch arrastrando desde el área segura
- Las líneas deben formar polígonos cerrados que se rellenan automáticamente
- Al cerrar un polígono válido, se revela esa área de la imagen de fondo
- El área segura inicial son los bordes de la pantalla (ya revelados)
- Sistema de predicción visual: mostrar línea verde cuando el jugador está cerca de cerrar el polígono
- Validación de polígonos: mínimo 3 puntos, no debe intersectar con enemigos durante el trazado

### 2. Sistema de Jugador
- **Movimiento**: Control con WASD o flechas del teclado
- **Física**: Movimiento suave con aceleración/desaceleración y easing
- **Velocidad base**: 35 unidades, velocidad máxima 5x la base
- **Efectos visuales**:
  - Estela de partículas que sigue al jugador (60 partículas máximo)
  - Efecto de brillo pulsante
  - Círculo cyan con núcleo blanco
  - Radio de colisión: 6 píxeles
- **Sistema de vidas**: 3 vidas iniciales
- **Invulnerabilidad**: 3 segundos después de recibir daño con efecto de parpadeo
- **Escudo**: Power-up que otorga protección temporal (10 segundos) con efecto visual de pulso y líneas de energía

### 3. Sistema de Enemigos (Arañas)
- **5 tipos diferentes** con comportamientos únicos:
  1. **Araña básica** (nivel 1): Movimiento aleatorio, velocidad 18, color negro/gris
  2. **Araña de hielo** (nivel 2): Persigue al jugador lentamente, velocidad 22, color azul hielo
  3. **Araña gigante** (nivel 3): Rebota agresivamente en bordes, velocidad 26, color marrón
  4. **Araña eléctrica** (nivel 4): Persigue rápidamente, velocidad 30, color azul eléctrico
  5. **Araña de fuego** (nivel 5): Combina comportamientos, cambia cada 3-5 segundos, velocidad 35, color rojo/naranja

- **IA y Comportamiento**:
  - Perseguidora: Calcula dirección hacia el jugador
  - Rebotadora: Mantiene dirección hasta chocar con bordes
  - Aleatoria: Cambia dirección periódicamente
  - Inteligente: Alterna entre comportamientos

- **Efectos visuales**:
  - Animación de 8 patas con movimiento sinusoidal
  - Trail de movimiento (10 puntos máximo)
  - Rotación del cuerpo
  - Partículas de impacto al colisionar
  - Efecto de brillo durante impacto
  - Imagen de sprite para la araña (assets/spider.png)

- **Spawn**: Cada 1.5-2 segundos, máximo 5 enemigos simultáneos
- **Colisiones**: Con jugador, con líneas trazadas, dentro de polígonos cerrados

### 4. Sistema de Power-Ups
Implementar 5 tipos de power-ups con efectos visuales únicos:

1. **Escudo** (Azul cielo):
   - Duración: 10 segundos
   - Efecto: Protege al jugador de un impacto
   - Visual: Símbolo de escudo hexagonal con pulso

2. **Ralentizador** (Verde lima):
   - Duración: 5 segundos
   - Efecto: Reduce velocidad de enemigos al 10%
   - Visual: Símbolo de reloj con manecillas animadas

3. **Congelación** (Azul hielo):
   - Duración: 4 segundos
   - Efecto: Congela todos los enemigos completamente
   - Visual: Copo de nieve con 6 puntas y ramificaciones

4. **Vida Extra** (Rojo brillante):
   - Efecto: Añade una vida (máximo 3)
   - Visual: Corazón animado con efecto de latido

5. **Bomba** (Naranja):
   - Efecto: Revela área circular (150px radio) y elimina enemigos en esa zona
   - Visual: Bomba con mecha, explosión con partículas

- **Generación**: Cada 8 segundos, posición aleatoria
- **Prioridad**: Si jugador tiene 1 vida, generar vida extra cada 4 segundos
- **Límite**: Máximo 3 de cada tipo por nivel
- **Efectos visuales**: Rotación, pulso, partículas decorativas, brillo exterior

### 5. Sistema de Niveles
- **10 niveles** con imágenes diferentes (nivel1.png a nivel10.png)
- **Dificultad progresiva**:
  - Porcentaje requerido: 75% base, aumenta 2% por nivel (máximo 95%)
  - Tiempo límite: 90 segundos base, reduce 5 segundos por nivel (mínimo 60)
- **Carga de imágenes**: Desde carpeta `assets/imagenes/`
- **Área segura inicial**: Bordes de la pantalla revelados
- **Sistema de puntaje**:
  - 1 punto por píxel revelado
  - 10 puntos por segundo restante al completar
  - 100 puntos por cada 1% sobre el mínimo requerido

### 6. Interfaz de Usuario (HUD)
- **Barra lateral derecha** (200px de ancho):
  - Nivel actual (texto grande)
  - Tiempo restante (formato MM:SS, fuente digital)
  - Barra de progreso animada con efecto de brillo
  - Porcentaje actual / Porcentaje meta
  - Puntaje actual (formato con comas)
  - Vidas (corazones estilizados, máximo 3)
- **Efectos visuales**:
  - Partículas decorativas flotantes
  - Transiciones suaves entre niveles
  - Efectos de glow en elementos importantes
  - Texto con sombra para mejor legibilidad
- **Pantalla de nivel completado**:
  - Panel lateral con mensaje "¡FELICIDADES!"
  - Número de nivel completado
  - Efectos de pulso y animación
  - Instrucciones para continuar

### 7. Sistema de Temas
Implementar 3 temas visuales intercambiables:

1. **Neon Nights** (por defecto):
   - Primary: #00ffff (Cyan)
   - Secondary: #ff1493 (Rosa)
   - Accent: #7b2ff7 (Púrpura)
   - Dark: #120458 (Azul oscuro)

2. **Golden Hour**:
   - Primary: #ffd700 (Dorado)
   - Secondary: #ff8c00 (Naranja oscuro)
   - Accent: #ff4500 (Rojo-naranja)
   - Dark: #2c1810 (Marrón oscuro)

3. **Ice Queen**:
   - Primary: #a5f2f3 (Cyan claro)
   - Secondary: #8cd6f7 (Azul cielo)
   - Accent: #4361ee (Azul)
   - Dark: #1a1b4b (Azul marino)

- **Cambio de tema**: Teclas 1, 2, 3
- **Aplicación**: Colores de UI, efectos de partículas, colores de trazado

### 8. Sistema de Sonidos
- **Efectos de sonido** (carpeta `assets/sonidos/`):
  - impacto.wav - Cuando enemigo choca con línea
  - victoria.wav - Al completar nivel
  - daño.wav - Al recibir daño
  - powerup.wav - Al recoger power-up
  - explosion.wav - Al detonar bomba
- **Control de volumen**: Configurable (0.0 a 1.0)
- **Gestión**: Carga asíncrona, reproducción bajo demanda

## Especificaciones Técnicas de Phaser

### Escenas (Scenes)
1. **PreloadScene**: Carga de assets (imágenes, sonidos, fuentes)
2. **MainMenuScene**: Menú principal (opcional)
3. **GameScene**: Escena principal del juego
4. **LevelCompleteScene**: Pantalla de nivel completado
5. **GameOverScene**: Pantalla de game over

### Game Objects y Componentes
- **Player**: Sprite o Graphics con física Arcade
- **Enemy**: Sprite con física Arcade, múltiples tipos
- **PowerUp**: Sprite con física Arcade, diferentes tipos
- **LineDrawer**: Sistema personalizado para trazado de líneas
- **PolygonFiller**: Sistema de relleno de polígonos
- **ParticleSystem**: Sistema de partículas para efectos
- **HUD**: Contenedor UI con elementos de información

### Física
- Usar **Arcade Physics** de Phaser para colisiones
- Configurar grupos de colisión:
  - Grupo de jugador
  - Grupo de enemigos
  - Grupo de power-ups
  - Grupo de líneas trazadas (overlap detection)

### Sistema de Trazado
- Usar `Graphics` de Phaser para dibujar líneas
- Almacenar puntos en array durante el arrastre
- Detectar cierre de polígono (distancia al primer punto < umbral)
- Usar algoritmo de scanline o flood fill para rellenar polígono
- Aplicar máscara o blend mode para revelar imagen de fondo

### Gestión de Imágenes Reveladas
- Usar `RenderTexture` para almacenar áreas reveladas
- O usar sistema de máscaras con `BitmapMask` o `GeometryMask`
- Actualizar textura cuando se revela nueva área

### Sistema de Partículas
- Usar `ParticleEmitterManager` de Phaser
- Configurar emisores para:
  - Estela del jugador
  - Impactos de enemigos
  - Efectos de power-ups
  - Explosiones

### Input
- **Teclado**: WASD/Flechas para movimiento
- **Mouse/Touch**: Click y arrastre para trazado
- **Teclas especiales**:
  - ESC: Pausa / Continuar nivel
  - F3: Modo debug
  - 1, 2, 3: Cambiar tema

## Estructura del Proyecto

```
phaser-gals-panic/
├── src/
│   ├── scenes/
│   │   ├── PreloadScene.ts
│   │   ├── GameScene.ts
│   │   ├── LevelCompleteScene.ts
│   │   └── GameOverScene.ts
│   ├── entities/
│   │   ├── Player.ts
│   │   ├── Enemy.ts
│   │   └── PowerUp.ts
│   ├── systems/
│   │   ├── LineDrawer.ts
│   │   ├── PolygonFiller.ts
│   │   ├── EnemyManager.ts
│   │   ├── PowerUpManager.ts
│   │   ├── LevelManager.ts
│   │   ├── SoundManager.ts
│   │   └── ThemeManager.ts
│   ├── ui/
│   │   ├── HUD.ts
│   │   └── UIComponents.ts
│   ├── utils/
│   │   ├── GeometryUtils.ts
│   │   ├── CollisionUtils.ts
│   │   └── MathUtils.ts
│   ├── config/
│   │   ├── GameConfig.ts
│   │   └── themes.json
│   └── main.ts
├── assets/
│   ├── imagenes/
│   │   ├── nivel1.png
│   │   ├── nivel2.png
│   │   └── ... (nivel10.png)
│   ├── sonidos/
│   │   ├── impacto.wav
│   │   ├── victoria.wav
│   │   ├── daño.wav
│   │   ├── powerup.wav
│   │   └── explosion.wav
│   └── sprites/
│       └── spider.png
├── public/
│   └── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── README.md
```

## Características Adicionales

### Modo Debug (F3)
- Mostrar hitboxes de colisión
- Mostrar vectores de dirección de enemigos
- Mostrar información de FPS
- Mostrar posición del mouse
- Mostrar puntos del trazado actual

### Optimizaciones
- Usar object pooling para enemigos y partículas
- Pre-renderizar elementos estáticos
- Usar `setTexture` en lugar de crear nuevos sprites
- Optimizar detección de colisiones (spatial partitioning si es necesario)
- Lazy loading de imágenes de niveles

### Responsive Design
- Mantener aspect ratio 5:3
- Escalar canvas manteniendo proporciones
- Adaptar UI para diferentes tamaños de pantalla

## Detalles de Implementación Específicos

### Algoritmo de Relleno de Polígonos
- Implementar scanline fill algorithm
- O usar `Graphics.fillPoints()` de Phaser si está disponible
- Validar polígono antes de rellenar (mínimo 3 puntos, no auto-intersectante)

### Sistema de Predicción de Cierre
- Calcular distancia del punto actual al primer punto del trazado
- Si distancia < umbral (60px), mostrar línea verde de predicción
- Al cerrar, conectar automáticamente al punto más cercano

### Gestión de Estado
- Usar Phaser Data Manager o sistema propio para:
  - Nivel actual
  - Vidas
  - Puntaje
  - Tiempo restante
  - Estado de power-ups activos

### Transiciones
- Usar `cameras.main.fade()` para transiciones entre niveles
- Efectos de fade in/out suaves
- Duración configurable por tema

## Requisitos de Performance

- **FPS objetivo**: 60 FPS constante
- **Delta time**: Usar `time.delta` de Phaser para frame-independent updates
- **Límites**:
  - Máximo 5 enemigos simultáneos
  - Máximo 60 partículas en estela del jugador
  - Máximo 30 partículas por impacto
  - Máximo 3 power-ups de cada tipo

## Entregables Esperados

1. Código fuente completo y comentado
2. Assets necesarios (imágenes de niveles, sprite de araña, sonidos)
3. Configuración de build (Vite/Webpack)
4. README con instrucciones de instalación y ejecución
5. Documentación de clases y métodos principales
6. Sistema de temas completamente funcional
7. Todos los power-ups implementados
8. Sistema de sonidos funcional
9. Modo debug implementado
10. 10 niveles con imágenes diferentes

## Notas Adicionales

- El juego debe ser completamente funcional y jugable
- Todos los efectos visuales deben estar implementados
- El código debe ser modular y fácil de extender
- Usar TypeScript para mejor tipado y mantenibilidad
- Seguir las mejores prácticas de Phaser 3
- Comentar código complejo (algoritmos geométricos, IA de enemigos)

---

**Objetivo Final**: Crear una versión completa y pulida del juego Gals Panic usando Phaser 3, manteniendo todas las mecánicas, efectos visuales y sistemas del juego original, pero adaptado a las capacidades y mejores prácticas de Phaser.


