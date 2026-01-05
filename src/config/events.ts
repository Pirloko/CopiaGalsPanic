/**
 * Sistema de eventos globales del juego
 */
export enum GameEvents {
  // Área/Polígono
  AREA_CLOSED = 'area_closed',
  POLYGON_VALIDATED = 'polygon_validated',
  
  // Player
  PLAYER_HIT = 'player_hit',
  PLAYER_DIED = 'player_died',
  PLAYER_POWERUP_COLLECTED = 'player_powerup_collected',
  
  // Nivel
  LEVEL_COMPLETE = 'level_complete',
  LEVEL_START = 'level_start',
  
  // Power-ups
  POWERUP_COLLECTED = 'powerup_collected',
  POWERUP_SPAWNED = 'powerup_spawned',
  
  // Enemigos
  ENEMY_SPAWNED = 'enemy_spawned',
  ENEMY_DESTROYED = 'enemy_destroyed',
  
  // UI
  SCORE_UPDATED = 'score_updated',
  TIME_UPDATED = 'time_updated',
  LIVES_UPDATED = 'lives_updated',
  
  // Game
  GAME_OVER = 'game_over',
  GAME_PAUSED = 'game_paused',
  GAME_RESUMED = 'game_resumed',
}
