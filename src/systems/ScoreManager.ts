import Phaser from 'phaser';
import { GameEvents } from '../config/events';

/**
 * Sistema de gestión de puntaje
 * Calcula y gestiona el puntaje del jugador
 */
export class ScoreManager {
  private scene: Phaser.Scene;
  private currentScore: number = 0;
  private basePointsPerPixel: number = 1; // Puntos base por píxel cuadrado
  private complexityMultiplier: number = 0.1; // Multiplicador por vértice adicional

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }

  /**
   * Añade puntos por área cerrada
   * @param area Área del polígono en píxeles cuadrados
   * @param vertexCount Número de vértices del polígono
   */
  public addAreaScore(area: number, vertexCount: number): void {
    // Puntos base = área * puntos por píxel
    let points = area * this.basePointsPerPixel;

    // Bonificación por complejidad (más vértices = más difícil)
    if (vertexCount > 3) {
      const complexityBonus = (vertexCount - 3) * this.complexityMultiplier;
      points *= 1 + complexityBonus;
    }

    this.currentScore += Math.floor(points);

    // Emitir evento
    this.scene.events.emit(GameEvents.SCORE_UPDATED, {
      score: this.currentScore,
      pointsAdded: Math.floor(points),
    });
  }

  /**
   * Añade bonificación por tiempo restante
   * @param timeRemaining Tiempo restante en milisegundos
   */
  public addTimeBonus(timeRemaining: number): void {
    // Bonificación = tiempo restante en segundos * 10 puntos
    const bonus = Math.floor(timeRemaining / 1000) * 10;
    this.currentScore += bonus;

    this.scene.events.emit(GameEvents.SCORE_UPDATED, {
      score: this.currentScore,
      pointsAdded: bonus,
      isBonus: true,
    });
  }

  /**
   * Añade bonificación por completar nivel
   * @param level Nivel completado
   */
  public addLevelCompleteBonus(level: number): void {
    // Bonificación = nivel * 1000 puntos
    const bonus = level * 1000;
    this.currentScore += bonus;

    this.scene.events.emit(GameEvents.SCORE_UPDATED, {
      score: this.currentScore,
      pointsAdded: bonus,
      isBonus: true,
    });
  }

  /**
   * Obtiene el puntaje actual
   */
  public getScore(): number {
    return this.currentScore;
  }

  /**
   * Establece el puntaje (útil para reset)
   */
  public setScore(score: number): void {
    this.currentScore = Math.max(0, score);
    this.scene.events.emit(GameEvents.SCORE_UPDATED, {
      score: this.currentScore,
      pointsAdded: 0,
    });
  }

  /**
   * Resetea el puntaje
   */
  public reset(): void {
    this.currentScore = 0;
    this.scene.events.emit(GameEvents.SCORE_UPDATED, {
      score: 0,
      pointsAdded: 0,
    });
  }
}
