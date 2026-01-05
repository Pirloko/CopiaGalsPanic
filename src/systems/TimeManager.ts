import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';

/**
 * Sistema de gestión de tiempo del juego
 * Maneja el tiempo restante según el nivel actual
 */
export class TimeManager {
  private scene: Phaser.Scene;
  private currentTime: number = 0; // Tiempo en milisegundos
  private timerEvent?: Phaser.Time.TimerEvent;
  private isRunning: boolean = false;
  private currentLevel: number = 1;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }

  /**
   * Inicia el temporizador para un nivel específico
   */
  public startTimer(level: number): void {
    this.stopTimer();
    this.currentLevel = level;
    
    // Calcular tiempo según nivel
    this.currentTime = Math.max(
      GAME_CONFIG.INITIAL_TIME - (level - 1) * GAME_CONFIG.TIME_REDUCTION_PER_LEVEL,
      GAME_CONFIG.MIN_TIME
    );

    this.isRunning = true;

    // Emitir evento inicial
    this.scene.events.emit(GameEvents.TIME_UPDATED, {
      time: this.currentTime,
      formatted: this.formatTime(this.currentTime),
    });

    // Configurar timer para reducir tiempo cada segundo
    this.timerEvent = this.scene.time.addEvent({
      delay: 1000, // 1 segundo
      callback: this.updateTime,
      callbackScope: this,
      loop: true,
    });
  }

  /**
   * Actualiza el tiempo (llamado cada segundo)
   */
  private updateTime(): void {
    if (!this.isRunning) return;

    this.currentTime -= 1000; // Reducir 1 segundo

    // Asegurar que no sea negativo
    if (this.currentTime < 0) {
      this.currentTime = 0;
    }

    // Emitir evento de actualización
    this.scene.events.emit(GameEvents.TIME_UPDATED, {
      time: this.currentTime,
      formatted: this.formatTime(this.currentTime),
    });

    // Verificar si el tiempo se agotó
    if (this.currentTime <= 0) {
      this.isRunning = false;
      this.scene.events.emit(GameEvents.GAME_OVER, {
        reason: 'timeout',
        level: this.currentLevel,
      });
    }
  }

  /**
   * Formatea el tiempo en formato MM:SS
   */
  private formatTime(milliseconds: number): string {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }

  /**
   * Detiene el temporizador
   */
  public stopTimer(): void {
    this.isRunning = false;
    if (this.timerEvent) {
      this.timerEvent.destroy();
      this.timerEvent = undefined;
    }
  }

  /**
   * Pausa el temporizador
   */
  public pauseTimer(): void {
    this.isRunning = false;
  }

  /**
   * Reanuda el temporizador
   */
  public resumeTimer(): void {
    if (this.currentTime > 0) {
      this.isRunning = true;
    }
  }

  /**
   * Obtiene el tiempo actual en milisegundos
   */
  public getCurrentTime(): number {
    return this.currentTime;
  }

  /**
   * Obtiene el tiempo formateado (MM:SS)
   */
  public getFormattedTime(): string {
    return this.formatTime(this.currentTime);
  }

  /**
   * Verifica si el temporizador está corriendo
   */
  public getIsRunning(): boolean {
    return this.isRunning;
  }

  /**
   * Resetea el temporizador
   */
  public reset(): void {
    this.stopTimer();
    this.currentTime = 0;
  }
}
