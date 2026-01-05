import Phaser from 'phaser';
import { PLAYER_CONFIG } from '../config/gameConfig';
import { VirtualJoystick } from '../ui/VirtualJoystick';
import { Geometry, Point } from '../utils/geometry';
import { LINE_DRAWER_CONFIG } from '../config/gameConfig';

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

  // Estado del trazado (como en el juego original)
  public isTracing: boolean = false;
  private tracePoints: Point[] = [];
  private lastValidPoint: Point | null = null;
  private predictionPoint: Point | null = null;
  private readonly minPointDistance: number = LINE_DRAWER_CONFIG.MIN_POINT_DISTANCE;
  private readonly predictionDistance: number = LINE_DRAWER_CONFIG.CLOSE_DISTANCE_THRESHOLD;

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
    if (!this.useTouchControls) {
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
   * Inicia el trazado (llamado cuando se presiona el botón del mouse/touch)
   */
  public startTracing(): void {
    if (this.isInvulnerable) {
      return; // No permitir trazado mientras está invulnerable
    }
    
    this.isTracing = true;
    this.tracePoints = [{ x: this.x, y: this.y }];
    this.lastValidPoint = { x: this.x, y: this.y };
    this.predictionPoint = null;
  }

  /**
   * Detiene el trazado y retorna los puntos
   */
  public stopTracing(): Point[] {
    if (!this.isTracing) {
      return [];
    }

    this.isTracing = false;

    // Si hay un punto de predicción, usarlo como punto final
    if (this.predictionPoint) {
      this.tracePoints.push(this.predictionPoint);
    } else {
      // Añadir el último punto si es diferente
      const currentPoint = { x: this.x, y: this.y };
      if (!this.lastValidPoint || 
          Geometry.distance(currentPoint, this.lastValidPoint) > 0.1) {
        this.tracePoints.push(currentPoint);
      }
    }

    const points = [...this.tracePoints];
    this.clearTracing();
    return points;
  }

  /**
   * Cancela el trazado sin retornar puntos
   */
  public cancelTracing(): void {
    this.isTracing = false;
    this.clearTracing();
  }

  /**
   * Limpia todas las variables relacionadas con el trazado
   */
  private clearTracing(): void {
    this.tracePoints = [];
    this.lastValidPoint = null;
    this.predictionPoint = null;
  }

  /**
   * Actualiza el trazado basado en la posición del jugador
   */
  private updateTracing(): void {
    if (!this.isTracing) {
      return;
    }

    const currentPoint: Point = { x: this.x, y: this.y };
    
    if (!this.lastValidPoint) {
      this.lastValidPoint = currentPoint;
      return;
    }

    // Calcular distancia al último punto
    const distance = Geometry.distance(currentPoint, this.lastValidPoint);

    // Añadir punto solo si está lo suficientemente lejos
    if (distance >= this.minPointDistance) {
      this.tracePoints.push(currentPoint);
      this.lastValidPoint = currentPoint;
    }

    // Actualizar punto de predicción (para cierre de polígono)
    this.updatePredictionPoint(currentPoint);
  }

  /**
   * Actualiza el punto de predicción para el cierre del polígono
   */
  private updatePredictionPoint(currentPoint: Point): void {
    if (this.tracePoints.length < 3) {
      this.predictionPoint = null;
      return;
    }

    // Ignorar los últimos puntos para evitar conexiones no deseadas
    const pointsToCheck = this.tracePoints.slice(0, -2);
    let closestPoint: Point | null = null;
    let minDistance = this.predictionDistance;

    for (const point of pointsToCheck) {
      const distance = Geometry.distance(currentPoint, point);
      if (distance < minDistance) {
        minDistance = distance;
        closestPoint = point;
      }
    }

    this.predictionPoint = closestPoint;
  }

  /**
   * Obtiene los puntos del trazado actual
   */
  public getTracePoints(): Point[] {
    return [...this.tracePoints];
  }

  /**
   * Obtiene el punto de predicción (para cierre)
   */
  public getPredictionPoint(): Point | null {
    return this.predictionPoint;
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

    // Actualizar trazado si está activo (como en el juego original)
    this.updateTracing();
  }

  /**
   * Establece el estado de invulnerabilidad
   */
  public setInvulnerable(duration: number): void {
    if (this.isInvulnerable) {
      return;
    }

    this.isInvulnerable = true;

    // Crear efecto de parpadeo
    this.setAlpha(0.5);

    if (this.invulnerabilityTimer) {
      this.invulnerabilityTimer.destroy();
    }

    this.invulnerabilityTimer = this.scene.time.delayedCall(duration * 1000, () => {
      this.isInvulnerable = false;
      this.setAlpha(1.0);
      this.invulnerabilityTimer = undefined;
    });
  }

  /**
   * Obtiene si el jugador es invulnerable
   */
  public getIsInvulnerable(): boolean {
    return this.isInvulnerable;
  }
}
