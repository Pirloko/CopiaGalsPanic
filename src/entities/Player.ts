import Phaser from 'phaser';
import { PLAYER_CONFIG } from '../config/gameConfig';
import { VirtualJoystick } from '../ui/VirtualJoystick';

/**
 * Entidad del jugador
 * Maneja movimiento, colisiones y estado del jugador
 */
export class Player extends Phaser.GameObjects.Arc {
  private cursors?: Phaser.Types.Input.Keyboard.CursorKeys;
  private virtualJoystick?: VirtualJoystick;
  private velocityX: number = 0;
  private velocityY: number = 0;
  private isInvulnerable: boolean = false;
  private invulnerabilityTimer?: Phaser.Time.TimerEvent;
  private useTouchControls: boolean = false;

  constructor(scene: Phaser.Scene, x: number, y: number, useTouchControls: boolean = false) {
    super(scene, x, y, PLAYER_CONFIG.SIZE, 0, 360, false, PLAYER_CONFIG.COLOR);
    
    scene.add.existing(this);
    scene.physics.add.existing(this);
    
    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setCollideWorldBounds(true);
    body.setBounce(0);
    
    this.useTouchControls = useTouchControls;
    this.setupInput();
  }

  /**
   * Configura los controles (teclado o táctil)
   */
  private setupInput(): void {
    if (this.useTouchControls) {
      // Crear joystick virtual para móviles
      this.virtualJoystick = new VirtualJoystick(this.scene);
    } else {
      // Controles de teclado para desktop
      if (this.scene.input.keyboard) {
        this.cursors = this.scene.input.keyboard.createCursorKeys();
      }
    }
  }

  /**
   * Establece el joystick virtual (llamado desde GameScene si es necesario)
   */
  public setVirtualJoystick(joystick: VirtualJoystick): void {
    this.virtualJoystick = joystick;
    this.useTouchControls = true;
  }

  /**
   * Actualiza el estado del jugador cada frame
   */
  update(delta: number): void {
    const deltaSeconds = delta / 1000;
    const body = this.body as Phaser.Physics.Arcade.Body;
    
    let inputX = 0;
    let inputY = 0;
    
    if (this.useTouchControls && this.virtualJoystick) {
      // Controles táctiles (joystick virtual)
      inputX = this.virtualJoystick.getDirectionX();
      inputY = this.virtualJoystick.getDirectionY();
    } else if (this.cursors) {
      // Controles de teclado
      if (this.cursors.left.isDown) {
        inputX = -1;
      } else if (this.cursors.right.isDown) {
        inputX = 1;
      }
      
      if (this.cursors.up.isDown) {
        inputY = -1;
      } else if (this.cursors.down.isDown) {
        inputY = 1;
      }
    }
    
    // Aplicar movimiento con aceleración/desaceleración
    const targetVelocityX = inputX * PLAYER_CONFIG.SPEED;
    const targetVelocityY = inputY * PLAYER_CONFIG.SPEED;
    
    // Movimiento horizontal
    if (inputX !== 0) {
      if (Math.abs(targetVelocityX - this.velocityX) < PLAYER_CONFIG.ACCELERATION * deltaSeconds) {
        this.velocityX = targetVelocityX;
      } else {
        this.velocityX += (targetVelocityX > this.velocityX ? 1 : -1) * PLAYER_CONFIG.ACCELERATION * deltaSeconds;
        this.velocityX = Phaser.Math.Clamp(this.velocityX, -PLAYER_CONFIG.SPEED, PLAYER_CONFIG.SPEED);
      }
    } else {
      // Desaceleración suave
      if (this.velocityX > 0) {
        this.velocityX = Math.max(0, this.velocityX - PLAYER_CONFIG.DECELERATION * deltaSeconds);
      } else if (this.velocityX < 0) {
        this.velocityX = Math.min(0, this.velocityX + PLAYER_CONFIG.DECELERATION * deltaSeconds);
      }
    }
    
    // Movimiento vertical
    if (inputY !== 0) {
      if (Math.abs(targetVelocityY - this.velocityY) < PLAYER_CONFIG.ACCELERATION * deltaSeconds) {
        this.velocityY = targetVelocityY;
      } else {
        this.velocityY += (targetVelocityY > this.velocityY ? 1 : -1) * PLAYER_CONFIG.ACCELERATION * deltaSeconds;
        this.velocityY = Phaser.Math.Clamp(this.velocityY, -PLAYER_CONFIG.SPEED, PLAYER_CONFIG.SPEED);
      }
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
   * Verifica si el jugador es invulnerable
   */
  getInvulnerable(): boolean {
    return this.isInvulnerable;
  }

  /**
   * Limpia recursos
   */
  destroy(): void {
    if (this.invulnerabilityTimer) {
      this.invulnerabilityTimer.destroy();
    }
    if (this.virtualJoystick) {
      this.virtualJoystick.destroy();
    }
    super.destroy();
  }
}
