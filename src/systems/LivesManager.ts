import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';

/**
 * Sistema de gestión de vidas del jugador
 */
export class LivesManager {
  private scene: Phaser.Scene;
  private currentLives: number = GAME_CONFIG.INITIAL_LIVES;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }

  /**
   * Reduce una vida
   */
  public loseLife(): void {
    if (this.currentLives > 0) {
      this.currentLives--;
      
      this.scene.events.emit(GameEvents.LIVES_UPDATED, {
        lives: this.currentLives,
      });

      // Verificar si se quedó sin vidas
      if (this.currentLives <= 0) {
        this.scene.events.emit(GameEvents.GAME_OVER, {
          reason: 'lives',
        });
      }
    }
  }

  /**
   * Añade una vida
   */
  public addLife(): void {
    this.currentLives++;
    this.scene.events.emit(GameEvents.LIVES_UPDATED, {
      lives: this.currentLives,
    });
  }

  /**
   * Obtiene el número de vidas actuales
   */
  public getLives(): number {
    return this.currentLives;
  }

  /**
   * Establece el número de vidas
   */
  public setLives(lives: number): void {
    this.currentLives = Math.max(0, lives);
    this.scene.events.emit(GameEvents.LIVES_UPDATED, {
      lives: this.currentLives,
    });
  }

  /**
   * Resetea las vidas al valor inicial
   */
  public reset(): void {
    this.currentLives = GAME_CONFIG.INITIAL_LIVES;
    this.scene.events.emit(GameEvents.LIVES_UPDATED, {
      lives: this.currentLives,
    });
  }
}
