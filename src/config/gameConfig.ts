/**
 * Configuración global del juego
 */
export const GAME_CONFIG = {
  // Dimensiones
  WIDTH: 1000,
  HEIGHT: 600,
  GAME_AREA_WIDTH: 800,
  GAME_AREA_HEIGHT: 600,
  HUD_WIDTH: 200,
  HUD_HEIGHT: 600,

  // FPS
  TARGET_FPS: 60,

  // Niveles
  MAX_LEVELS: 10,
  INITIAL_LIVES: 3,
  
  // Tiempo
  INITIAL_TIME: 90000, // 90 segundos en ms
  TIME_REDUCTION_PER_LEVEL: 5000, // -5 segundos por nivel
  MIN_TIME: 60000, // 60 segundos mínimo

  // Porcentaje requerido
  BASE_PERCENTAGE_REQUIRED: 75,
  PERCENTAGE_INCREASE_PER_LEVEL: 2,
  MAX_PERCENTAGE_REQUIRED: 95,

  // Enemigos
  MAX_ENEMIES_ACTIVE: 5,

  // Power-ups
  POWERUP_SPAWN_INTERVAL: 8000, // 8 segundos
  MAX_POWERUPS_PER_TYPE: 3,

  // Física
  GRAVITY: 0,
} as const;

/**
 * Configuración del Player
 */
export const PLAYER_CONFIG = {
  SPEED: 200,
  ACCELERATION: 600,
  DECELERATION: 800,
  SIZE: 20,
  COLOR: 0x00ff00,
  START_X: 50,
  START_Y: 300,
  INVULNERABILITY_TIME: 2000, // 2 segundos
} as const;

/**
 * Configuración del sistema de dibujo de líneas
 */
export const LINE_DRAWER_CONFIG = {
  LINE_COLOR: 0xffffff, // Blanco
  LINE_WIDTH: 2,
  CLOSE_INDICATOR_COLOR: 0x00ff00, // Verde
  CLOSE_DISTANCE_THRESHOLD: 30, // Distancia para detectar cierre
  MIN_POINT_DISTANCE: 5, // Distancia mínima entre puntos (evitar acumulación)
  ACTIVE: true, // Si el dibujo está activo
} as const;

/**
 * Configuración del sistema de rellenado de polígonos
 */
export const POLYGON_FILLER_CONFIG = {
  REVEAL_COLOR: 0x4444ff, // Azul para áreas reveladas
  FILL_ALPHA: 0.7,
} as const;

/**
 * Tipos de enemigos
 */
export enum EnemyType {
  RANDOM = 0,           // Movimiento aleatorio
  SLOW_CHASER = 1,      // Perseguidor lento
  BOUNCE = 2,           // Rebote agresivo (FASE 6)
  FAST_CHASER = 3,      // Perseguidor rápido (FASE 6)
  COMBINED = 4,         // Combinado (FASE 6)
}

/**
 * Configuración de enemigos
 */
export const ENEMY_CONFIG = {
  SIZE: 15,
  SPEED_RANDOM: 80,        // Velocidad del tipo aleatorio
  SPEED_SLOW_CHASER: 60,   // Velocidad del perseguidor lento
  SPEED_BOUNCE: 120,       // Velocidad del tipo rebote (acelera)
  SPEED_FAST_CHASER: 100,  // Velocidad del perseguidor rápido
  SPEED_COMBINED: 90,      // Velocidad del tipo combinado
  COLOR_RANDOM: 0xff4444,      // Rojo
  COLOR_SLOW_CHASER: 0xff8844, // Naranja
  COLOR_BOUNCE: 0xff0088,      // Magenta
  COLOR_FAST_CHASER: 0xff0000, // Rojo intenso
  COLOR_COMBINED: 0xff00ff,    // Fucsia
  SPAWN_INTERVAL: 3000,    // Intervalo entre spawns (ms)
  CHANGE_DIRECTION_INTERVAL: 2000, // Intervalo para cambiar dirección (tipo aleatorio)
  BOUNCE_ACCELERATION: 1.1, // Factor de aceleración al rebotar
  POINTS_PER_CAPTURED_ENEMY: 500, // Puntos por enemigo capturado en polígono
} as const;

/**
 * Tipos de power-ups
 */
export enum PowerUpType {
  SHIELD = 0,      // Escudo - Invulnerabilidad temporal
  SLOW = 1,        // Ralentización - Enemigos más lentos
  FREEZE = 2,      // Congelación - Enemigos detenidos
  EXTRA_LIFE = 3,  // Vida Extra - Añade una vida
  BOMB = 4,        // Bomba - Destruye todos los enemigos
}

/**
 * Configuración de power-ups
 */
export const POWERUP_CONFIG = {
  SIZE: 18,
  LIFETIME: 10000, // 10 segundos antes de desaparecer
  SHIELD_DURATION: 5000, // 5 segundos de escudo
  SLOW_DURATION: 4000,   // 4 segundos de ralentización
  FREEZE_DURATION: 3000, // 3 segundos de congelación
  SLOW_MULTIPLIER: 0.5,  // Multiplicador de velocidad (50% más lento)
  COLOR_SHIELD: 0x00ffff,     // Cyan
  COLOR_SLOW: 0x8888ff,       // Azul claro
  COLOR_FREEZE: 0x00ff88,     // Verde azulado
  COLOR_EXTRA_LIFE: 0xff00ff, // Magenta
  COLOR_BOMB: 0xff0000,       // Rojo
  PULSE_SCALE: 1.2,           // Escala de pulso visual
} as const;