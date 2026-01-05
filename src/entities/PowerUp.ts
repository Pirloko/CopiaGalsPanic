import Phaser from 'phaser';
import { PowerUpType, POWERUP_CONFIG, GAME_CONFIG } from '../config/gameConfig';

/**
 * Entidad de power-up
 * Objetos que otorgan efectos temporales al jugador
 */
export class PowerUp extends Phaser.GameObjects.Arc {
  private powerUpType: PowerUpType;
  private lifetimeTimer?: Phaser.Time.TimerEvent;
  private pulseTween?: Phaser.Tweens.Tween;

  constructor(
    scene: Phaser.Scene,
    x: number,
    y: number,
    type: PowerUpType
  ) {
    const color = PowerUp.getColorForType(type);
    super(scene, x, y, POWERUP_CONFIG.SIZE, 0, 360, false, color);

    this.powerUpType = type;
    this.setupPhysics();
    this.setupVisuals();
    this.startLifetime();
  }

  /**
   * Obtiene el color según el tipo de power-up
   */
  private static getColorForType(type: PowerUpType): number {
    switch (type) {
      case PowerUpType.SHIELD:
        return POWERUP_CONFIG.COLOR_SHIELD;
      case PowerUpType.SLOW:
        return POWERUP_CONFIG.COLOR_SLOW;
      case PowerUpType.FREEZE:
        return POWERUP_CONFIG.COLOR_FREEZE;
      case PowerUpType.EXTRA_LIFE:
        return POWERUP_CONFIG.COLOR_EXTRA_LIFE;
      case PowerUpType.BOMB:
        return POWERUP_CONFIG.COLOR_BOMB;
      default:
        return 0xffffff;
    }
  }

  /**
   * Configura la física del power-up
   */
  private setupPhysics(): void {
    this.scene.add.existing(this);
    this.scene.physics.add.existing(this);

    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setCollideWorldBounds(false);
  }

  /**
   * Configura efectos visuales
   */
  private setupVisuals(): void {
    // Efecto de pulso
    this.pulseTween = this.scene.tweens.add({
      targets: this,
      scaleX: POWERUP_CONFIG.PULSE_SCALE,
      scaleY: POWERUP_CONFIG.PULSE_SCALE,
      duration: 500,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });

    // Efecto de brillo/glow (simulado con alpha)
    this.setAlpha(0.9);
  }

  /**
   * Inicia el temporizador de vida del power-up
   */
  private startLifetime(): void {
    this.lifetimeTimer = this.scene.time.delayedCall(
      POWERUP_CONFIG.LIFETIME,
      () => {
        this.destroy();
      }
    );
  }

  /**
   * Obtiene el tipo del power-up
   */
  public getType(): PowerUpType {
    return this.powerUpType;
  }

  /**
   * Obtiene el nombre del tipo (útil para debug)
   */
  public getTypeName(): string {
    switch (this.powerUpType) {
      case PowerUpType.SHIELD:
        return 'Escudo';
      case PowerUpType.SLOW:
        return 'Ralentización';
      case PowerUpType.FREEZE:
        return 'Congelación';
      case PowerUpType.EXTRA_LIFE:
        return 'Vida Extra';
      case PowerUpType.BOMB:
        return 'Bomba';
      default:
        return 'Desconocido';
    }
  }

  /**
   * Destruye el power-up y limpia recursos
   */
  destroy(): void {
    if (this.lifetimeTimer) {
      this.lifetimeTimer.destroy();
    }
    if (this.pulseTween) {
      this.pulseTween.stop();
      this.pulseTween.destroy();
    }
    super.destroy();
  }
}