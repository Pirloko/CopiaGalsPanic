import Phaser from 'phaser';
import { PowerUp } from '../entities/PowerUp';
import { PowerUpType, POWERUP_CONFIG, GAME_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';
import { PLAYER_CONFIG } from '../config/gameConfig';

/**
 * Sistema de gestión de power-ups
 * Maneja spawn, colisiones y efectos de power-ups
 */
export class PowerUpManager {
  private scene: Phaser.Scene;
  private powerUps: PowerUp[] = [];
  private player?: Phaser.GameObjects.GameObject;
  private spawnTimer?: Phaser.Time.TimerEvent;
  private isActive: boolean = false;
  private spawnCounts: Map<PowerUpType, number> = new Map(); // Contador por tipo

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.initializeSpawnCounts();
  }

  /**
   * Inicializa los contadores de spawn
   */
  private initializeSpawnCounts(): void {
    for (let i = 0; i <= 4; i++) {
      this.spawnCounts.set(i as PowerUpType, 0);
    }
  }

  /**
   * Establece la referencia al jugador
   */
  public setPlayer(player: Phaser.GameObjects.GameObject): void {
    this.player = player;
  }

  /**
   * Inicia el sistema de spawn de power-ups
   */
  public startSpawning(): void {
    this.isActive = true;

    // Configurar spawn periódico
    this.spawnTimer = this.scene.time.addEvent({
      delay: GAME_CONFIG.POWERUP_SPAWN_INTERVAL,
      callback: this.spawnPowerUp,
      callbackScope: this,
      loop: true,
    });
  }

  /**
   * Detiene el sistema de spawn
   */
  public stopSpawning(): void {
    this.isActive = false;
    if (this.spawnTimer) {
      this.spawnTimer.destroy();
      this.spawnTimer = undefined;
    }
  }

  /**
   * Genera un power-up en una posición aleatoria
   */
  private spawnPowerUp(): void {
    if (!this.isActive) return;

    // Seleccionar tipo aleatorio que no haya alcanzado el límite
    const availableTypes = this.getAvailableTypes();
    if (availableTypes.length === 0) {
      return; // Todos los tipos han alcanzado su límite
    }

    const type = Phaser.Math.RND.pick(availableTypes);

    // Posición aleatoria dentro del área de juego
    const x = Phaser.Math.Between(
      POWERUP_CONFIG.SIZE,
      GAME_CONFIG.GAME_AREA_WIDTH - POWERUP_CONFIG.SIZE
    );
    const y = Phaser.Math.Between(
      POWERUP_CONFIG.SIZE,
      GAME_CONFIG.GAME_AREA_HEIGHT - POWERUP_CONFIG.SIZE
    );

    const powerUp = new PowerUp(this.scene, x, y, type);

    // Incrementar contador
    const currentCount = this.spawnCounts.get(type) || 0;
    this.spawnCounts.set(type, currentCount + 1);

    this.powerUps.push(powerUp);

    // Emitir evento
    this.scene.events.emit(GameEvents.POWERUP_SPAWNED, {
      powerUp: powerUp,
      type: type,
    });
  }

  /**
   * Obtiene los tipos de power-ups disponibles para spawn
   */
  private getAvailableTypes(): PowerUpType[] {
    const available: PowerUpType[] = [];

    for (let i = 0; i <= 4; i++) {
      const type = i as PowerUpType;
      const count = this.spawnCounts.get(type) || 0;
      if (count < GAME_CONFIG.MAX_POWERUPS_PER_TYPE) {
        available.push(type);
      }
    }

    return available;
  }

  /**
   * Actualiza todos los power-ups y verifica colisiones
   */
  public update(delta: number): void {
    // Verificar colisiones con jugador
    if (this.player) {
      this.checkPlayerCollision();
    }

    // Limpiar power-ups destruidos
    this.powerUps = this.powerUps.filter(powerUp => powerUp.active);
  }

  /**
   * Verifica colisiones entre power-ups y el jugador
   */
  private checkPlayerCollision(): void {
    if (!this.player) return;

    this.powerUps.forEach(powerUp => {
      if (!powerUp.active) return;

      const distance = Phaser.Math.Distance.Between(
        powerUp.x,
        powerUp.y,
        this.player!.x,
        this.player!.y
      );

      const minDistance = POWERUP_CONFIG.SIZE + PLAYER_CONFIG.SIZE;

      if (distance < minDistance) {
        // Colisión detectada: recolectar power-up
        this.collectPowerUp(powerUp);
      }
    });
  }

  /**
   * Recolecta un power-up y aplica su efecto
   */
  private collectPowerUp(powerUp: PowerUp): void {
    const type = powerUp.getType();

    // Decrementar contador
    const currentCount = this.spawnCounts.get(type) || 0;
    if (currentCount > 0) {
      this.spawnCounts.set(type, currentCount - 1);
    }

    // Remover de la lista
    const index = this.powerUps.indexOf(powerUp);
    if (index !== -1) {
      this.powerUps.splice(index, 1);
    }

    // Destruir el power-up
    powerUp.destroy();

    // Emitir evento
    this.scene.events.emit(GameEvents.POWERUP_COLLECTED, {
      type: type,
      typeName: powerUp.getTypeName(),
    });
  }

  /**
   * Obtiene todos los power-ups activos
   */
  public getPowerUps(): PowerUp[] {
    return [...this.powerUps];
  }

  /**
   * Limpia todos los power-ups
   */
  public clearAll(): void {
    this.powerUps.forEach(powerUp => powerUp.destroy());
    this.powerUps = [];
  }

  /**
   * Resetea el sistema
   */
  public reset(): void {
    this.stopSpawning();
    this.clearAll();
    this.initializeSpawnCounts();
  }
}
