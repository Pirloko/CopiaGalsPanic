import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';

/**
 * Sistema de gestión de niveles
 * Maneja el nivel actual, porcentaje requerido y condición de victoria
 */
export class LevelManager {
  private scene: Phaser.Scene;
  private currentLevel: number = 1;
  private requiredPercentage: number = 0;
  private isLevelComplete: boolean = false;

  constructor(scene: Phaser.Scene, startLevel: number = 1) {
    this.scene = scene;
    this.currentLevel = Math.max(1, Math.min(startLevel, GAME_CONFIG.MAX_LEVELS));
    this.calculateRequiredPercentage();
  }

  /**
   * Calcula el porcentaje requerido según el nivel actual
   */
  private calculateRequiredPercentage(): void {
    this.requiredPercentage =
      GAME_CONFIG.BASE_PERCENTAGE_REQUIRED +
      (this.currentLevel - 1) * GAME_CONFIG.PERCENTAGE_INCREASE_PER_LEVEL;
    
    // Limitar al máximo permitido
    this.requiredPercentage = Math.min(
      this.requiredPercentage,
      GAME_CONFIG.MAX_PERCENTAGE_REQUIRED
    );
  }

  /**
   * Verifica si el porcentaje revelado alcanza el requerido
   * @param revealedPercentage Porcentaje actual revelado
   * @returns true si el nivel está completo
   */
  public checkLevelComplete(revealedPercentage: number): boolean {
    if (this.isLevelComplete) return true;

    if (revealedPercentage >= this.requiredPercentage) {
      this.isLevelComplete = true;
      this.scene.events.emit(GameEvents.LEVEL_COMPLETE, {
        level: this.currentLevel,
        percentage: revealedPercentage,
        requiredPercentage: this.requiredPercentage,
      });
      return true;
    }

    return false;
  }

  /**
   * Avanza al siguiente nivel
   */
  public nextLevel(): void {
    if (this.currentLevel < GAME_CONFIG.MAX_LEVELS) {
      this.currentLevel++;
      this.isLevelComplete = false;
      this.calculateRequiredPercentage();
      
      this.scene.events.emit(GameEvents.LEVEL_START, {
        level: this.currentLevel,
        requiredPercentage: this.requiredPercentage,
      });
    }
  }

  /**
   * Obtiene el nivel actual
   */
  public getCurrentLevel(): number {
    return this.currentLevel;
  }

  /**
   * Obtiene el porcentaje requerido para el nivel actual
   */
  public getRequiredPercentage(): number {
    return this.requiredPercentage;
  }

  /**
   * Verifica si el nivel está completo
   */
  public getIsLevelComplete(): boolean {
    return this.isLevelComplete;
  }

  /**
   * Resetea el nivel actual (sin avanzar)
   */
  public resetLevel(): void {
    this.isLevelComplete = false;
  }

  /**
   * Resetea el manager al nivel inicial
   */
  public reset(startLevel: number = 1): void {
    this.currentLevel = Math.max(1, Math.min(startLevel, GAME_CONFIG.MAX_LEVELS));
    this.isLevelComplete = false;
    this.calculateRequiredPercentage();
  }
}
