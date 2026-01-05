import Phaser from 'phaser';
import { PLAYER_CONFIG } from '../config/gameConfig';

/**
 * Entidad del jugador
 * Maneja movimiento, colisiones y estado del jugador
 */
export class Player extends Phaser.GameObjects.Arc {
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private velocityX: number = 0;
  private velocityY: number = 0;
  private isInvulnerable: boolean = false;
  private invulnerabilityTimer?: Phaser.Time.TimerEvent;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    super(scene, x, y, PLAYER_CONFIG.SIZE, 0, 360, false, PLAYER_CONFIG.COLOR);
    
    scene.add.existing(this);
    scene.physics.add.existing(this);
    
    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setCollideWorldBounds(true);
    body.setBounce(0);
    
    this.setupInput();
  }

  /**
   * Configura los controles del teclado
   */
  private setupInput(): void {
    this.cursors = this.scene.input.keyboard!.createCursorKeys();
  }

  /**
   * Actualiza el estado del jugador cada frame
   */
  update(delta: number): void {
    const deltaSeconds = delta / 1000;
    const body = this.body as Phaser.Physics.Arcade.Body;
    
    // Movimiento horizontal
    if (this.cursors.left.isDown) {
      this.velocityX = Math.max(
        this.velocityX - PLAYER_CONFIG.ACCELERATION * deltaSeconds,
        -PLAYER_CONFIG.SPEED
      );
    } else if (this.cursors.right.isDown) {
      this.velocityX = Math.min(
        this.velocityX + PLAYER_CONFIG.ACCELERATION * deltaSeconds,
        PLAYER_CONFIG.SPEED
      );
    } else {
      // Desaceleración suave
      if (this.velocityX > 0) {
        this.velocityX = Math.max(0, this.velocityX - PLAYER_CONFIG.DECELERATION * deltaSeconds);
      } else if (this.velocityX < 0) {
        this.velocityX = Math.min(0, this.velocityX + PLAYER_CONFIG.DECELERATION * deltaSeconds);
      }
    }
    
    // Movimiento vertical
    if (this.cursors.up.isDown) {
      this.velocityY = Math.max(
        this.velocityY - PLAYER_CONFIG.ACCELERATION * deltaSeconds,
        -PLAYER_CONFIG.SPEED
      );
    } else if (this.cursors.down.isDown) {
      this.velocityY = Math.min(
        this.velocityY + PLAYER_CONFIG.ACCELERATION * deltaSeconds,
        PLAYER_CONFIG.SPEED
      );
    } else {
      // Desaceleración suave
      if (this.velocityY > 0) {
        this.velocityY = Math.max(0, this.velocityY - PLAYER_CONFIG.DECELERATION * deltaSeconds);
      } else if (this.velocityY < 0) {
        this.velocityY = Math.min(0, this.velocityY + PLAYER_CONFIG.DECELERATION * deltaSeconds);
      }
    }
    
    body.setVelocity(this.velocityX, this.velocityY);
  }

  /**
   * Hace al jugador invulnerable temporalmente
   * TODO: Implementar efectos visuales (parpadeo, glow)
   */
  setInvulnerable(duration: number = PLAYER_CONFIG.INVULNERABILITY_TIME): void {
    if (this.invulnerabilityTimer) {
      this.invulnerabilityTimer.destroy();
    }
    
    this.isInvulnerable = true;
    
    this.invulnerabilityTimer = this.scene.time.delayedCall(duration, () => {
      this.isInvulnerable = false;
      this.setAlpha(1);
    });
    
    // Efecto visual básico (parpadeo)
    this.scene.tweens.add({
      targets: this,
      alpha: 0.3,
      duration: 100,
      yoyo: true,
      repeat: Math.floor(duration / 200),
      onComplete: () => {
        this.setAlpha(1);
      }
    });
  }

  /**
   * Obtiene si el jugador es invulnerable
   */
  getInvulnerable(): boolean {
    return this.isInvulnerable;
  }

  /**
   * Destruye el jugador y limpia recursos
   */
  destroy(): void {
    if (this.invulnerabilityTimer) {
      this.invulnerabilityTimer.destroy();
    }
    super.destroy();
  }
}
