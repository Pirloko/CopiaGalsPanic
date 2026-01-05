import Phaser from 'phaser';
import { EnemyType, ENEMY_CONFIG } from '../config/gameConfig';

/**
 * Entidad de enemigo
 * Clase base para todos los tipos de enemigos
 */
export class Enemy extends Phaser.GameObjects.Arc {
  protected enemyType: EnemyType;
  protected speed: number = 0;
  protected target?: Phaser.GameObjects.GameObject; // Target para perseguir (jugador, etc.)
  protected changeDirectionTimer?: Phaser.Time.TimerEvent;
  protected currentDirection: Phaser.Math.Vector2 = new Phaser.Math.Vector2(0, 0);

  constructor(
    scene: Phaser.Scene,
    x: number,
    y: number,
    type: EnemyType,
    color: number = 0xff0000
  ) {
    super(scene, x, y, ENEMY_CONFIG.SIZE, 0, 360, false, color);

    this.enemyType = type;
    this.setupPhysics();
    this.setupType();
  }

  /**
   * Configura la física del enemigo
   */
  private setupPhysics(): void {
    this.scene.add.existing(this);
    this.scene.physics.add.existing(this);

    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setCollideWorldBounds(true);
    body.setBounce(0.5); // Rebote en bordes
  }

  /**
   * Configura el comportamiento según el tipo
   */
  protected setupType(): void {
    switch (this.enemyType) {
      case EnemyType.RANDOM:
        this.speed = ENEMY_CONFIG.SPEED_RANDOM;
        this.setFillStyle(ENEMY_CONFIG.COLOR_RANDOM);
        this.startRandomMovement();
        break;

      case EnemyType.SLOW_CHASER:
        this.speed = ENEMY_CONFIG.SPEED_SLOW_CHASER;
        this.setFillStyle(ENEMY_CONFIG.COLOR_SLOW_CHASER);
        break;

      case EnemyType.BOUNCE:
        this.speed = ENEMY_CONFIG.SPEED_BOUNCE;
        this.setFillStyle(ENEMY_CONFIG.COLOR_BOUNCE);
        this.setupBounce();
        break;

      case EnemyType.FAST_CHASER:
        this.speed = ENEMY_CONFIG.SPEED_FAST_CHASER;
        this.setFillStyle(ENEMY_CONFIG.COLOR_FAST_CHASER);
        break;

      case EnemyType.COMBINED:
        this.speed = ENEMY_CONFIG.SPEED_COMBINED;
        this.setFillStyle(ENEMY_CONFIG.COLOR_COMBINED);
        break;

      default:
        this.speed = ENEMY_CONFIG.SPEED_RANDOM;
        break;
    }
  }

  /**
   * Configura el tipo rebote (bounce más agresivo)
   */
  private setupBounce(): void {
    const body = this.body as Phaser.Physics.Arcade.Body;
    body.setBounce(1.0); // Rebote completo
    body.setCollideWorldBounds(true);
    
    // Dirección inicial aleatoria
    this.changeDirection();
  }

  /**
   * Inicia el movimiento aleatorio (tipo RANDOM)
   */
  private startRandomMovement(): void {
    this.changeDirection();
    
    // Cambiar dirección periódicamente
    this.changeDirectionTimer = this.scene.time.addEvent({
      delay: ENEMY_CONFIG.CHANGE_DIRECTION_INTERVAL,
      callback: this.changeDirection,
      callbackScope: this,
      loop: true,
    });
  }

  /**
   * Cambia la dirección del movimiento (para tipo aleatorio)
   */
  protected changeDirection(): void {
    const angle = Phaser.Math.FloatBetween(0, Math.PI * 2);
    this.currentDirection.setTo(Math.cos(angle), Math.sin(angle));
  }

  /**
   * Establece el target para perseguir (para tipos perseguidor)
   */
  public setTarget(target: Phaser.GameObjects.GameObject): void {
    this.target = target;
  }

  /**
   * Actualiza el enemigo cada frame
   */
  public update(_delta: number, player?: Phaser.GameObjects.GameObject): void {
    const body = this.body as Phaser.Physics.Arcade.Body;

    switch (this.enemyType) {
      case EnemyType.RANDOM:
        // Movimiento aleatorio
        body.setVelocity(
          this.currentDirection.x * this.speed,
          this.currentDirection.y * this.speed
        );
        break;

      case EnemyType.SLOW_CHASER:
      case EnemyType.FAST_CHASER:
        // Perseguir al jugador (velocidad según tipo)
        if (player && 'x' in player && 'y' in player) {
          const dx = (player as any).x - this.x;
          const dy = (player as any).y - this.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance > 0) {
            const velX = (dx / distance) * this.speed;
            const velY = (dy / distance) * this.speed;
            body.setVelocity(velX, velY);
          }
        }
        break;

      case EnemyType.BOUNCE:
        // Movimiento constante con rebote en bordes
        // La física de Phaser maneja el rebote automáticamente
        if (body.velocity.x === 0 && body.velocity.y === 0) {
          // Si está detenido, iniciar movimiento
          body.setVelocity(
            this.currentDirection.x * this.speed,
            this.currentDirection.y * this.speed
          );
        } else {
          // Acelerar ligeramente (simular rebote agresivo)
          const currentSpeed = Math.sqrt(body.velocity.x ** 2 + body.velocity.y ** 2);
          if (currentSpeed < this.speed * 1.5) {
            body.setVelocity(
              body.velocity.x * ENEMY_CONFIG.BOUNCE_ACCELERATION,
              body.velocity.y * ENEMY_CONFIG.BOUNCE_ACCELERATION
            );
          }
        }
        break;

      case EnemyType.COMBINED:
        // Combina comportamiento: persigue pero con movimiento más errático
        if (player && 'x' in player && 'y' in player) {
          const dx = (player as any).x - this.x;
          const dy = (player as any).y - this.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance > 0) {
            // Añadir variación aleatoria al movimiento
            const angle = Math.atan2(dy, dx) + Phaser.Math.FloatBetween(-0.3, 0.3);
            const velX = Math.cos(angle) * this.speed;
            const velY = Math.sin(angle) * this.speed;
            body.setVelocity(velX, velY);
          }
        }
        break;
    }
  }

  /**
   * Obtiene el tipo del enemigo
   */
  public getType(): EnemyType {
    return this.enemyType;
  }

  /**
   * Destruye el enemigo y limpia recursos
   */
  destroy(): void {
    if (this.changeDirectionTimer) {
      this.changeDirectionTimer.destroy();
    }
    super.destroy();
  }
}